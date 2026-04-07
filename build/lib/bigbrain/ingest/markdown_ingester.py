"""Markdown file ingester with heading structure preservation."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from bigbrain.ingest.registry import BaseIngester
from bigbrain.kb.models import Document, DocumentSection, SourceMetadata
from bigbrain.errors import FileAccessError
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)

# Regex for ATX headings: # Heading, ## Heading, etc.
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)(?:\s+#*)?$", re.MULTILINE)
# Regex for Markdown links: [text](url)
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


class MarkdownIngester(BaseIngester):
    """Ingests Markdown (.md) files preserving heading structure."""

    def supported_extensions(self) -> list[str]:
        return [".md"]

    def ingest(self, path: Path) -> Document:
        path = Path(path).resolve()

        if not path.is_file():
            raise FileAccessError(str(path), "file not found")

        content = self._read_file(path)
        stat = path.stat()

        # Extract sections from headings
        sections = self._extract_sections(content)

        # Infer title: first H1, or first heading, or filename
        title = self._infer_title(content, sections, path)

        # Extract links for metadata
        links = _LINK_RE.findall(content)
        internal_links = [
            {"text": text, "href": href}
            for text, href in links
            if not href.startswith(("http://", "https://", "mailto:"))
        ]

        source = SourceMetadata(
            file_path=str(path),
            file_extension=".md",
            source_type="md",
            modified_at=datetime.fromtimestamp(stat.st_mtime),
            size_bytes=stat.st_size,
        )

        return Document(
            title=title,
            content=content,
            source=source,
            language="markdown",
            sections=sections,
            metadata={
                "heading_count": len(sections),
                "link_count": len(links),
                "internal_links": internal_links,
                "line_count": content.count("\n") + 1 if content else 0,
            },
        )

    def _extract_sections(self, content: str) -> list[DocumentSection]:
        """Parse ATX headings into DocumentSection list."""
        sections: list[DocumentSection] = []
        lines = content.split("\n")
        current_title = ""
        current_level = 0
        current_lines: list[str] = []

        for line in lines:
            match = _HEADING_RE.match(line)
            if match:
                # Save previous section if any
                if current_title or current_lines:
                    sections.append(DocumentSection(
                        title=current_title,
                        content="\n".join(current_lines).strip(),
                        level=current_level,
                    ))
                current_level = len(match.group(1))
                current_title = match.group(2).strip()
                current_lines = []
            else:
                current_lines.append(line)

        # Don't forget the last section
        if current_title or current_lines:
            sections.append(DocumentSection(
                title=current_title,
                content="\n".join(current_lines).strip(),
                level=current_level,
            ))

        return sections

    def _infer_title(
        self,
        content: str,
        sections: list[DocumentSection],
        path: Path,
    ) -> str:
        """Infer title from first H1, first heading, or filename."""
        # Look for first H1
        for section in sections:
            if section.level == 1 and section.title:
                return section.title
        # Fall back to first heading of any level
        for section in sections:
            if section.title:
                return section.title
        # Fall back to filename
        return path.stem.replace("_", " ").replace("-", " ").title()

    def _read_file(self, path: Path) -> str:
        """Read with UTF-8, fallback to latin-1."""
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            logger.warning("UTF-8 decode failed for %s, trying latin-1", path)
            try:
                return path.read_text(encoding="latin-1")
            except Exception as exc:
                raise FileAccessError(str(path), f"encoding error: {exc}") from exc
        except OSError as exc:
            raise FileAccessError(str(path), str(exc)) from exc
