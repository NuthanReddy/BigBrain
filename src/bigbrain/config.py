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
class DistillConfig:
    """Configuration for the distillation pipeline."""
    chunk_strategy: str = "by_section"  # "by_section", "sliding_window", "by_paragraph"
    chunk_size: int = 1000  # max characters per chunk (for sliding_window)
    chunk_overlap: int = 200  # overlap between chunks (for sliding_window)
    summary_max_length: int = 500  # max words for summaries
    entity_extraction: bool = True
    relationship_extraction: bool = True
    max_chunks_per_doc: int = 50  # safety limit


@dataclass
class CompileConfig:
    """Configuration for the knowledge compilation pipeline."""
    output_dir: str = "build"  # directory for compiled output files
    default_format: str = "markdown"  # markdown, flashcard, cheatsheet, qa, study_guide
    flashcard_count: int = 20  # max flashcards per document
    qa_count: int = 15  # max Q&A pairs per document
    include_relationships: bool = True
    include_entities: bool = True


@dataclass
class NotionConfig:
    """Configuration for the Notion integration."""
    enabled: bool = False
    token: str = ""  # Notion integration token (ntn_*); also reads BIGBRAIN_NOTION_TOKEN env var
    default_page_id: str = ""  # Default parent page for exports
    sync_direction: str = "bidirectional"  # bidirectional | import_only | export_only
    auto_create_pages: bool = True  # Create new Notion pages on export if not mapped


@dataclass
class StoreConfig:
    """Configuration for the polyglot entity store."""
    backend: str = "sqlite"  # sqlite | postgres | neo4j | qdrant | weaviate | pinecone
    # PostgreSQL + pgvector
    postgres_url: str = ""  # e.g., "postgresql://user:pass@localhost:5432/bigbrain"
    # Neo4j
    neo4j_url: str = ""  # e.g., "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = ""
    # Qdrant
    qdrant_url: str = ""  # e.g., "http://localhost:6333"
    qdrant_collection: str = "bigbrain_entities"
    # Weaviate
    weaviate_url: str = ""  # e.g., "http://localhost:8080"
    # Pinecone
    pinecone_api_key: str = ""
    pinecone_index: str = "bigbrain-entities"
    pinecone_environment: str = ""


@dataclass
class PluginConfig:
    """Configuration for the plugin system."""
    plugins_dir: str = "plugins"  # directory to scan for plugin files
    auto_discover: bool = True  # auto-discover plugins on startup
    enabled_plugins: list[str] = field(default_factory=list)  # empty = all discovered
    disabled_plugins: list[str] = field(default_factory=list)


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

    # distillation
    distillation: DistillConfig = field(default_factory=DistillConfig)

    # compile
    compile: CompileConfig = field(default_factory=CompileConfig)

    # kb
    kb: KBConfig = field(default_factory=KBConfig)

    # notion
    notion: NotionConfig = field(default_factory=NotionConfig)

    # plugins
    plugins: PluginConfig = field(default_factory=PluginConfig)

    # entity store
    entity_store: StoreConfig = field(default_factory=StoreConfig)

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
_YAML_DICT_SECTIONS = ("providers",)


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

    # Special handling for distillation → DistillConfig
    if "distillation" in yaml_data and isinstance(yaml_data["distillation"], dict):
        dist_data = yaml_data["distillation"]
        dist_defaults = DistillConfig()
        dist_kwargs = {}
        for dist_field in fields(DistillConfig):
            if dist_field.name in dist_data:
                dist_kwargs[dist_field.name] = dist_data[dist_field.name]
        flat["distillation"] = DistillConfig(**{
            **{f.name: getattr(dist_defaults, f.name) for f in fields(DistillConfig)},
            **dist_kwargs,
        })

    # Special handling for compile → CompileConfig
    if "compile" in yaml_data and isinstance(yaml_data["compile"], dict):
        comp_data = yaml_data["compile"]
        comp_defaults = CompileConfig()
        comp_kwargs = {}
        for comp_field in fields(CompileConfig):
            if comp_field.name in comp_data:
                comp_kwargs[comp_field.name] = comp_data[comp_field.name]
        flat["compile"] = CompileConfig(**{
            **{f.name: getattr(comp_defaults, f.name) for f in fields(CompileConfig)},
            **comp_kwargs,
        })

    # Special handling for notion → NotionConfig
    if "notion" in yaml_data and isinstance(yaml_data["notion"], dict):
        notion_data = yaml_data["notion"]
        notion_defaults = NotionConfig()
        notion_kwargs = {}
        for notion_field in fields(NotionConfig):
            if notion_field.name in notion_data:
                notion_kwargs[notion_field.name] = notion_data[notion_field.name]
        flat["notion"] = NotionConfig(**{
            **{f.name: getattr(notion_defaults, f.name) for f in fields(NotionConfig)},
            **notion_kwargs,
        })

    # Special handling for plugins → PluginConfig
    if "plugins" in yaml_data and isinstance(yaml_data["plugins"], dict):
        plugin_data = yaml_data["plugins"]
        plugin_defaults = PluginConfig()
        plugin_kwargs = {}
        for plugin_field in fields(PluginConfig):
            if plugin_field.name in plugin_data:
                plugin_kwargs[plugin_field.name] = plugin_data[plugin_field.name]
        flat["plugins"] = PluginConfig(**{
            **{f.name: getattr(plugin_defaults, f.name) for f in fields(PluginConfig)},
            **plugin_kwargs,
        })

    # Special handling for entity_store → StoreConfig
    if "entity_store" in yaml_data and isinstance(yaml_data["entity_store"], dict):
        store_data = yaml_data["entity_store"]
        store_defaults = StoreConfig()
        store_kwargs = {}
        for store_field in fields(StoreConfig):
            if store_field.name in store_data:
                store_kwargs[store_field.name] = store_data[store_field.name]
        flat["entity_store"] = StoreConfig(**{
            **{f.name: getattr(store_defaults, f.name) for f in fields(StoreConfig)},
            **store_kwargs,
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
_DISTILL_ENV_PREFIX = "BIGBRAIN_DISTILL_"
_COMPILE_ENV_PREFIX = "BIGBRAIN_COMPILE_"
_NOTION_ENV_PREFIX = "BIGBRAIN_NOTION_"
_PLUGINS_ENV_PREFIX = "BIGBRAIN_PLUGINS_"
_STORE_ENV_PREFIX = "BIGBRAIN_STORE_"

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

# DistillConfig field metadata for type coercion
_DISTILL_VALID_FIELDS: set[str] = {f.name for f in fields(DistillConfig)}
_DISTILL_BOOL_FIELDS: set[str] = {
    f.name for f in fields(DistillConfig) if f.type == "bool"
}
_DISTILL_INT_FIELDS: set[str] = {
    f.name for f in fields(DistillConfig) if f.type == "int"
}

# CompileConfig field metadata for type coercion
_COMPILE_VALID_FIELDS: set[str] = {f.name for f in fields(CompileConfig)}
_COMPILE_BOOL_FIELDS: set[str] = {
    f.name for f in fields(CompileConfig) if f.type == "bool"
}
_COMPILE_INT_FIELDS: set[str] = {
    f.name for f in fields(CompileConfig) if f.type == "int"
}

# NotionConfig field metadata for type coercion
_NOTION_VALID_FIELDS: set[str] = {f.name for f in fields(NotionConfig)}
_NOTION_BOOL_FIELDS: set[str] = {
    f.name for f in fields(NotionConfig) if f.type == "bool"
}

# PluginConfig field metadata for type coercion
_PLUGINS_VALID_FIELDS: set[str] = {f.name for f in fields(PluginConfig)}
_PLUGINS_BOOL_FIELDS: set[str] = {
    f.name for f in fields(PluginConfig) if f.type == "bool"
}
_PLUGINS_LIST_FIELDS: set[str] = {
    f.name for f in fields(PluginConfig) if f.type == "list[str]"
}

# StoreConfig field metadata for type coercion
_STORE_VALID_FIELDS: set[str] = {f.name for f in fields(StoreConfig)}


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
    distill_overrides: dict[str, Any] = {}
    compile_overrides: dict[str, Any] = {}
    notion_overrides: dict[str, Any] = {}
    plugins_overrides: dict[str, Any] = {}
    store_overrides: dict[str, Any] = {}

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

        # Check for BIGBRAIN_DISTILL_*
        if key.startswith(_DISTILL_ENV_PREFIX):
            dist_field = key[len(_DISTILL_ENV_PREFIX):].lower()
            if dist_field not in _DISTILL_VALID_FIELDS:
                continue
            if dist_field in _DISTILL_BOOL_FIELDS:
                distill_overrides[dist_field] = _coerce_bool(value)
            elif dist_field in _DISTILL_INT_FIELDS:
                distill_overrides[dist_field] = int(value)
            else:
                distill_overrides[dist_field] = value
            continue

        # Check for BIGBRAIN_NOTION_*
        if key.startswith(_NOTION_ENV_PREFIX):
            notion_field = key[len(_NOTION_ENV_PREFIX):].lower()
            if notion_field not in _NOTION_VALID_FIELDS:
                continue
            if notion_field in _NOTION_BOOL_FIELDS:
                notion_overrides[notion_field] = _coerce_bool(value)
            else:
                notion_overrides[notion_field] = value
            continue

        # Check for BIGBRAIN_PLUGINS_*
        if key.startswith(_PLUGINS_ENV_PREFIX):
            plugin_field = key[len(_PLUGINS_ENV_PREFIX):].lower()
            if plugin_field not in _PLUGINS_VALID_FIELDS:
                continue
            if plugin_field in _PLUGINS_BOOL_FIELDS:
                plugins_overrides[plugin_field] = _coerce_bool(value)
            elif plugin_field in _PLUGINS_LIST_FIELDS:
                plugins_overrides[plugin_field] = [
                    item.strip() for item in value.split(",") if item.strip()
                ]
            else:
                plugins_overrides[plugin_field] = value
            continue

        # Check for BIGBRAIN_COMPILE_*
        if key.startswith(_COMPILE_ENV_PREFIX):
            comp_field = key[len(_COMPILE_ENV_PREFIX):].lower()
            if comp_field not in _COMPILE_VALID_FIELDS:
                continue
            if comp_field in _COMPILE_BOOL_FIELDS:
                compile_overrides[comp_field] = _coerce_bool(value)
            elif comp_field in _COMPILE_INT_FIELDS:
                compile_overrides[comp_field] = int(value)
            else:
                compile_overrides[comp_field] = value
            continue

        # Check for BIGBRAIN_STORE_*
        if key.startswith(_STORE_ENV_PREFIX):
            store_field = key[len(_STORE_ENV_PREFIX):].lower()
            if store_field not in _STORE_VALID_FIELDS:
                continue
            store_overrides[store_field] = value
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
    if distill_overrides:
        overrides["distillation"] = distill_overrides
    if compile_overrides:
        overrides["compile"] = compile_overrides
    if notion_overrides:
        overrides["notion"] = notion_overrides
    if plugins_overrides:
        overrides["plugins"] = plugins_overrides
    if store_overrides:
        overrides["entity_store"] = store_overrides

    return overrides


# ---------------------------------------------------------------------------
# Main loader
# ---------------------------------------------------------------------------

_config_cache: BigBrainConfig | None = None
_config_cache_path: str | None = None


def clear_config_cache() -> None:
    """Clear the config cache (useful for tests)."""
    global _config_cache, _config_cache_path
    _config_cache = None
    _config_cache_path = None


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
    global _config_cache, _config_cache_path

    # Return cached config if path matches
    effective_path = config_path or "config/example.yaml"
    if _config_cache is not None and _config_cache_path == effective_path:
        return _config_cache

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
        elif f.name == "distillation":
            # Special merge: defaults → YAML → env (field-level)
            base_dist = yaml_values.get("distillation", DistillConfig())
            env_dist = env_values.get("distillation")
            if env_dist:
                dist_kwargs = {
                    fld.name: getattr(base_dist, fld.name)
                    for fld in fields(DistillConfig)
                }
                dist_kwargs.update(env_dist)
                merged["distillation"] = DistillConfig(**dist_kwargs)
            elif "distillation" in yaml_values:
                merged["distillation"] = base_dist
            # else: dataclass default is used automatically
        elif f.name == "compile":
            # Special merge: defaults → YAML → env (field-level)
            base_comp = yaml_values.get("compile", CompileConfig())
            env_comp = env_values.get("compile")
            if env_comp:
                comp_kwargs = {
                    fld.name: getattr(base_comp, fld.name)
                    for fld in fields(CompileConfig)
                }
                comp_kwargs.update(env_comp)
                merged["compile"] = CompileConfig(**comp_kwargs)
            elif "compile" in yaml_values:
                merged["compile"] = base_comp
            # else: dataclass default is used automatically
        elif f.name == "notion":
            # Special merge: defaults → YAML → env (field-level)
            base_notion = yaml_values.get("notion", NotionConfig())
            env_notion = env_values.get("notion")
            if env_notion:
                notion_kwargs = {
                    fld.name: getattr(base_notion, fld.name)
                    for fld in fields(NotionConfig)
                }
                notion_kwargs.update(env_notion)
                merged["notion"] = NotionConfig(**notion_kwargs)
            elif "notion" in yaml_values:
                merged["notion"] = base_notion
            # else: dataclass default is used automatically
        elif f.name == "plugins":
            # Special merge: defaults → YAML → env (field-level)
            base_plugins = yaml_values.get("plugins", PluginConfig())
            env_plugins = env_values.get("plugins")
            if env_plugins:
                plugins_kwargs = {
                    fld.name: getattr(base_plugins, fld.name)
                    for fld in fields(PluginConfig)
                }
                plugins_kwargs.update(env_plugins)
                merged["plugins"] = PluginConfig(**plugins_kwargs)
            elif "plugins" in yaml_values:
                merged["plugins"] = base_plugins
            # else: dataclass default is used automatically
        elif f.name == "entity_store":
            # Special merge: defaults → YAML → env (field-level)
            base_store = yaml_values.get("entity_store", StoreConfig())
            env_store = env_values.get("entity_store")
            if env_store:
                store_kwargs = {
                    fld.name: getattr(base_store, fld.name)
                    for fld in fields(StoreConfig)
                }
                store_kwargs.update(env_store)
                merged["entity_store"] = StoreConfig(**store_kwargs)
            elif "entity_store" in yaml_values:
                merged["entity_store"] = base_store
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

    result = BigBrainConfig(**merged)
    _config_cache = result
    _config_cache_path = effective_path
    return result
