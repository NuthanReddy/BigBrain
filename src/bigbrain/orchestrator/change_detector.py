"""File change detection for incremental processing."""

from __future__ import annotations

import hashlib
import sys
from dataclasses import dataclass, field
from pathlib import Path

from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class ChangeResult:
    """Result of a change detection scan."""

    new_files: list[Path] = field(default_factory=list)
    modified_files: list[Path] = field(default_factory=list)
    deleted_paths: list[str] = field(default_factory=list)
    unchanged_files: list[Path] = field(default_factory=list)

    @property
    def has_changes(self) -> bool:
        return bool(self.new_files or self.modified_files or self.deleted_paths)

    @property
    def changed_files(self) -> list[Path]:
        return self.new_files + self.modified_files


class ChangeDetector:
    """Detects file changes by comparing mtime and content hash against stored records.

    Uses a two-tier strategy: mtime is checked first as a fast hint, then
    a full SHA-256 content hash is compared only when mtime differs.  This
    avoids expensive I/O on unchanged files while still catching every real
    modification.
    """

    DEFAULT_EXTENSIONS = [".txt", ".md", ".pdf", ".py"]

    def __init__(self, store: KBStore) -> None:
        self._store = store

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def scan(
        self,
        paths: list[Path],
        *,
        supported_extensions: list[str] | None = None,
    ) -> ChangeResult:
        """Scan *paths* and classify each file against the KB.

        Only files present in *paths* are classified (new / modified /
        unchanged).  A file recorded in the KB but **not** present in
        *paths* is reported as deleted — so callers should pass a complete
        discovery snapshot for accurate deletion detection.
        """
        if supported_extensions is None:
            supported_extensions = self.DEFAULT_EXTENSIONS

        result = ChangeResult()
        stored_hashes = self._store.get_file_hashes()
        seen_keys: set[str] = set()

        for path in paths:
            if not path.is_file():
                continue
            if path.suffix.lower() not in supported_extensions:
                continue

            key = self._normalize_path(path)
            seen_keys.add(key)

            stored = stored_hashes.get(key)
            if stored is None:
                result.new_files.append(path)
                logger.debug("New file: %s", path)
                continue

            current_mtime = path.stat().st_mtime
            if current_mtime != stored["mtime"]:
                # mtime differs — verify with content hash
                current_hash = self.file_hash(path)
                if current_hash != stored["content_hash"]:
                    result.modified_files.append(path)
                    logger.debug("Modified: %s", path)
                else:
                    result.unchanged_files.append(path)
            else:
                result.unchanged_files.append(path)

        # Detect deletions: stored paths absent from the scan
        for stored_path in stored_hashes:
            if stored_path not in seen_keys:
                result.deleted_paths.append(stored_path)
                logger.debug("Deleted: %s", stored_path)

        return result

    def save_file_record(self, path: Path, document_id: str = "") -> None:
        """Persist the current mtime and content hash for *path*."""
        key = self._normalize_path(path)
        mtime = path.stat().st_mtime
        content_hash = self.file_hash(path)
        self._store.save_file_hash(key, mtime, content_hash, document_id)

    def remove_file_record(self, file_path: str) -> bool:
        """Remove the stored hash record for a deleted file."""
        return self._store.delete_file_hash(file_path)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def file_hash(path: Path) -> str:
        """Compute the full SHA-256 hex digest of *path*'s contents."""
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    @staticmethod
    def _normalize_path(path: Path) -> str:
        """Canonical absolute path string, case-folded on Windows."""
        resolved = str(path.resolve())
        if sys.platform == "win32":
            resolved = resolved.lower()
        return resolved
