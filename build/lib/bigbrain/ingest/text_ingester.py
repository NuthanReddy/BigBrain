"""TXT file ingester."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from bigbrain.ingest.registry import BaseIngester
from bigbrain.kb.models import Document, SourceMetadata
from bigbrain.errors import FileAccessError
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


class TextIngester(BaseIngester):
    """Ingests plain text (.txt) files into Document objects."""

    def supported_extensions(self) -> list[str]:
        return [".txt"]

    def ingest(self, path: Path) -> Document:
        path = Path(path).resolve()

        if not path.is_file():
            raise FileAccessError(str(path), "file not found")

        # Read with UTF-8 first, fallback to latin-1
        content = self._read_file(path)

        # Infer title from filename
        title = path.stem.replace("_", " ").replace("-", " ").title()

        # Get file stats
        stat = path.stat()

        source = SourceMetadata(
            file_path=str(path),
            file_extension=".txt",
            source_type="txt",
            modified_at=datetime.fromtimestamp(stat.st_mtime),
            size_bytes=stat.st_size,
        )

        return Document(
            title=title,
            content=content,
            source=source,
            language="",
            metadata={"line_count": content.count("\n") + 1 if content else 0},
        )

    def _read_file(self, path: Path) -> str:
        """Read file with UTF-8, falling back to latin-1."""
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
