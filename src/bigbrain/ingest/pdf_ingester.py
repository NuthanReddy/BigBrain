"""PDF file ingester with configurable backends.

Supports two extraction modes controlled by ``pdf_mode`` in config or CLI:

- ``standard`` – PyMuPDF text extraction with image-aware OCR.  Pages are
  classified as scanned, digital-with-figures, or pure-text.  Scanned pages
  get full-page OCR; figures in digital pages are individually extracted and
  OCR'd for axis labels, legends, and diagram text.
- ``max_accuracy`` – chandra-ocr.  Highest benchmark scores for math/tables.
  Requires ``pip install 'bigbrain[chandra]'``.
"""

from __future__ import annotations

import hashlib
import io
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from bigbrain.ingest.registry import BaseIngester
from bigbrain.kb.models import Document, DocumentSection, SourceMetadata
from bigbrain.errors import FileAccessError, UserError
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)

VALID_PDF_MODES = ("standard", "max_accuracy")

# Heuristic: lines made mostly of non-alphanumeric chars are likely
# figure debris (card suits, box-drawing, stray symbols).
_JUNK_LINE_RE = re.compile(r"^[\s\W]{4,}$")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

# Pages with fewer than this many non-whitespace chars are "sparse"
_OCR_MIN_CHARS = 20
# Images covering ≥5% of the page are "significant" (same as pymupdf4llm)
_IMG_MIN_COVERAGE = 0.05
# Scanned pages: images cover ≥50% and text is sparse
_SCANNED_IMG_COVERAGE = 0.50
# Minimum image dimensions (pixels) to bother OCR'ing
_IMG_MIN_OCR_SIZE = 100
# Maximum images to process per page (avoid pathological cases)
_MAX_IMAGES_PER_PAGE = 30
# Caption search distance in points below image
_CAPTION_SEARCH_DISTANCE = 40

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


def _classify_page(page: object, text: str) -> tuple[str, list[dict]]:
    """Classify a PDF page based on text content and embedded images.

    Returns
    -------
    tuple[str, list[dict]]
        (page_type, significant_images) where page_type is one of:
        - ``"scanned"`` — images dominate, text is sparse → full-page OCR
        - ``"digital_with_images"`` — text present + significant figures
        - ``"text_only"`` — enough text, no significant images
        - ``"blank"`` — no text, no images
    """
    text_chars = len(text.replace(" ", "").replace("\n", ""))

    try:
        page_rect = page.rect  # type: ignore[union-attr]
        page_area = page_rect.width * page_rect.height
    except Exception:
        page_area = 0

    if page_area <= 0:
        return ("text_only" if text_chars >= _OCR_MIN_CHARS else "blank", [])

    # Get image metadata with bounding boxes
    try:
        image_info_list = page.get_image_info()  # type: ignore[union-attr]
    except Exception:
        image_info_list = []

    # Filter to significant images (≥5% page area, capped at 30)
    significant: list[dict] = []
    total_image_area = 0.0
    for info in image_info_list:
        bbox = info.get("bbox", None)
        if bbox is None:
            continue
        try:
            if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
                w = abs(bbox[2] - bbox[0])
                h = abs(bbox[3] - bbox[1])
            else:
                w = abs(bbox.width)
                h = abs(bbox.height)
        except Exception:
            continue

        area = w * h
        if area <= 0:
            continue
        total_image_area += area

        if area / page_area >= _IMG_MIN_COVERAGE:
            significant.append(info)
            if len(significant) >= _MAX_IMAGES_PER_PAGE:
                break

    image_coverage = total_image_area / page_area

    if text_chars < _OCR_MIN_CHARS and image_coverage >= _SCANNED_IMG_COVERAGE:
        return ("scanned", [])
    elif text_chars < _OCR_MIN_CHARS and not significant:
        return ("blank", [])
    elif text_chars >= _OCR_MIN_CHARS and significant:
        return ("digital_with_images", significant)
    elif text_chars < _OCR_MIN_CHARS and significant:
        # Sparse text but has a few figures — treat as scanned
        return ("scanned", [])
    else:
        return ("text_only", [])


def _find_caption(page: object, image_bbox: Any) -> str:
    """Find caption text immediately below an image bounding box.

    Looks for text blocks within ``_CAPTION_SEARCH_DISTANCE`` points below
    the image that are horizontally aligned.  Returns the first match or
    empty string.
    """
    try:
        blocks = page.get_text("blocks")  # type: ignore[union-attr]
    except Exception:
        return ""

    if isinstance(image_bbox, (list, tuple)) and len(image_bbox) >= 4:
        img_x0, img_y0, img_x1, img_y1 = image_bbox[0], image_bbox[1], image_bbox[2], image_bbox[3]
    else:
        try:
            img_x0, img_y0, img_x1, img_y1 = image_bbox.x0, image_bbox.y0, image_bbox.x1, image_bbox.y1
        except Exception:
            return ""

    img_width = abs(img_x1 - img_x0)

    for block in blocks:
        if not isinstance(block, (list, tuple)) or len(block) < 6:
            continue
        # block[-1] == 0 means text block
        if block[-1] != 0:
            continue

        bx0, by0, bx1, by1 = block[0], block[1], block[2], block[3]
        text = block[4] if len(block) > 4 else ""

        # Must be below the image, within search distance
        gap = by0 - img_y1
        if gap < 0 or gap > _CAPTION_SEARCH_DISTANCE:
            continue

        # Must be horizontally overlapping with the image
        if bx1 < img_x0 - 20 or bx0 > img_x1 + 20:
            continue

        text = str(text).strip()
        if text:
            # Truncate long text to first line (captions are short)
            first_line = text.split("\n")[0].strip()
            if len(first_line) > 200:
                first_line = first_line[:200] + "..."
            return first_line

    return ""


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
        if mode == "max_accuracy":
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
        ocr_page_count = 0
        total_images_found = 0
        total_images_ocrd = 0

        for i, page in enumerate(doc):
            try:
                raw = page.get_text("text") or ""
                text = _clean_page_text(raw)
            except Exception as exc:
                logger.warning("Failed to extract page %d of %s: %s", i + 1, path, exc)
                text = ""

            page_type, sig_images = _classify_page(page, text)
            meta: dict[str, Any] = {"page_number": i + 1, "page_type": page_type}

            if page_type == "scanned":
                # Full-page OCR for scanned pages
                ocr_text = self._ocr_page(page, i + 1, path)
                if ocr_text:
                    text = ocr_text
                    ocr_page_count += 1
                    meta["ocr"] = True

            elif page_type == "digital_with_images":
                # Extract and OCR individual figures
                image_results = self._extract_and_ocr_images(
                    doc, page, sig_images, i + 1, path,
                )
                total_images_found += len(sig_images)
                if image_results:
                    img_text_parts: list[str] = []
                    img_meta_list: list[dict] = []
                    for img_info in image_results:
                        if img_info.get("ocr_text"):
                            total_images_ocrd += 1
                            caption = img_info.get("caption", "")
                            label = caption or f"Figure on page {i + 1}"
                            img_text_parts.append(
                                f"\n[{label}]: {img_info['ocr_text']}"
                            )
                        img_meta_list.append(img_info)
                    if img_text_parts:
                        text = text + "\n" + "\n".join(img_text_parts)
                    meta["images"] = img_meta_list

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

        extra: dict[str, Any] = {**pdf_meta, "pdf_mode": "standard"}
        if ocr_page_count:
            extra["ocr_pages"] = str(ocr_page_count)
        if total_images_found:
            extra["images_found"] = str(total_images_found)
            extra["images_ocrd"] = str(total_images_ocrd)

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
            metadata={
                "page_count": len(pages),
                "ocr_pages": ocr_page_count,
                "images_found": total_images_found,
                "images_ocrd": total_images_ocrd,
                **pdf_meta,
            },
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
    def _extract_and_ocr_images(
        doc: object,
        page: object,
        sig_images: list[dict],
        page_num: int,
        path: Path,
    ) -> list[dict[str, Any]]:
        """Extract significant images from a page and OCR them.

        Returns a list of dicts with keys: xref, width, height,
        page_coverage, caption, ocr_text, saved_path (if saved).
        """
        if not _is_tesseract_available():
            # Still collect image metadata even without OCR
            results: list[dict[str, Any]] = []
            for info in sig_images:
                results.append({
                    "width": info.get("width", 0),
                    "height": info.get("height", 0),
                    "xref": info.get("xref", 0),
                })
            return results

        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            return []

        results = []
        for info in sig_images:
            xref = info.get("xref", 0)
            if not xref:
                continue

            entry: dict[str, Any] = {
                "xref": xref,
                "width": info.get("width", 0),
                "height": info.get("height", 0),
            }

            # Try caption extraction
            bbox = info.get("bbox")
            if bbox:
                caption = _find_caption(page, bbox)
                if caption:
                    entry["caption"] = caption

            # Extract and OCR the image
            try:
                img_data = doc.extract_image(xref)  # type: ignore[union-attr]
                img_bytes = img_data["image"]
                img = Image.open(io.BytesIO(img_bytes))

                # Only OCR images large enough to contain readable text
                if img.width >= _IMG_MIN_OCR_SIZE and img.height >= _IMG_MIN_OCR_SIZE:
                    ocr_text = pytesseract.image_to_string(img).strip()
                    ocr_text = _clean_page_text(ocr_text)
                    if ocr_text and len(ocr_text) > 5:
                        entry["ocr_text"] = ocr_text
                        logger.debug(
                            "OCR extracted %d chars from image xref=%d on page %d of %s",
                            len(ocr_text), xref, page_num, path,
                        )

                # Save image to data/images/<doc_hash>/
                try:
                    doc_hash = hashlib.md5(str(path).encode()).hexdigest()[:12]
                    img_dir = Path("data") / "images" / doc_hash
                    img_dir.mkdir(parents=True, exist_ok=True)
                    ext = img_data.get("ext", "png")
                    img_path = img_dir / f"page{page_num}_img{xref}.{ext}"
                    img_path.write_bytes(img_bytes)
                    entry["saved_path"] = str(img_path)
                except Exception as exc:
                    logger.debug("Failed to save image xref=%d: %s", xref, exc)

            except Exception as exc:
                logger.debug(
                    "Failed to extract/OCR image xref=%d on page %d: %s",
                    xref, page_num, exc,
                )

            results.append(entry)

        return results

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
