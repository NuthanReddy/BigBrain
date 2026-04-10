"""PDF file ingester with configurable backends.

Supports three extraction modes controlled by ``pdf_mode`` in config or CLI:

- ``standard`` – PyMuPDF text extraction + Tesseract OCR for scanned pages.
  Pages with little/no embedded text are rendered to images and OCR'd.
- ``high_fidelity`` – marker-pdf.  Markdown output with LaTeX math, tables,
  figures.  Requires ``pip install 'bigbrain[marker]'``.
- ``max_accuracy`` – chandra-ocr.  Highest benchmark scores for math/tables.
  Requires ``pip install 'bigbrain[chandra]'``.
"""

from __future__ import annotations

import io
import re
from datetime import datetime
from pathlib import Path

from bigbrain.ingest.registry import BaseIngester
from bigbrain.kb.models import Document, DocumentSection, SourceMetadata
from bigbrain.errors import FileAccessError, UserError
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)

VALID_PDF_MODES = ("standard", "high_fidelity", "max_accuracy")

# Heuristic: lines made mostly of non-alphanumeric chars are likely
# figure debris (card suits, box-drawing, stray symbols).
_JUNK_LINE_RE = re.compile(r"^[\s\W]{4,}$")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

# Pages with fewer than this many non-whitespace chars trigger OCR
_OCR_MIN_CHARS = 20

# Runtime pdf_mode — set by ingest_path() from config/CLI before calling ingest()
_active_pdf_mode: str = "standard"

# Lazy-cached Tesseract availability check
_tesseract_available: bool | None = None


def _is_tesseract_available() -> bool:
    """Check whether pytesseract + Tesseract binary are usable."""
    global _tesseract_available
    if _tesseract_available is None:
        try:
            import pytesseract
            pytesseract.get_tesseract_version()
            _tesseract_available = True
        except Exception:
            _tesseract_available = False
    return _tesseract_available


def set_active_pdf_mode(mode: str) -> None:
    """Set the PDF extraction mode for subsequent ingest calls."""
    global _active_pdf_mode
    if mode not in VALID_PDF_MODES:
        raise UserError(
            f"Invalid pdf_mode '{mode}'. "
            f"Valid options: {', '.join(VALID_PDF_MODES)}"
        )
    _active_pdf_mode = mode


def get_active_pdf_mode() -> str:
    """Return the currently active PDF extraction mode."""
    return _active_pdf_mode


def _clean_page_text(raw: str) -> str:
    """Light cleanup of extracted PDF text."""
    lines: list[str] = []
    for line in raw.splitlines():
        if _JUNK_LINE_RE.match(line):
            continue
        lines.append(line)

    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _split_markdown_sections(markdown: str) -> list[DocumentSection]:
    """Split Markdown output into sections by headings."""
    sections: list[DocumentSection] = []
    parts = _HEADING_RE.split(markdown)

    if parts[0].strip():
        sections.append(DocumentSection(
            title="Introduction",
            content=parts[0].strip(),
            level=0,
        ))

    i = 1
    while i + 2 <= len(parts):
        hashes = parts[i]
        title = parts[i + 1].strip()
        body = parts[i + 2].strip() if i + 2 < len(parts) else ""
        sections.append(DocumentSection(
            title=title,
            content=body,
            level=len(hashes),
        ))
        i += 3

    if not sections and markdown.strip():
        sections.append(DocumentSection(
            title="Full Document",
            content=markdown.strip(),
            level=0,
        ))

    return sections


class PdfIngester(BaseIngester):
    """PDF ingester with configurable extraction backends.

    The backend is selected at runtime from the module-level ``_active_pdf_mode``
    (set via :func:`set_active_pdf_mode` before calling :meth:`ingest`).
    """

    def supported_extensions(self) -> list[str]:
        return [".pdf"]

    def ingest(self, path: Path) -> Document:
        path = Path(path).resolve()

        if not path.is_file():
            raise FileAccessError(str(path), "file not found")

        mode = _active_pdf_mode
        if mode == "high_fidelity":
            return self._ingest_marker(path)
        elif mode == "max_accuracy":
            return self._ingest_chandra(path)
        else:
            return self._ingest_standard(path)

    # ------------------------------------------------------------------
    # Standard backend (PyMuPDF / pypdf)
    # ------------------------------------------------------------------
    def _ingest_standard(self, path: Path) -> Document:
        """Extract with PyMuPDF (primary) or pypdf (fallback)."""
        try:
            return self._ingest_pymupdf(path)
        except ImportError:
            logger.info("PyMuPDF not available, falling back to pypdf")
            return self._ingest_pypdf(path)

    def _ingest_pymupdf(self, path: Path) -> Document:
        import fitz  # PyMuPDF

        try:
            doc = fitz.open(str(path))
        except Exception as exc:
            raise FileAccessError(str(path), f"cannot read PDF: {exc}") from exc

        pages: list[DocumentSection] = []
        all_text_parts: list[str] = []
        ocr_pages = 0

        for i, page in enumerate(doc):
            try:
                raw = page.get_text("text") or ""
                text = _clean_page_text(raw)
            except Exception as exc:
                logger.warning("Failed to extract page %d of %s: %s", i + 1, path, exc)
                text = ""

            # OCR fallback: if embedded text is sparse, render page and OCR
            if len(text.replace(" ", "").replace("\n", "")) < _OCR_MIN_CHARS:
                ocr_text = self._ocr_page(page, i + 1, path)
                if ocr_text:
                    text = ocr_text
                    ocr_pages += 1

            meta: dict = {"page_number": i + 1}
            if ocr_pages and len(text.replace(" ", "").replace("\n", "")) >= _OCR_MIN_CHARS:
                meta["ocr"] = True

            pages.append(DocumentSection(
                title=f"Page {i + 1}",
                content=text,
                level=i + 1,
                metadata=meta,
            ))
            if text.strip():
                all_text_parts.append(text)

        content = "\n\n".join(all_text_parts)

        pdf_meta = self._extract_pdf_metadata(path, doc=doc)
        doc.close()

        title = pdf_meta.get("pdf_title", "") or path.stem.replace("_", " ").replace("-", " ").title()
        stat = path.stat()

        extra = {**pdf_meta, "pdf_mode": "standard"}
        if ocr_pages:
            extra["ocr_pages"] = str(ocr_pages)

        return Document(
            title=title,
            content=content,
            source=SourceMetadata(
                file_path=str(path),
                file_extension=".pdf",
                source_type="pdf",
                modified_at=datetime.fromtimestamp(stat.st_mtime),
                size_bytes=stat.st_size,
                extra=extra,
            ),
            language="",
            sections=pages,
            metadata={"page_count": len(pages), "ocr_pages": ocr_pages, **pdf_meta},
        )

    def _ingest_pypdf(self, path: Path) -> Document:
        try:
            from pypdf import PdfReader
        except ImportError:
            raise FileAccessError(
                str(path),
                "No PDF library found. Install pymupdf or pypdf: pip install pymupdf",
            )

        try:
            reader = PdfReader(str(path))
        except Exception as exc:
            raise FileAccessError(str(path), f"cannot read PDF: {exc}") from exc

        pages: list[DocumentSection] = []
        all_text_parts: list[str] = []

        for i, page in enumerate(reader.pages):
            try:
                raw = page.extract_text() or ""
                text = _clean_page_text(raw)
            except Exception as exc:
                logger.warning("Failed to extract page %d of %s: %s", i + 1, path, exc)
                text = ""

            pages.append(DocumentSection(
                title=f"Page {i + 1}",
                content=text,
                level=i + 1,
                metadata={"page_number": i + 1},
            ))
            if text.strip():
                all_text_parts.append(text)

        content = "\n\n".join(all_text_parts)

        pdf_meta: dict[str, str] = {}
        if reader.metadata:
            meta = reader.metadata
            for attr in ("title", "author", "subject", "creator"):
                val = getattr(meta, attr, None)
                if val:
                    pdf_meta[f"pdf_{attr}"] = val

        title = pdf_meta.get("pdf_title", "") or path.stem.replace("_", " ").replace("-", " ").title()
        stat = path.stat()

        return Document(
            title=title,
            content=content,
            source=SourceMetadata(
                file_path=str(path),
                file_extension=".pdf",
                source_type="pdf",
                modified_at=datetime.fromtimestamp(stat.st_mtime),
                size_bytes=stat.st_size,
                extra={**pdf_meta, "pdf_mode": "standard"},
            ),
            language="",
            sections=pages,
            metadata={"page_count": len(pages), **pdf_meta},
        )

    # ------------------------------------------------------------------
    # marker-pdf backend (high_fidelity)
    # ------------------------------------------------------------------
    def _ingest_marker(self, path: Path) -> Document:
        """High-fidelity extraction using marker-pdf."""
        try:
            from marker.converters.pdf import PdfConverter
            from marker.models import create_model_dict
            from marker.output import text_from_rendered
        except ImportError as exc:
            raise UserError(
                "marker-pdf is required for high_fidelity PDF mode but is not installed. "
                "Install with: pip install 'bigbrain[marker]'"
            ) from exc

        try:
            converter = PdfConverter(artifact_dict=create_model_dict())
            rendered = converter(str(path))
            markdown_text, _, images = text_from_rendered(rendered)
        except Exception as exc:
            raise FileAccessError(
                str(path), f"marker-pdf extraction failed: {exc}"
            ) from exc

        if not markdown_text or not markdown_text.strip():
            logger.warning("marker-pdf returned empty text for %s", path)
            markdown_text = ""

        sections = _split_markdown_sections(markdown_text)
        pdf_meta = self._extract_pdf_metadata(path)

        title = (
            pdf_meta.get("pdf_title", "")
            or path.stem.replace("_", " ").replace("-", " ").title()
        )

        stat = path.stat()
        image_count = len(images) if images else 0

        return Document(
            title=title,
            content=markdown_text,
            source=SourceMetadata(
                file_path=str(path),
                file_extension=".pdf",
                source_type="pdf",
                modified_at=datetime.fromtimestamp(stat.st_mtime),
                size_bytes=stat.st_size,
                extra={**pdf_meta, "pdf_mode": "high_fidelity"},
            ),
            language="",
            sections=sections,
            metadata={
                "page_count": len(sections) or 1,
                "image_count": image_count,
                "pdf_mode": "high_fidelity",
                **pdf_meta,
            },
        )

    # ------------------------------------------------------------------
    # chandra-ocr backend (max_accuracy)
    # ------------------------------------------------------------------
    def _ingest_chandra(self, path: Path) -> Document:
        """Maximum-accuracy extraction using chandra-ocr."""
        try:
            from chandra_ocr import process_pdf
        except ImportError as exc:
            raise UserError(
                "chandra-ocr is required for max_accuracy PDF mode but is not installed. "
                "Install with: pip install 'bigbrain[chandra]'"
            ) from exc

        try:
            results = process_pdf(str(path), output_format="markdown")
            if isinstance(results, list):
                markdown_text = "\n\n".join(
                    r if isinstance(r, str) else str(r) for r in results
                )
            else:
                markdown_text = str(results)
        except Exception as exc:
            raise FileAccessError(
                str(path), f"chandra-ocr extraction failed: {exc}"
            ) from exc

        if not markdown_text or not markdown_text.strip():
            logger.warning("chandra-ocr returned empty text for %s", path)
            markdown_text = ""

        sections = _split_markdown_sections(markdown_text)
        pdf_meta = self._extract_pdf_metadata(path)

        title = (
            pdf_meta.get("pdf_title", "")
            or path.stem.replace("_", " ").replace("-", " ").title()
        )

        stat = path.stat()

        return Document(
            title=title,
            content=markdown_text,
            source=SourceMetadata(
                file_path=str(path),
                file_extension=".pdf",
                source_type="pdf",
                modified_at=datetime.fromtimestamp(stat.st_mtime),
                size_bytes=stat.st_size,
                extra={**pdf_meta, "pdf_mode": "max_accuracy"},
            ),
            language="",
            sections=sections,
            metadata={
                "section_count": len(sections),
                "pdf_mode": "max_accuracy",
                **pdf_meta,
            },
        )

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _ocr_page(page: object, page_num: int, path: Path) -> str:
        """Render a PyMuPDF page to image and run Tesseract OCR.

        Returns the OCR text, or empty string if Tesseract is unavailable.
        """
        if not _is_tesseract_available():
            return ""

        try:
            import pytesseract
            from PIL import Image

            # Render at 300 DPI for good OCR quality
            pix = page.get_pixmap(dpi=300)  # type: ignore[union-attr]
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(img)
            text = _clean_page_text(text)
            if text:
                logger.debug("OCR recovered %d chars on page %d of %s", len(text), page_num, path)
            return text
        except Exception as exc:
            logger.warning("OCR failed on page %d of %s: %s", page_num, path, exc)
            return ""

    @staticmethod
    def _extract_pdf_metadata(path: Path, *, doc: object | None = None) -> dict[str, str]:
        """Extract PDF metadata using PyMuPDF if available.

        If a fitz Document ``doc`` is already open, use it directly.
        Otherwise open and close one.
        """
        pdf_meta: dict[str, str] = {}
        try:
            import fitz
            should_close = doc is None
            if doc is None:
                doc = fitz.open(str(path))
            meta = doc.metadata or {}  # type: ignore[union-attr]
            for key in ("title", "author", "subject", "creator"):
                val = meta.get(key, "")
                if val:
                    pdf_meta[f"pdf_{key}"] = val
            if should_close:
                doc.close()  # type: ignore[union-attr]
        except Exception:
            pass
        return pdf_meta
