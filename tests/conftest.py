"""Shared fixtures and path setup for BigBrain tests."""

import sys
from pathlib import Path

import pytest

# Ensure the src/ layout is importable without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "ingest"


@pytest.fixture(autouse=True)
def _clear_config_cache():
    """Clear the config cache before each test to avoid cross-test pollution."""
    from bigbrain.config import clear_config_cache
    clear_config_cache()
    yield
    clear_config_cache()
