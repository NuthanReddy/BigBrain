"""Tests for bigbrain.ingest.service."""

from pathlib import Path

import pytest

from bigbrain.ingest.service import ingest_path
from bigbrain.kb.models import IngestionResult
from bigbrain.errors import FileAccessError

from tests.conftest import FIXTURES_DIR


class TestIngestPath:
    """Tests for ingest_path()."""

    def test_ingest_single_file(self):
        result = ingest_path(FIXTURES_DIR / "sample.txt")
        assert isinstance(result, IngestionResult)
        assert result.processed == 1
        assert len(result.documents) == 1

    def test_ingest_directory(self):
        result = ingest_path(FIXTURES_DIR)
        assert isinstance(result, IngestionResult)
        assert result.processed >= 4  # sample.txt, .md, .py, .pdf at minimum

    def test_returns_correct_counts(self):
        result = ingest_path(FIXTURES_DIR)
        assert result.processed > 0
        # unsupported.xyz should be skipped
        assert result.skipped > 0
        # All supported files should succeed
        assert result.failed == 0

    def test_type_filter(self):
        result = ingest_path(FIXTURES_DIR, file_type="txt")
        # Only .txt files should be processed
        for doc in result.documents:
            assert doc.source.file_extension == ".txt"
        assert result.processed >= 1

    def test_raises_file_access_error_for_nonexistent(self):
        with pytest.raises(FileAccessError):
            ingest_path("/nonexistent/path/that/does/not/exist")
