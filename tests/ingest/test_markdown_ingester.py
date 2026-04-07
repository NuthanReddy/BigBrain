"""Tests for bigbrain.ingest.markdown_ingester."""

from pathlib import Path

import pytest

from bigbrain.ingest.markdown_ingester import MarkdownIngester
from bigbrain.kb.models import Document
from bigbrain.errors import FileAccessError

from tests.conftest import FIXTURES_DIR


class TestMarkdownIngester:
    """Tests for MarkdownIngester."""

    def setup_method(self):
        self.ingester = MarkdownIngester()

    def test_ingest_sample_md(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.md")
        assert isinstance(doc, Document)
        assert doc.content  # non-empty
        assert doc.language == "markdown"

    def test_extracts_heading_sections(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.md")
        assert len(doc.sections) > 0
        # Check that sections have titles
        section_titles = [s.title for s in doc.sections]
        assert "Section One" in section_titles
        assert "Section Two" in section_titles

    def test_infers_title_from_first_h1(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.md")
        assert doc.title == "Sample Markdown Document"

    def test_extracts_internal_links(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.md")
        internal_links = doc.metadata.get("internal_links", [])
        assert len(internal_links) > 0
        hrefs = [link["href"] for link in internal_links]
        assert "./other-doc.md" in hrefs

    def test_returns_correct_metadata_counts(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.md")
        assert doc.metadata.get("heading_count", 0) > 0
        assert doc.metadata.get("link_count", 0) > 0

    def test_source_metadata(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.md")
        assert doc.source is not None
        assert doc.source.source_type == "md"
        assert doc.source.file_extension == ".md"

    def test_raises_file_access_error_for_nonexistent(self):
        with pytest.raises(FileAccessError):
            self.ingester.ingest(Path("/nonexistent/file.md"))
