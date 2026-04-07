"""File discovery and filtering for the ingestion pipeline."""

from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass, field

from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class DiscoveryResult:
    """Result of file discovery."""
    files: list[Path] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)  # reasons
    

def discover_files(
    path: str | Path,
    *,
    supported_extensions: list[str] | None = None,
    recursive: bool = True,
    skip_hidden: bool = True,
    max_file_size_mb: int = 50,
) -> DiscoveryResult:
    """Discover files eligible for ingestion.
    
    - If path is a file, validate and return it.
    - If path is a directory, walk it (optionally recursively).
    - Filter by extension, hidden status, and size.
    """
    if supported_extensions is None:
        supported_extensions = [".txt", ".md", ".pdf", ".py"]
    
    target = Path(path).resolve()
    result = DiscoveryResult()
    max_bytes = max_file_size_mb * 1024 * 1024
    
    if not target.exists():
        from bigbrain.errors import FileAccessError
        raise FileAccessError(str(target), "path does not exist")
    
    if target.is_file():
        _check_file(target, supported_extensions, skip_hidden, max_bytes, result)
        return result
    
    if target.is_dir():
        walker = target.rglob("*") if recursive else target.iterdir()
        for item in sorted(walker):
            if item.is_file():
                _check_file(item, supported_extensions, skip_hidden, max_bytes, result)
        return result
    
    from bigbrain.errors import FileAccessError
    raise FileAccessError(str(target), "not a file or directory")


def _check_file(
    path: Path,
    supported_extensions: list[str],
    skip_hidden: bool,
    max_bytes: int,
    result: DiscoveryResult,
) -> None:
    """Validate a single file and add to result or skip list."""
    # Hidden file check
    if skip_hidden and any(part.startswith(".") for part in path.parts):
        reason = f"hidden: {path}"
        result.skipped.append(reason)
        logger.debug("Skipping %s", reason)
        return
    
    # Extension check
    ext = path.suffix.lower()
    if ext not in supported_extensions:
        reason = f"unsupported extension '{ext}': {path}"
        result.skipped.append(reason)
        logger.debug("Skipping %s", reason)
        return
    
    # Size check
    try:
        size = path.stat().st_size
    except OSError as e:
        reason = f"cannot stat: {path} ({e})"
        result.skipped.append(reason)
        logger.warning("Skipping %s", reason)
        return
    
    if size > max_bytes:
        reason = f"too large ({size} bytes): {path}"
        result.skipped.append(reason)
        logger.warning("Skipping %s", reason)
        return
    
    result.files.append(path)
