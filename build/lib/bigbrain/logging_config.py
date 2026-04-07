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

import logging
import sys

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
# Public API
# ---------------------------------------------------------------------------


def setup_logging(level: str = "INFO", log_format: str = "console") -> None:
    """Configure the root logger for the application.

    This function is **idempotent** – calling it more than once is a no-op
    after the first invocation so that importers / test harnesses cannot
    accidentally reconfigure logging mid-run.

    Parameters
    ----------
    level:
        One of DEBUG, INFO, WARNING, ERROR, CRITICAL (case-insensitive).
    log_format:
        The output format to use.  Currently only ``"console"`` is
        supported.

        .. note::

            **Extension point – file logging**: A ``"file"`` format option
            could be added here to attach a ``logging.FileHandler`` that
            writes to a configurable path.

        .. note::

            **Extension point – structured / JSON logging**: A ``"json"``
            format option could be added here to emit structured log
            records (e.g. using ``logging.Formatter`` subclass that
            serialises to JSON).
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
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)

    formatter = logging.Formatter(fmt=_DEFAULT_FORMAT, datefmt=_DEFAULT_DATE_FORMAT)
    handler.setFormatter(formatter)

    root_logger.addHandler(handler)

    _logging_configured = True


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
