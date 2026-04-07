"""Tests for bigbrain.config."""

import os
from pathlib import Path
from unittest import mock

from bigbrain.config import (
    BigBrainConfig,
    IngestionConfig,
    KBConfig,
    load_config,
    load_env_overrides,
)


class TestDefaultConfig:
    """Tests for default configuration values."""

    def test_default_config_values(self):
        cfg = BigBrainConfig()
        assert cfg.app_name == "bigbrain"
        assert cfg.debug is False
        assert cfg.log_level == "INFO"
        assert isinstance(cfg.ingestion, IngestionConfig)

    def test_default_ingestion_config(self):
        ing = IngestionConfig()
        assert ".txt" in ing.supported_extensions
        assert ".md" in ing.supported_extensions
        assert ".pdf" in ing.supported_extensions
        assert ".py" in ing.supported_extensions
        assert ing.recursive is True
        assert ing.skip_hidden is True
        assert ing.max_file_size_mb == 50


class TestLoadEnvOverrides:
    """Tests for load_env_overrides()."""

    def test_picks_up_bigbrain_vars(self):
        with mock.patch.dict(os.environ, {"BIGBRAIN_LOG_LEVEL": "DEBUG"}, clear=False):
            overrides = load_env_overrides()
            assert overrides.get("log_level") == "DEBUG"

    def test_picks_up_ingestion_vars(self):
        with mock.patch.dict(
            os.environ,
            {"BIGBRAIN_INGESTION_ENCODING": "latin-1"},
            clear=False,
        ):
            overrides = load_env_overrides()
            ing = overrides.get("ingestion", {})
            assert ing.get("encoding") == "latin-1"

    def test_bool_coercion_true_values(self):
        for val in ("true", "1", "yes", "on", "True", "TRUE"):
            with mock.patch.dict(os.environ, {"BIGBRAIN_DEBUG": val}, clear=False):
                overrides = load_env_overrides()
                assert overrides.get("debug") is True, f"Failed for '{val}'"

    def test_bool_coercion_false_values(self):
        for val in ("false", "0", "no", "off"):
            with mock.patch.dict(os.environ, {"BIGBRAIN_DEBUG": val}, clear=False):
                overrides = load_env_overrides()
                assert overrides.get("debug") is False, f"Failed for '{val}'"

    def test_supported_extensions_parsed_as_list(self):
        with mock.patch.dict(
            os.environ,
            {"BIGBRAIN_INGESTION_SUPPORTED_EXTENSIONS": ".txt,.md,.rs"},
            clear=False,
        ):
            overrides = load_env_overrides()
            ing = overrides.get("ingestion", {})
            exts = ing.get("supported_extensions")
            assert exts == [".txt", ".md", ".rs"]

    def test_max_file_size_mb_parsed_as_int(self):
        with mock.patch.dict(
            os.environ,
            {"BIGBRAIN_INGESTION_MAX_FILE_SIZE_MB": "100"},
            clear=False,
        ):
            overrides = load_env_overrides()
            ing = overrides.get("ingestion", {})
            assert ing.get("max_file_size_mb") == 100
            assert isinstance(ing["max_file_size_mb"], int)

    def test_config_precedence_env_over_yaml(self):
        with mock.patch.dict(
            os.environ,
            {"BIGBRAIN_LOG_LEVEL": "WARNING"},
            clear=False,
        ):
            cfg = load_config()
            assert cfg.log_level == "WARNING"


class TestKBConfig:
    """Tests for KBConfig defaults and kb_db_path derivation."""

    def test_default_kb_config(self):
        kb = KBConfig()
        assert kb.backend == "sqlite"
        assert kb.db_path == ""

    def test_kb_db_path_derived_from_kb_dir(self):
        cfg = BigBrainConfig(kb_dir="data/kb")
        assert cfg.kb_db_path == str(Path("data/kb") / "bigbrain.db")

    def test_kb_db_path_explicit_overrides(self):
        cfg = BigBrainConfig(kb=KBConfig(db_path="/custom/path.db"))
        assert cfg.kb_db_path == "/custom/path.db"

    def test_kb_env_overrides(self):
        with mock.patch.dict(
            os.environ,
            {"BIGBRAIN_KB_DB_PATH": "/env/override.db"},
            clear=False,
        ):
            cfg = load_config()
            assert cfg.kb.db_path == "/env/override.db"
            assert cfg.kb_db_path == "/env/override.db"
