"""BigBrain configuration loading module.

Load order (highest precedence wins):
    1. Built-in defaults  – dataclass field defaults in ``BigBrainConfig``
    2. YAML config file   – loaded via ``load_yaml_config()``
    3. Environment vars   – ``BIGBRAIN_*`` prefix, loaded via ``load_env_overrides()``

This means an environment variable will always beat a YAML value, and a YAML
value will always beat the compiled-in default.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Settings model
# ---------------------------------------------------------------------------

@dataclass
class IngestionConfig:
    """Configuration for the ingestion pipeline."""

    supported_extensions: list[str] = field(
        default_factory=lambda: [".txt", ".md", ".pdf", ".py"]
    )
    recursive: bool = True
    skip_hidden: bool = True
    max_file_size_mb: int = 50
    encoding: str = "utf-8"
    encoding_fallback: str = "latin-1"
    # PDF-specific
    pdf_extract_metadata: bool = True
    pdf_preserve_pages: bool = True
    # Python-specific
    py_extract_docstrings: bool = True
    py_extract_symbols: bool = True


@dataclass
class BigBrainConfig:
    """Central configuration object for the BigBrain application."""

    # app
    app_name: str = "bigbrain"
    debug: bool = False

    # logging
    log_level: str = "INFO"
    log_format: str = "console"  # console | json

    # paths
    config_path: str = "config/example.yaml"
    data_dir: str = "data"
    kb_dir: str = "data/kb"

    # providers (reserved for Phase 3+)
    providers: dict = field(default_factory=lambda: {
        "github_copilot": {"enabled": False, "api_key": ""},
        "ollama": {"enabled": False, "base_url": "http://localhost:11434"},
        "lm_studio": {"enabled": False, "base_url": "http://localhost:1234"},
    })

    # ingestion
    ingestion: IngestionConfig = field(default_factory=IngestionConfig)

    # distillation (reserved)
    distillation: dict = field(default_factory=dict)

    # kb (reserved)
    kb: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# YAML section → flat field mapping
# ---------------------------------------------------------------------------

_YAML_FIELD_MAP: dict[str, str] = {
    # app section
    "app.name": "app_name",
    "app.debug": "debug",
    # logging section
    "logging.level": "log_level",
    "logging.format": "log_format",
    # paths section
    "paths.config_path": "config_path",
    "paths.data_dir": "data_dir",
    "paths.kb_dir": "kb_dir",
}

# Sections that map 1-to-1 to dict fields on the dataclass.
_YAML_DICT_SECTIONS = ("providers", "distillation", "kb")


def _flatten_yaml(yaml_data: dict[str, Any]) -> dict[str, Any]:
    """Convert the nested YAML structure into kwargs for BigBrainConfig."""
    flat: dict[str, Any] = {}

    # Scalar fields via the mapping table
    for dotted_key, field_name in _YAML_FIELD_MAP.items():
        section, key = dotted_key.split(".")
        section_data = yaml_data.get(section)
        if isinstance(section_data, dict) and key in section_data:
            flat[field_name] = section_data[key]

    # Dict fields – pass through the whole sub-dict
    for section in _YAML_DICT_SECTIONS:
        if section in yaml_data and isinstance(yaml_data[section], dict):
            flat[section] = yaml_data[section]

    # Special handling for ingestion → IngestionConfig
    if "ingestion" in yaml_data and isinstance(yaml_data["ingestion"], dict):
        ing_data = yaml_data["ingestion"]
        ing_defaults = IngestionConfig()
        ing_kwargs = {}
        for ing_field in fields(IngestionConfig):
            if ing_field.name in ing_data:
                ing_kwargs[ing_field.name] = ing_data[ing_field.name]
        flat["ingestion"] = IngestionConfig(**{
            **{f.name: getattr(ing_defaults, f.name) for f in fields(IngestionConfig)},
            **ing_kwargs,
        })

    return flat


# ---------------------------------------------------------------------------
# YAML loading
# ---------------------------------------------------------------------------

def load_yaml_config(path: str) -> dict[str, Any]:
    """Load a YAML config file and return its contents as a dict.

    Returns an empty dict when the file is not found or when *pyyaml* is not
    installed – in both cases a warning is logged.
    """
    try:
        import yaml  # noqa: WPS433 – optional import
    except ImportError:
        logger.warning(
            "pyyaml is not installed; YAML configuration will not be loaded. "
            "Install it with: pip install pyyaml"
        )
        return {}

    resolved = Path(path)
    if not resolved.is_file():
        logger.warning("Config file not found: %s – using defaults", resolved)
        return {}

    with open(resolved, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    return data if isinstance(data, dict) else {}


# ---------------------------------------------------------------------------
# Environment variable overrides
# ---------------------------------------------------------------------------

_ENV_PREFIX = "BIGBRAIN_"
_INGESTION_ENV_PREFIX = "BIGBRAIN_INGESTION_"

# Fields whose env values should be interpreted as booleans.
_BOOL_FIELDS: set[str] = {f.name for f in fields(BigBrainConfig) if f.type == "bool"}

_VALID_FIELD_NAMES: set[str] = {f.name for f in fields(BigBrainConfig)}

# IngestionConfig field metadata for type coercion
_INGESTION_VALID_FIELDS: set[str] = {f.name for f in fields(IngestionConfig)}
_INGESTION_BOOL_FIELDS: set[str] = {
    f.name for f in fields(IngestionConfig) if f.type == "bool"
}
_INGESTION_INT_FIELDS: set[str] = {
    f.name for f in fields(IngestionConfig) if f.type == "int"
}
_INGESTION_LIST_FIELDS: set[str] = {
    f.name for f in fields(IngestionConfig) if f.type == "list[str]"
}


def _coerce_bool(value: str) -> bool:
    return value.strip().lower() in ("1", "true", "yes", "on")


def load_env_overrides() -> dict[str, Any]:
    """Read ``BIGBRAIN_*`` environment variables and return matching config values.

    **Top-level fields** – ``BIGBRAIN_LOG_LEVEL`` → ``log_level``,
    ``BIGBRAIN_DEBUG`` → ``debug``, etc.  Bool fields are converted from
    common truthy/falsy strings.

    **Nested ingestion fields** – ``BIGBRAIN_INGESTION_*`` variables are
    mapped to :class:`IngestionConfig` fields.  Examples::

        BIGBRAIN_INGESTION_RECURSIVE=false        → ingestion.recursive = False
        BIGBRAIN_INGESTION_SKIP_HIDDEN=true        → ingestion.skip_hidden = True
        BIGBRAIN_INGESTION_MAX_FILE_SIZE_MB=100    → ingestion.max_file_size_mb = 100
        BIGBRAIN_INGESTION_ENCODING=latin-1        → ingestion.encoding = "latin-1"
        BIGBRAIN_INGESTION_SUPPORTED_EXTENSIONS=.txt,.md
            → ingestion.supported_extensions = [".txt", ".md"]

    Type coercion is applied automatically: booleans, integers,
    comma-separated lists, and plain strings.

    Returns
    -------
    dict[str, Any]
        Overrides dict.  May contain an ``"ingestion"`` key holding a
        partially-built :class:`IngestionConfig` when any
        ``BIGBRAIN_INGESTION_*`` variables are present.
    """
    overrides: dict[str, Any] = {}
    ingestion_overrides: dict[str, Any] = {}

    for key, value in os.environ.items():
        if not key.startswith(_ENV_PREFIX):
            continue

        # Check for BIGBRAIN_INGESTION_* first (longer prefix)
        if key.startswith(_INGESTION_ENV_PREFIX):
            ing_field = key[len(_INGESTION_ENV_PREFIX):].lower()
            if ing_field not in _INGESTION_VALID_FIELDS:
                continue
            if ing_field in _INGESTION_BOOL_FIELDS:
                ingestion_overrides[ing_field] = _coerce_bool(value)
            elif ing_field in _INGESTION_INT_FIELDS:
                ingestion_overrides[ing_field] = int(value)
            elif ing_field in _INGESTION_LIST_FIELDS:
                ingestion_overrides[ing_field] = [
                    item.strip() for item in value.split(",") if item.strip()
                ]
            else:
                ingestion_overrides[ing_field] = value
            continue

        # Top-level BIGBRAIN_* fields
        field_name = key[len(_ENV_PREFIX):].lower()
        if field_name not in _VALID_FIELD_NAMES:
            continue
        if field_name in _BOOL_FIELDS:
            overrides[field_name] = _coerce_bool(value)
        else:
            overrides[field_name] = value

    if ingestion_overrides:
        overrides["ingestion"] = ingestion_overrides

    return overrides


# ---------------------------------------------------------------------------
# Main loader
# ---------------------------------------------------------------------------

def load_config(config_path: str | None = None) -> BigBrainConfig:
    """Build a ``BigBrainConfig`` by merging defaults → YAML → env vars.

    Parameters
    ----------
    config_path:
        Path to a YAML config file.  When *None*, the dataclass default
        ``config/example.yaml`` is used (resolved relative to cwd).

    Returns
    -------
    BigBrainConfig
        Fully merged configuration object.
    """
    # 1. Start with built-in defaults
    defaults = BigBrainConfig()

    # Determine which YAML file to load
    yaml_path = config_path if config_path is not None else defaults.config_path

    # 2. Layer YAML values on top
    yaml_raw = load_yaml_config(yaml_path)
    yaml_values = _flatten_yaml(yaml_raw) if yaml_raw else {}

    # 3. Layer env vars on top
    env_values = load_env_overrides()

    # Merge: defaults ← yaml ← env
    merged: dict[str, Any] = {}
    for f in fields(BigBrainConfig):
        if f.name == "ingestion":
            # Special merge: defaults → YAML → env (field-level, not replace)
            base_ing = yaml_values.get("ingestion", IngestionConfig())
            env_ing = env_values.get("ingestion")
            if env_ing:
                ing_kwargs = {
                    fld.name: getattr(base_ing, fld.name)
                    for fld in fields(IngestionConfig)
                }
                ing_kwargs.update(env_ing)
                merged["ingestion"] = IngestionConfig(**ing_kwargs)
            elif "ingestion" in yaml_values:
                merged["ingestion"] = base_ing
            # else: dataclass default is used automatically
        elif f.name in env_values:
            merged[f.name] = env_values[f.name]
        elif f.name in yaml_values:
            merged[f.name] = yaml_values[f.name]
        # else: dataclass default is used automatically

    return BigBrainConfig(**merged)
