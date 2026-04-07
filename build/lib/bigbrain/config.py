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

from bigbrain.providers.config import (
    GitHubCopilotConfig,
    LMStudioConfig,
    OllamaConfig,
    ProviderConfig,
)

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
class KBConfig:
    """Configuration for the knowledge base storage layer."""

    backend: str = "sqlite"  # sqlite (only option for now)
    db_path: str = ""  # empty = derive from BigBrainConfig.kb_dir


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

    # providers
    providers: ProviderConfig = field(default_factory=ProviderConfig)

    # ingestion
    ingestion: IngestionConfig = field(default_factory=IngestionConfig)

    # distillation (reserved)
    distillation: dict = field(default_factory=dict)

    # kb
    kb: KBConfig = field(default_factory=KBConfig)

    @property
    def kb_db_path(self) -> str:
        """Resolved database path: explicit kb.db_path or derived from kb_dir."""
        if self.kb.db_path:
            return self.kb.db_path
        return str(Path(self.kb_dir) / "bigbrain.db")


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
_YAML_DICT_SECTIONS = ("distillation",)


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

    # Special handling for kb → KBConfig
    if "kb" in yaml_data and isinstance(yaml_data["kb"], dict):
        kb_data = yaml_data["kb"]
        kb_defaults = KBConfig()
        kb_kwargs = {}
        for kb_field in fields(KBConfig):
            if kb_field.name in kb_data:
                kb_kwargs[kb_field.name] = kb_data[kb_field.name]
        flat["kb"] = KBConfig(**{
            **{f.name: getattr(kb_defaults, f.name) for f in fields(KBConfig)},
            **kb_kwargs,
        })

    # Special handling for providers → ProviderConfig
    if "providers" in yaml_data and isinstance(yaml_data["providers"], dict):
        prov_data = yaml_data["providers"]
        ollama_kwargs = {}
        if "ollama" in prov_data and isinstance(prov_data["ollama"], dict):
            ollama_defaults = OllamaConfig()
            for f in fields(OllamaConfig):
                if f.name in prov_data["ollama"]:
                    ollama_kwargs[f.name] = prov_data["ollama"][f.name]
            ollama_cfg = OllamaConfig(**{
                **{f.name: getattr(ollama_defaults, f.name) for f in fields(OllamaConfig)},
                **ollama_kwargs,
            })
        else:
            ollama_cfg = OllamaConfig()

        lms_kwargs = {}
        if "lm_studio" in prov_data and isinstance(prov_data["lm_studio"], dict):
            lms_defaults = LMStudioConfig()
            for f in fields(LMStudioConfig):
                if f.name in prov_data["lm_studio"]:
                    lms_kwargs[f.name] = prov_data["lm_studio"][f.name]
            lms_cfg = LMStudioConfig(**{
                **{f.name: getattr(lms_defaults, f.name) for f in fields(LMStudioConfig)},
                **lms_kwargs,
            })
        else:
            lms_cfg = LMStudioConfig()

        ghc_kwargs = {}
        if "github_copilot" in prov_data and isinstance(prov_data["github_copilot"], dict):
            ghc_defaults = GitHubCopilotConfig()
            for f in fields(GitHubCopilotConfig):
                if f.name in prov_data["github_copilot"]:
                    ghc_kwargs[f.name] = prov_data["github_copilot"][f.name]
            ghc_cfg = GitHubCopilotConfig(**{
                **{f.name: getattr(ghc_defaults, f.name) for f in fields(GitHubCopilotConfig)},
                **ghc_kwargs,
            })
        else:
            ghc_cfg = GitHubCopilotConfig()

        flat["providers"] = ProviderConfig(
            preferred_provider=prov_data.get("preferred_provider", ""),
            ollama=ollama_cfg, lm_studio=lms_cfg, github_copilot=ghc_cfg,
        )

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
_KB_ENV_PREFIX = "BIGBRAIN_KB_"
_PROVIDERS_ENV_PREFIX = "BIGBRAIN_PROVIDERS_"

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

# KBConfig field metadata
_KB_VALID_FIELDS: set[str] = {f.name for f in fields(KBConfig)}


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

    **Nested KB fields** – ``BIGBRAIN_KB_*`` variables are mapped to
    :class:`KBConfig` fields.  Examples::

        BIGBRAIN_KB_BACKEND=sqlite    → kb.backend = "sqlite"
        BIGBRAIN_KB_DB_PATH=/tmp/bb.db → kb.db_path = "/tmp/bb.db"

    Type coercion is applied automatically: booleans, integers,
    comma-separated lists, and plain strings.

    Returns
    -------
    dict[str, Any]
        Overrides dict.  May contain ``"ingestion"`` and/or ``"kb"``
        keys when any nested variables are present.
    """
    overrides: dict[str, Any] = {}
    ingestion_overrides: dict[str, Any] = {}
    kb_overrides: dict[str, Any] = {}
    providers_overrides: dict[str, Any] = {}

    for key, value in os.environ.items():
        if not key.startswith(_ENV_PREFIX):
            continue

        # Check for BIGBRAIN_PROVIDERS_* (e.g. BIGBRAIN_PROVIDERS_PREFERRED)
        if key.startswith(_PROVIDERS_ENV_PREFIX):
            prov_field = key[len(_PROVIDERS_ENV_PREFIX):].lower()
            if prov_field == "preferred":
                providers_overrides["preferred_provider"] = value
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

        # Check for BIGBRAIN_KB_*
        if key.startswith(_KB_ENV_PREFIX):
            kb_field = key[len(_KB_ENV_PREFIX):].lower()
            if kb_field not in _KB_VALID_FIELDS:
                continue
            kb_overrides[kb_field] = value
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
    if kb_overrides:
        overrides["kb"] = kb_overrides
    if providers_overrides:
        overrides["providers"] = providers_overrides

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
        elif f.name == "kb":
            # Special merge: defaults → YAML → env (field-level)
            base_kb = yaml_values.get("kb", KBConfig())
            env_kb = env_values.get("kb")
            if env_kb:
                kb_kwargs = {
                    fld.name: getattr(base_kb, fld.name)
                    for fld in fields(KBConfig)
                }
                kb_kwargs.update(env_kb)
                merged["kb"] = KBConfig(**kb_kwargs)
            elif "kb" in yaml_values:
                merged["kb"] = base_kb
            # else: dataclass default is used automatically
        elif f.name == "providers":
            # Special merge: defaults → YAML → env (field-level)
            base_prov = yaml_values.get("providers", ProviderConfig())
            env_prov = env_values.get("providers")
            if env_prov:
                prov_kwargs = {
                    fld.name: getattr(base_prov, fld.name)
                    for fld in fields(ProviderConfig)
                }
                prov_kwargs.update(env_prov)
                merged["providers"] = ProviderConfig(**prov_kwargs)
            elif "providers" in yaml_values:
                merged["providers"] = base_prov
            # else: dataclass default is used automatically
        elif f.name in env_values:
            merged[f.name] = env_values[f.name]
        elif f.name in yaml_values:
            merged[f.name] = yaml_values[f.name]
        # else: dataclass default is used automatically

    return BigBrainConfig(**merged)
