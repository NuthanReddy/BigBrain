"""Ingester registry – maps file extensions to ingester implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from bigbrain.logging_config import get_logger

if TYPE_CHECKING:
    from bigbrain.kb.models import Document

logger = get_logger(__name__)


class BaseIngester(ABC):
    """Abstract base for all file ingesters."""
    
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Return list of extensions this ingester handles (e.g., ['.txt'])."""
        ...
    
    @abstractmethod
    def ingest(self, path: Path) -> Document:
        """Ingest a single file and return a Document."""
        ...


# Global registry
_registry: dict[str, BaseIngester] = {}


def register_ingester(ingester: BaseIngester) -> None:
    """Register an ingester for its supported extensions."""
    for ext in ingester.supported_extensions():
        ext = ext.lower()
        _registry[ext] = ingester
        logger.debug("Registered ingester for '%s': %s", ext, type(ingester).__name__)


def get_ingester(extension: str) -> BaseIngester | None:
    """Look up the ingester for a given file extension."""
    return _registry.get(extension.lower())


def get_registered_extensions() -> list[str]:
    """Return all registered extensions."""
    return sorted(_registry.keys())


def _init_default_ingesters() -> None:
    """Register all built-in ingesters. Called once at import time."""
    from bigbrain.ingest.text_ingester import TextIngester
    from bigbrain.ingest.markdown_ingester import MarkdownIngester
    from bigbrain.ingest.pdf_ingester import PdfIngester
    from bigbrain.ingest.python_ingester import PythonIngester
    
    register_ingester(TextIngester())
    register_ingester(MarkdownIngester())
    register_ingester(PdfIngester())
    register_ingester(PythonIngester())
