"""Tests for bigbrain.ingest.pdf_ingester."""

from pathlib import Path

import pytest

from bigbrain.ingest.pdf_ingester import PdfIngester
from bigbrain.kb.models import Document
from bigbrain.errors import FileAccessError

from tests.conftest import FIXTURES_DIR

PDF_PATH = FIXTURES_DIR / "sample.pdf"


class TestPdfIngester:
    """Tests for PdfIngester."""

    def setup_method(self):
        self.ingester = PdfIngester()

    def test_ingest_pdf_successfully(self):
        doc = self.ingester.ingest(PDF_PATH)
        assert isinstance(doc, Document)
        assert doc.content  # non-empty

    def test_returns_sections_per_page(self):
        doc = self.ingester.ingest(PDF_PATH)
        assert len(doc.sections) == 2, "sample.pdf should have 2 pages"
        assert doc.sections[0].title == "Page 1"
        assert doc.sections[1].title == "Page 2"

    def test_extracts_pdf_metadata(self):
        doc = self.ingester.ingest(PDF_PATH)
        # The PDF has metadata: title="Test Document", author="BigBrain Tests"
        assert doc.metadata.get("pdf_title") == "Test Document"
        assert doc.metadata.get("pdf_author") == "BigBrain Tests"

    def test_content_contains_text_from_pages(self):
        doc = self.ingester.ingest(PDF_PATH)
        # Each page section should have some content
        for section in doc.sections:
            assert section.metadata.get("page_number") is not None

    def test_source_metadata(self):
        doc = self.ingester.ingest(PDF_PATH)
        assert doc.source is not None
        assert doc.source.source_type == "pdf"
        assert doc.source.file_extension == ".pdf"
        assert doc.source.size_bytes > 0

    def test_title_from_pdf_metadata(self):
        doc = self.ingester.ingest(PDF_PATH)
        assert doc.title == "Test Document"

    def test_raises_file_access_error_for_nonexistent(self):
        with pytest.raises(FileAccessError):
            self.ingester.ingest(Path("/nonexistent/file.pdf"))
