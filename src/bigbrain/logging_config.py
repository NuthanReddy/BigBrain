"""Centralized logging configuration for BigBrain.

Usage in any module::

    from bigbrain.logging_config import get_logger
    logger = get_logger(__name__)

    logger.info("Processing %s", item)

Setup (call exactly once at CLI startup)::

    from bigbrain.logging_config import setup_logging
    setup_logging(level="INFO")

``UserError`` is the base exception for user-facing errors (bad input,
missing config, unsupported operations).  The CLI layer should catch
``UserError`` and display its message *without* a stack trace.  Internal
or unexpected errors should show stack traces only when the log level is
set to DEBUG.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

__all__ = ["setup_logging", "get_logger", "UserError"]

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_DEFAULT_FORMAT = "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
_DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_VALID_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})

# Sentinel so we know whether setup_logging has already run.
_logging_configured: bool = False


# ---------------------------------------------------------------------------
# JSON formatter
# ---------------------------------------------------------------------------


class JsonFormatter(logging.Formatter):
    """Structured JSON log formatter."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def setup_logging(
    level: str = "INFO",
    log_format: str = "console",
    log_file: str = "",
    quiet: bool = False,
) -> None:
    """Configure the root logger for the application.

    This function is **idempotent** – calling it more than once is a no-op
    after the first invocation so that importers / test harnesses cannot
    accidentally reconfigure logging mid-run.

    Parameters
    ----------
    level:
        One of DEBUG, INFO, WARNING, ERROR, CRITICAL (case-insensitive).
    log_format:
        ``"console"`` for human-readable output or ``"json"`` for
        structured JSON records.
    log_file:
        Path to a log file.  When non-empty a ``FileHandler`` is added
        (parent directories are created automatically).
    quiet:
        If ``True``, suppress console output (useful for scripts).
    """
    global _logging_configured  # noqa: PLW0603

    if _logging_configured:
        return

    level = level.upper()
    if level not in _VALID_LEVELS:
        raise ValueError(
            f"Invalid log level {level!r}. "
            f"Choose from: {', '.join(sorted(_VALID_LEVELS))}"
        )

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Console handler ---------------------------------------------------------
    if not quiet:
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(level)

        if log_format == "json":
            handler.setFormatter(JsonFormatter())
        else:
            handler.setFormatter(
                logging.Formatter(fmt=_DEFAULT_FORMAT, datefmt=_DEFAULT_DATE_FORMAT)
            )

        root_logger.addHandler(handler)

    # File handler ------------------------------------------------------------
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(str(log_path), encoding="utf-8")
        file_handler.setLevel(level)

        if log_format == "json":
            file_handler.setFormatter(JsonFormatter())
        else:
            file_handler.setFormatter(
                logging.Formatter(fmt=_DEFAULT_FORMAT, datefmt=_DEFAULT_DATE_FORMAT)
            )

        root_logger.addHandler(file_handler)

    _logging_configured = True


def reset_logging() -> None:
    """Reset logging configuration (for tests)."""
    global _logging_configured  # noqa: PLW0603
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)
    _logging_configured = False


def get_logger(name: str) -> logging.Logger:
    """Return a logger for *name*.

    The canonical pattern for every module is::

        from bigbrain.logging_config import get_logger
        logger = get_logger(__name__)
    """
    return logging.getLogger(name)


# ---------------------------------------------------------------------------
# Error-handling helpers
# ---------------------------------------------------------------------------


# Re-export UserError for backward compatibility.
# The canonical location is now bigbrain.errors.
from bigbrain.errors import UserError  # noqa: F401
