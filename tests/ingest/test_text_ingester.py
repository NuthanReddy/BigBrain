"""Tests for bigbrain.ingest.text_ingester."""

from pathlib import Path

import pytest

from bigbrain.ingest.text_ingester import TextIngester
from bigbrain.kb.models import Document
from bigbrain.errors import FileAccessError

from tests.conftest import FIXTURES_DIR


class TestTextIngester:
    """Tests for TextIngester."""

    def setup_method(self):
        self.ingester = TextIngester()

    def test_ingest_sample_txt(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.txt")
        assert isinstance(doc, Document)
        assert doc.content  # non-empty
        assert "sample text file" in doc.content.lower()

    def test_returns_correct_title(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.txt")
        # Title inferred from filename: "sample" → "Sample"
        assert doc.title == "Sample"

    def test_returns_correct_source_metadata(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.txt")
        assert doc.source is not None
        assert doc.source.source_type == "txt"
        assert doc.source.file_extension == ".txt"
        assert doc.source.size_bytes > 0
        assert doc.source.modified_at is not None

    def test_handles_empty_file(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "empty.txt")
        assert isinstance(doc, Document)
        assert doc.content == ""
        assert doc.metadata.get("line_count") == 0

    def test_raises_file_access_error_for_nonexistent(self):
        with pytest.raises(FileAccessError):
            self.ingester.ingest(Path("/nonexistent/file.txt"))
