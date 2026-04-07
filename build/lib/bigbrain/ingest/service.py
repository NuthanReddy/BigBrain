"""Ingestion service – orchestrates discovery, dispatch, and result aggregation."""

from __future__ import annotations

from pathlib import Path

from bigbrain.ingest.discovery import discover_files
from bigbrain.ingest.registry import get_ingester, _init_default_ingesters
from bigbrain.kb.models import IngestionResult
from bigbrain.logging_config import get_logger
from bigbrain.config import load_config, IngestionConfig

logger = get_logger(__name__)

# Ensure ingesters are registered on first import
_init_default_ingesters()


def ingest_path(
    path: str | Path,
    *,
    recursive: bool | None = None,
    file_type: str = "auto",
    skip_hidden: bool | None = None,
    config: IngestionConfig | None = None,
) -> IngestionResult:
    """Ingest a file or directory, returning an IngestionResult.
    
    Parameters
    ----------
    path : file or directory to ingest
    recursive : override config recursive setting
    file_type : force a specific type ("txt", "md", "pdf", "py") or "auto"
    skip_hidden : override config skip_hidden setting
    config : ingestion config; loaded from default if None
    """
    if config is None:
        cfg = load_config()
        config = cfg.ingestion
    
    rec = recursive if recursive is not None else config.recursive
    hidden = skip_hidden if skip_hidden is not None else config.skip_hidden
    
    # Discover files
    discovery = discover_files(
        path,
        supported_extensions=config.supported_extensions,
        recursive=rec,
        skip_hidden=hidden,
        max_file_size_mb=config.max_file_size_mb,
    )
    
    result = IngestionResult()
    result.warnings.extend(discovery.skipped)
    result.skipped = len(discovery.skipped)
    
    # Process each discovered file
    for file_path in discovery.files:
        ext = file_path.suffix.lower()
        
        # If type forced, skip files that don't match
        if file_type != "auto":
            forced_ext = f".{file_type}" if not file_type.startswith(".") else file_type
            if ext != forced_ext:
                result.skipped += 1
                result.warnings.append(f"skipped (type filter): {file_path}")
                continue
        
        ingester = get_ingester(ext)
        if ingester is None:
            result.skipped += 1
            result.warnings.append(f"no ingester for '{ext}': {file_path}")
            continue
        
        try:
            doc = ingester.ingest(file_path)
            result.documents.append(doc)
            result.processed += 1
            logger.info("Ingested: %s", file_path)
        except Exception as exc:
            result.failed += 1
            result.errors.append(f"{file_path}: {exc}")
            logger.error("Failed to ingest %s: %s", file_path, exc)
    
    return result
