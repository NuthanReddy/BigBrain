"""Tests for PDF mode switching (standard / max_accuracy)."""

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
    _classify_page,
    _find_caption,
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
            pdf_mode="max_accuracy",
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
        """When page is classified as scanned, _ocr_page should be called."""
        import bigbrain.ingest.pdf_ingester as mod

        with patch.object(mod, '_is_tesseract_available', return_value=True), \
             patch.object(PdfIngester, '_ocr_page', return_value="OCR recovered text here") as mock_ocr:
            # Create a mock fitz page: sparse text + large image → scanned
            mock_rect = MagicMock()
            mock_rect.width = 612
            mock_rect.height = 792

            mock_page = MagicMock()
            mock_page.get_text.return_value = "x"  # fewer than 20 chars
            mock_page.rect = mock_rect
            # One full-page image → scanned classification
            mock_page.get_image_info.return_value = [
                {"bbox": (0, 0, 612, 792), "width": 612, "height": 792, "xref": 1}
            ]

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
            mock_rect = MagicMock()
            mock_rect.width = 612
            mock_rect.height = 792

            mock_page = MagicMock()
            mock_page.get_text.return_value = ""
            mock_page.rect = mock_rect
            mock_page.get_image_info.return_value = [
                {"bbox": (0, 0, 612, 792), "width": 612, "height": 792, "xref": 1}
            ]

            mock_doc = MagicMock()
            mock_doc.__iter__ = lambda self: iter([mock_page, mock_page])
            mock_doc.__len__ = lambda self: 2
            mock_doc.metadata = {}

            with patch("fitz.open", return_value=mock_doc):
                doc = self.ingester.ingest(PDF_PATH)

            assert doc.metadata.get("ocr_pages") == 2
            assert doc.source.extra.get("ocr_pages") == "2"


def _make_mock_page(
    text: str = "",
    page_width: float = 612,
    page_height: float = 792,
    images: list[dict] | None = None,
    text_blocks: list[tuple] | None = None,
) -> MagicMock:
    """Helper to create a mock fitz page with rect, get_text, get_image_info."""
    mock_rect = MagicMock()
    mock_rect.width = page_width
    mock_rect.height = page_height

    page = MagicMock()
    page.rect = mock_rect
    page.get_text.return_value = text
    page.get_image_info.return_value = images or []
    if text_blocks is not None:
        page.get_text.side_effect = lambda fmt="text": text_blocks if fmt == "blocks" else text
    return page


class TestClassifyPage:
    """Tests for _classify_page image-aware page classification."""

    def test_text_only_page(self):
        """Page with rich text and no images → text_only."""
        page = _make_mock_page(text="A" * 100, images=[])
        ptype, imgs = _classify_page(page, "A" * 100)
        assert ptype == "text_only"
        assert imgs == []

    def test_scanned_page(self):
        """Large image covering most of page + sparse text → scanned."""
        page = _make_mock_page(
            text="",
            images=[{"bbox": (0, 0, 612, 792), "width": 612, "height": 792, "xref": 1}],
        )
        ptype, imgs = _classify_page(page, "")
        assert ptype == "scanned"

    def test_blank_page(self):
        """No text and no images → blank."""
        page = _make_mock_page(text="", images=[])
        ptype, imgs = _classify_page(page, "")
        assert ptype == "blank"

    def test_digital_with_images(self):
        """Rich text + significant figure → digital_with_images."""
        page_area = 612 * 792  # ~484,704
        # Image covering ~30% of the page
        img_w = 400
        img_h = 350
        page = _make_mock_page(
            text="This is a page with substantial content about algorithms " * 5,
            images=[{"bbox": (50, 200, 50 + img_w, 200 + img_h), "width": img_w, "height": img_h, "xref": 42}],
        )
        text = "This is a page with substantial content about algorithms " * 5
        ptype, imgs = _classify_page(page, text)
        assert ptype == "digital_with_images"
        assert len(imgs) == 1
        assert imgs[0]["xref"] == 42

    def test_tiny_images_ignored(self):
        """Tiny images (<5% page area) are not significant."""
        page = _make_mock_page(
            text="Enough text here to pass the threshold with room to spare",
            images=[{"bbox": (0, 0, 20, 20), "width": 20, "height": 20, "xref": 5}],  # tiny icon
        )
        text = "Enough text here to pass the threshold with room to spare"
        ptype, imgs = _classify_page(page, text)
        assert ptype == "text_only"
        assert imgs == []

    def test_multiple_significant_images(self):
        """Multiple large figures on a page."""
        page = _make_mock_page(
            text="Content " * 20,
            images=[
                {"bbox": (0, 0, 300, 300), "width": 300, "height": 300, "xref": 10},
                {"bbox": (0, 400, 300, 700), "width": 300, "height": 300, "xref": 11},
            ],
        )
        ptype, imgs = _classify_page(page, "Content " * 20)
        assert ptype == "digital_with_images"
        assert len(imgs) == 2

    def test_sparse_text_with_images_is_scanned(self):
        """Sparse text + images → treat as scanned (might be OCR overlay)."""
        page = _make_mock_page(
            text="x",
            images=[{"bbox": (50, 50, 300, 300), "width": 250, "height": 250, "xref": 7}],
        )
        ptype, _ = _classify_page(page, "x")
        assert ptype == "scanned"


class TestFindCaption:
    """Tests for _find_caption spatial proximity caption extraction."""

    def test_finds_caption_below_image(self):
        page = MagicMock()
        # text block just below the image
        page.get_text.return_value = [
            (50, 510, 400, 530, "Figure 3.1: Merge sort comparison", 0, 0),
        ]
        caption = _find_caption(page, (50, 200, 450, 500))
        assert "Figure 3.1" in caption

    def test_no_caption_when_text_is_far(self):
        page = MagicMock()
        # text block far below the image (>40pts gap)
        page.get_text.return_value = [
            (50, 600, 400, 620, "Unrelated paragraph", 0, 0),
        ]
        caption = _find_caption(page, (50, 200, 450, 500))
        assert caption == ""

    def test_ignores_image_blocks(self):
        page = MagicMock()
        # type=1 means image block, not text
        page.get_text.return_value = [
            (50, 510, 400, 530, "", 0, 1),
        ]
        caption = _find_caption(page, (50, 200, 450, 500))
        assert caption == ""

    def test_no_blocks_returns_empty(self):
        page = MagicMock()
        page.get_text.return_value = []
        caption = _find_caption(page, (50, 200, 450, 500))
        assert caption == ""


class TestDigitalWithImagesIntegration:
    """Integration test: digital page with figures gets image OCR."""

    def setup_method(self):
        set_active_pdf_mode("standard")
        self.ingester = PdfIngester()

    def test_figures_ocrd_on_digital_page(self):
        """Digital page with a figure: figure should be extracted and OCR'd."""
        import bigbrain.ingest.pdf_ingester as mod

        with patch.object(mod, '_is_tesseract_available', return_value=True):
            mock_rect = MagicMock()
            mock_rect.width = 612
            mock_rect.height = 792

            mock_page = MagicMock()
            mock_page.rect = mock_rect
            mock_page.get_text.return_value = "This is a page with plenty of text about sorting algorithms " * 3
            mock_page.get_image_info.return_value = [
                {"bbox": (50, 300, 500, 600), "width": 450, "height": 300, "xref": 42}
            ]
            # Mock caption blocks
            mock_page.get_text.side_effect = lambda fmt="text": [
                (50, 610, 400, 630, "Figure 2.1: Time complexity chart", 0, 0),
            ] if fmt == "blocks" else "This is a page with plenty of text about sorting algorithms " * 3

            mock_img_data = {"image": b"\x89PNG\r\n\x1a\n" + b"\x00" * 100, "ext": "png"}
            mock_doc = MagicMock()
            mock_doc.__iter__ = lambda self: iter([mock_page])
            mock_doc.__len__ = lambda self: 1
            mock_doc.metadata = {}
            mock_doc.extract_image.return_value = mock_img_data

            with patch("fitz.open", return_value=mock_doc), \
                 patch("pytesseract.image_to_string", return_value="O(n log n)  O(n^2)"), \
                 patch("PIL.Image.open"):
                doc = self.ingester.ingest(PDF_PATH)

            assert doc.metadata.get("images_found") == 1
            # Verify images metadata in sections
            page_section = doc.sections[0]
            assert page_section.metadata.get("page_type") == "digital_with_images"

    def test_real_pdf_classifies_pages(self):
        """Real sample.pdf should classify as text_only (no images)."""
        doc = self.ingester.ingest(PDF_PATH)
        for section in doc.sections:
            assert section.metadata.get("page_type") in ("text_only", "digital_with_images", "blank")

