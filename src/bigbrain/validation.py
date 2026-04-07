"""Input validation and safety helpers."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

from bigbrain.errors import UserError
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)

_MAX_URL_LENGTH = 2048
_MAX_PATH_LENGTH = 4096
_MAX_API_RESPONSE_MB = 50


def validate_url(url: str) -> str:
    """Validate and normalize a URL. Returns the URL or raises UserError."""
    if not url or not url.strip():
        raise UserError("URL cannot be empty")

    url = url.strip()

    if len(url) > _MAX_URL_LENGTH:
        raise UserError(f"URL too long ({len(url)} chars, max {_MAX_URL_LENGTH})")

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise UserError(f"Invalid URL scheme: '{parsed.scheme}'. Only http/https are supported.")
    if not parsed.netloc:
        raise UserError(f"Invalid URL: missing host/domain")

    return url


def validate_path(path: str) -> Path:
    """Validate a file/directory path. Returns resolved Path or raises UserError."""
    if not path or not path.strip():
        raise UserError("Path cannot be empty")

    if len(path) > _MAX_PATH_LENGTH:
        raise UserError(f"Path too long ({len(path)} chars)")

    resolved = Path(path).resolve()

    # Basic path traversal check
    try:
        resolved.relative_to(Path.cwd())
    except ValueError:
        # Allow absolute paths, but warn about paths outside cwd
        pass

    return resolved


def validate_notion_page_id(page_id: str) -> str:
    """Validate a Notion page ID format."""
    if not page_id or not page_id.strip():
        raise UserError("Notion page ID cannot be empty")

    # Notion IDs are UUIDs (with or without dashes)
    clean = page_id.strip().replace("-", "")
    if not re.match(r"^[a-f0-9]{32}$", clean):
        raise UserError(f"Invalid Notion page ID format: '{page_id}'. Expected a UUID.")

    return page_id.strip()


def validate_doc_id(doc_id: str) -> str:
    """Validate a document ID."""
    if not doc_id or not doc_id.strip():
        raise UserError("Document ID cannot be empty")

    clean = doc_id.strip()
    if not re.match(r"^[a-f0-9]+$", clean):
        raise UserError(f"Invalid document ID: '{doc_id}'. Expected a hex string.")

    return clean


def sanitize_text(text: str, max_length: int = 100000) -> str:
    """Sanitize text content: trim, enforce max length."""
    if not text:
        return ""

    text = text.strip()
    if len(text) > max_length:
        logger.warning("Text truncated from %d to %d chars", len(text), max_length)
        text = text[:max_length]

    return text


def validate_model_name(model: str) -> str:
    """Validate an AI model name."""
    if not model:
        return ""

    model = model.strip()
    if len(model) > 200:
        raise UserError(f"Model name too long ({len(model)} chars)")

    # Allow alphanumeric, dots, dashes, underscores, slashes, colons
    if not re.match(r"^[\w.\-/:]+$", model):
        raise UserError(f"Invalid model name: '{model}'")

    return model
