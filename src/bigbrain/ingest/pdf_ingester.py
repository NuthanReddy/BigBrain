"""PDF file ingester with PyMuPDF (primary) and pypdf (fallback).

PyMuPDF provides superior text extraction, especially for complex layouts
with math, pseudocode, and multi-column content.  pypdf is used as a
fallback when PyMuPDF is not installed.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from bigbrain.ingest.registry import BaseIngester
from bigbrain.kb.models import Document, DocumentSection, SourceMetadata
from bigbrain.errors import FileAccessError
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)

# Heuristic: lines made mostly of non-alphanumeric chars are likely
# figure debris (card suits, box-drawing, stray symbols).
_JUNK_LINE_RE = re.compile(r"^[\s\W]{4,}$")


def _clean_page_text(raw: str) -> str:
    """Light cleanup of extracted PDF text."""
    lines: list[str] = []
    for line in raw.splitlines():
        # Drop lines that are pure symbol noise (figure remnants)
        if _JUNK_LINE_RE.match(line):
            continue
        lines.append(line)

    text = "\n".join(lines)
    # Collapse 3+ consecutive blank lines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


class PdfIngester(BaseIngester):
    """Ingests machine-readable PDF files, preserving page boundaries."""

    def supported_extensions(self) -> list[str]:
        return [".pdf"]

    def ingest(self, path: Path) -> Document:
        path = Path(path).resolve()

        if not path.is_file():
            raise FileAccessError(str(path), "file not found")

        # Try PyMuPDF first (better quality), fall back to pypdf
        try:
            return self._ingest_pymupdf(path)
        except ImportError:
            logger.info("PyMuPDF not available, falling back to pypdf")
            return self._ingest_pypdf(path)

    # ------------------------------------------------------------------
    # PyMuPDF backend
    # ------------------------------------------------------------------
    def _ingest_pymupdf(self, path: Path) -> Document:
        import fitz  # PyMuPDF

        try:
            doc = fitz.open(str(path))
        except Exception as exc:
            raise FileAccessError(str(path), f"cannot read PDF: {exc}") from exc

        pages: list[DocumentSection] = []
        all_text_parts: list[str] = []

        for i, page in enumerate(doc):
            try:
                raw = page.get_text("text") or ""
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

        # Metadata
        pdf_meta: dict[str, str] = {}
        meta = doc.metadata or {}
        for key in ("title", "author", "subject", "creator"):
            val = meta.get(key, "")
            if val:
                pdf_meta[f"pdf_{key}"] = val

        doc.close()

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
                extra=pdf_meta,
            ),
            language="",
            sections=pages,
            metadata={"page_count": len(pages), **pdf_meta},
        )

    # ------------------------------------------------------------------
    # pypdf fallback backend
    # ------------------------------------------------------------------
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
                extra=pdf_meta,
            ),
            language="",
            sections=pages,
            metadata={"page_count": len(pages), **pdf_meta},
        )
