"""Shared fixtures and path setup for BigBrain tests."""

import sys
from pathlib import Path

# Ensure the src/ layout is importable without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "ingest"
