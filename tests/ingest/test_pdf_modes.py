"""Tests for PDF mode switching (standard / high_fidelity / max_accuracy)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime

import pytest

from bigbrain.ingest.pdf_ingester import (
    PdfIngester,
    set_active_pdf_mode,
    get_active_pdf_mode,
    VALID_PDF_MODES,
    _split_markdown_sections,
)
from bigbrain.kb.models import Document
from bigbrain.errors import FileAccessError, UserError

from tests.conftest import FIXTURES_DIR

PDF_PATH = FIXTURES_DIR / "sample.pdf"


class TestPdfModeSwitch:
    """Tests for the pdf_mode backend selection."""

    def setup_method(self):
        # Reset to standard before each test
        set_active_pdf_mode("standard")
        self.ingester = PdfIngester()

    def test_default_mode_is_standard(self):
        assert get_active_pdf_mode() == "standard"

    def test_set_valid_modes(self):
        for mode in VALID_PDF_MODES:
            set_active_pdf_mode(mode)
            assert get_active_pdf_mode() == mode

    def test_set_invalid_mode_raises_user_error(self):
        with pytest.raises(UserError, match="Invalid pdf_mode"):
            set_active_pdf_mode("turbo")

    def test_set_empty_mode_raises_user_error(self):
        with pytest.raises(UserError, match="Invalid pdf_mode"):
            set_active_pdf_mode("")

    def test_standard_mode_uses_pymupdf(self):
        set_active_pdf_mode("standard")
        doc = self.ingester.ingest(PDF_PATH)
        assert isinstance(doc, Document)
        assert doc.source.source_type == "pdf"
        assert doc.source.extra.get("pdf_mode") == "standard"

    def test_standard_mode_preserves_existing_behavior(self):
        set_active_pdf_mode("standard")
        doc = self.ingester.ingest(PDF_PATH)
        assert len(doc.sections) == 2  # sample.pdf has 2 pages
        assert doc.sections[0].title == "Page 1"
        assert doc.metadata.get("pdf_title") == "Test Document"


class TestMarkerBackend:
    """Tests for the marker-pdf backend (high_fidelity mode)."""

    def setup_method(self):
        set_active_pdf_mode("standard")
        self.ingester = PdfIngester()

    def test_marker_mode_raises_when_not_installed(self):
        set_active_pdf_mode("high_fidelity")
        with patch.dict("sys.modules", {"marker": None, "marker.converters": None,
                                         "marker.converters.pdf": None,
                                         "marker.models": None,
                                         "marker.output": None}):
            with pytest.raises(UserError, match="marker-pdf is required"):
                self.ingester.ingest(PDF_PATH)

    def test_marker_mode_calls_marker_converter(self):
        set_active_pdf_mode("high_fidelity")

        # Mock the entire marker pipeline
        mock_converter_cls = MagicMock()
        mock_converter_instance = MagicMock()
        mock_converter_cls.return_value = mock_converter_instance

        mock_rendered = MagicMock()
        mock_converter_instance.return_value = mock_rendered

        mock_create_models = MagicMock(return_value={})

        sample_markdown = "# Chapter 1\n\nThis is $O(n \\log n)$ complexity.\n\n## Section 1.1\n\nDetails here."
        mock_text_from_rendered = MagicMock(return_value=(sample_markdown, {}, []))

        with patch.dict("sys.modules", {
            "marker": MagicMock(),
            "marker.converters": MagicMock(),
            "marker.converters.pdf": MagicMock(PdfConverter=mock_converter_cls),
            "marker.models": MagicMock(create_model_dict=mock_create_models),
            "marker.output": MagicMock(text_from_rendered=mock_text_from_rendered),
        }):
            doc = self.ingester.ingest(PDF_PATH)

        assert isinstance(doc, Document)
        assert doc.source.source_type == "pdf"
        assert doc.source.extra.get("pdf_mode") == "high_fidelity"
        assert doc.metadata.get("pdf_mode") == "high_fidelity"
        assert "$O(n" in doc.content
        # Should have sections from heading-based splitting
        assert any("Chapter 1" in s.title for s in doc.sections)

    def test_marker_mode_handles_empty_output(self):
        set_active_pdf_mode("high_fidelity")

        mock_converter_cls = MagicMock()
        mock_converter_instance = MagicMock()
        mock_converter_cls.return_value = mock_converter_instance
        mock_rendered = MagicMock()
        mock_converter_instance.return_value = mock_rendered
        mock_create_models = MagicMock(return_value={})
        mock_text_from_rendered = MagicMock(return_value=("", {}, []))

        with patch.dict("sys.modules", {
            "marker": MagicMock(),
            "marker.converters": MagicMock(),
            "marker.converters.pdf": MagicMock(PdfConverter=mock_converter_cls),
            "marker.models": MagicMock(create_model_dict=mock_create_models),
            "marker.output": MagicMock(text_from_rendered=mock_text_from_rendered),
        }):
            doc = self.ingester.ingest(PDF_PATH)

        assert doc.content == ""

    def test_marker_mode_extracts_images_count(self):
        set_active_pdf_mode("high_fidelity")

        mock_converter_cls = MagicMock()
        mock_converter_instance = MagicMock()
        mock_converter_cls.return_value = mock_converter_instance
        mock_rendered = MagicMock()
        mock_converter_instance.return_value = mock_rendered
        mock_create_models = MagicMock(return_value={})

        fake_images = [b"img1", b"img2", b"img3"]
        mock_text_from_rendered = MagicMock(
            return_value=("# Title\n\nContent", {}, fake_images)
        )

        with patch.dict("sys.modules", {
            "marker": MagicMock(),
            "marker.converters": MagicMock(),
            "marker.converters.pdf": MagicMock(PdfConverter=mock_converter_cls),
            "marker.models": MagicMock(create_model_dict=mock_create_models),
            "marker.output": MagicMock(text_from_rendered=mock_text_from_rendered),
        }):
            doc = self.ingester.ingest(PDF_PATH)

        assert doc.metadata.get("image_count") == 3


class TestChandraBackend:
    """Tests for the chandra-ocr backend (max_accuracy mode)."""

    def setup_method(self):
        set_active_pdf_mode("standard")
        self.ingester = PdfIngester()

    def test_chandra_mode_raises_when_not_installed(self):
        set_active_pdf_mode("max_accuracy")
        with patch.dict("sys.modules", {"chandra_ocr": None}):
            with pytest.raises(UserError, match="chandra-ocr is required"):
                self.ingester.ingest(PDF_PATH)

    def test_chandra_mode_calls_process_pdf(self):
        set_active_pdf_mode("max_accuracy")

        sample_md = "# Algorithm Analysis\n\nThe time complexity is $O(n^2)$.\n\n## Proof\n\nBy induction."
        mock_chandra = MagicMock()
        mock_chandra.process_pdf = MagicMock(return_value=sample_md)

        with patch.dict("sys.modules", {"chandra_ocr": mock_chandra}):
            doc = self.ingester.ingest(PDF_PATH)

        assert isinstance(doc, Document)
        assert doc.source.source_type == "pdf"
        assert doc.source.extra.get("pdf_mode") == "max_accuracy"
        assert "$O(n^2)$" in doc.content

    def test_chandra_mode_handles_list_result(self):
        set_active_pdf_mode("max_accuracy")

        mock_chandra = MagicMock()
        mock_chandra.process_pdf = MagicMock(return_value=["Page 1 content", "Page 2 content"])

        with patch.dict("sys.modules", {"chandra_ocr": mock_chandra}):
            doc = self.ingester.ingest(PDF_PATH)

        assert "Page 1 content" in doc.content
        assert "Page 2 content" in doc.content

    def test_chandra_mode_handles_empty_output(self):
        set_active_pdf_mode("max_accuracy")

        mock_chandra = MagicMock()
        mock_chandra.process_pdf = MagicMock(return_value="")

        with patch.dict("sys.modules", {"chandra_ocr": mock_chandra}):
            doc = self.ingester.ingest(PDF_PATH)

        assert doc.content == ""


class TestSplitMarkdownSections:
    """Tests for _split_markdown_sections helper."""

    def test_splits_by_headings(self):
        md = "# Title\n\nIntro text\n\n## Section A\n\nBody A\n\n## Section B\n\nBody B"
        sections = _split_markdown_sections(md)
        titles = [s.title for s in sections]
        assert "Title" in titles
        assert "Section A" in titles
        assert "Section B" in titles

    def test_leading_text_becomes_introduction(self):
        md = "Some preamble text\n\n# Chapter 1\n\nBody"
        sections = _split_markdown_sections(md)
        assert sections[0].title == "Introduction"
        assert "preamble" in sections[0].content

    def test_no_headings_returns_full_document(self):
        md = "Just plain text\nwith no headings"
        sections = _split_markdown_sections(md)
        assert len(sections) == 1
        assert sections[0].title == "Introduction"
        assert "plain text" in sections[0].content

    def test_empty_text_returns_empty_list(self):
        sections = _split_markdown_sections("")
        assert sections == []

    def test_heading_levels_preserved(self):
        md = "# H1\n\nBody1\n\n## H2\n\nBody2\n\n### H3\n\nBody3"
        sections = _split_markdown_sections(md)
        levels = {s.title: s.level for s in sections}
        assert levels["H1"] == 1
        assert levels["H2"] == 2
        assert levels["H3"] == 3


class TestSourceTypeConsistency:
    """All PDF modes must use source_type='pdf' for downstream compatibility."""

    def setup_method(self):
        self.ingester = PdfIngester()

    def test_standard_source_type_is_pdf(self):
        set_active_pdf_mode("standard")
        doc = self.ingester.ingest(PDF_PATH)
        assert doc.source.source_type == "pdf"

    def test_marker_source_type_is_pdf(self):
        set_active_pdf_mode("high_fidelity")

        mock_converter_cls = MagicMock()
        mock_converter_instance = MagicMock()
        mock_converter_cls.return_value = mock_converter_instance
        mock_rendered = MagicMock()
        mock_converter_instance.return_value = mock_rendered
        mock_create_models = MagicMock(return_value={})
        mock_text_from_rendered = MagicMock(return_value=("# Test\n\nContent", {}, []))

        with patch.dict("sys.modules", {
            "marker": MagicMock(),
            "marker.converters": MagicMock(),
            "marker.converters.pdf": MagicMock(PdfConverter=mock_converter_cls),
            "marker.models": MagicMock(create_model_dict=mock_create_models),
            "marker.output": MagicMock(text_from_rendered=mock_text_from_rendered),
        }):
            doc = self.ingester.ingest(PDF_PATH)
        assert doc.source.source_type == "pdf"

    def test_chandra_source_type_is_pdf(self):
        set_active_pdf_mode("max_accuracy")

        mock_chandra = MagicMock()
        mock_chandra.process_pdf = MagicMock(return_value="# Test\n\nContent")

        with patch.dict("sys.modules", {"chandra_ocr": mock_chandra}):
            doc = self.ingester.ingest(PDF_PATH)
        assert doc.source.source_type == "pdf"


class TestIngestPathPdfMode:
    """Tests that ingest_path() respects the pdf_mode parameter."""

    def test_ingest_path_with_pdf_mode(self):
        from bigbrain.ingest.service import ingest_path
        from bigbrain.config import IngestionConfig

        config = IngestionConfig(supported_extensions=[".pdf"])
        # Standard mode should work with real PDFs
        result = ingest_path(
            str(PDF_PATH),
            config=config,
            pdf_mode="standard",
        )
        assert result.processed == 1
        assert result.documents[0].source.extra.get("pdf_mode") == "standard"

    def test_ingest_path_pdf_mode_overrides_config(self):
        from bigbrain.ingest.service import ingest_path
        from bigbrain.config import IngestionConfig

        config = IngestionConfig(
            supported_extensions=[".pdf"],
            pdf_mode="high_fidelity",
        )
        # CLI override to standard should use standard
        result = ingest_path(
            str(PDF_PATH),
            config=config,
            pdf_mode="standard",
        )
        assert result.processed == 1
        assert result.documents[0].source.extra.get("pdf_mode") == "standard"

    def test_ingest_path_invalid_pdf_mode(self):
        from bigbrain.ingest.service import ingest_path
        from bigbrain.config import IngestionConfig

        config = IngestionConfig(supported_extensions=[".pdf"])
        with pytest.raises(UserError, match="Invalid pdf_mode"):
            ingest_path(str(PDF_PATH), config=config, pdf_mode="invalid")


class TestConfigPdfMode:
    """Tests for pdf_mode in config loading."""

    def test_default_pdf_mode(self):
        from bigbrain.config import IngestionConfig
        cfg = IngestionConfig()
        assert cfg.pdf_mode == "standard"

    def test_valid_pdf_modes_accepted(self):
        from bigbrain.config import IngestionConfig
        for mode in VALID_PDF_MODES:
            cfg = IngestionConfig(pdf_mode=mode)
            assert cfg.pdf_mode == mode


class TestOcrFallback:
    """Tests for Tesseract OCR fallback on scanned pages."""

    def setup_method(self):
        set_active_pdf_mode("standard")
        self.ingester = PdfIngester()

    def test_ocr_triggered_on_sparse_page(self):
        """When PyMuPDF yields <20 chars, _ocr_page should be called."""
        import bigbrain.ingest.pdf_ingester as mod

        with patch.object(mod, '_is_tesseract_available', return_value=True), \
             patch.object(PdfIngester, '_ocr_page', return_value="OCR recovered text here") as mock_ocr:
            # Create a mock fitz page that returns almost no text
            mock_page = MagicMock()
            mock_page.get_text.return_value = "x"  # fewer than 20 chars

            mock_doc = MagicMock()
            mock_doc.__iter__ = lambda self: iter([mock_page])
            mock_doc.__len__ = lambda self: 1
            mock_doc.metadata = {"title": "Scanned Doc"}

            with patch("fitz.open", return_value=mock_doc):
                doc = self.ingester.ingest(PDF_PATH)

            mock_ocr.assert_called_once()
            assert "OCR recovered text here" in doc.content

    def test_ocr_skipped_when_text_is_rich(self):
        """When PyMuPDF yields enough text, OCR should NOT be called."""
        import bigbrain.ingest.pdf_ingester as mod

        with patch.object(PdfIngester, '_ocr_page') as mock_ocr:
            # Real sample.pdf has plenty of text — OCR should not fire
            doc = self.ingester.ingest(PDF_PATH)
            mock_ocr.assert_not_called()

    def test_ocr_graceful_when_tesseract_missing(self):
        """If Tesseract is not installed, OCR fallback returns empty string."""
        import bigbrain.ingest.pdf_ingester as mod

        # Reset cache
        old_cache = mod._tesseract_available
        mod._tesseract_available = None

        try:
            with patch.dict("sys.modules", {"pytesseract": None}):
                mod._tesseract_available = None
                result = PdfIngester._ocr_page(MagicMock(), 1, PDF_PATH)
                assert result == ""
        finally:
            mod._tesseract_available = old_cache

    def test_ocr_page_count_in_metadata(self):
        """Documents with OCR pages should track the count in metadata."""
        import bigbrain.ingest.pdf_ingester as mod

        with patch.object(mod, '_is_tesseract_available', return_value=True), \
             patch.object(PdfIngester, '_ocr_page', return_value="Recovered via OCR"):
            mock_page = MagicMock()
            mock_page.get_text.return_value = ""

            mock_doc = MagicMock()
            mock_doc.__iter__ = lambda self: iter([mock_page, mock_page])
            mock_doc.__len__ = lambda self: 2
            mock_doc.metadata = {}

            with patch("fitz.open", return_value=mock_doc):
                doc = self.ingester.ingest(PDF_PATH)

            assert doc.metadata.get("ocr_pages") == 2
            assert doc.source.extra.get("ocr_pages") == "2"
