"""Plugin base classes for BigBrain extensibility."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from bigbrain.kb.models import Document
from bigbrain.compile.models import CompileOutput


@dataclass
class PluginInfo:
    """Metadata about a plugin."""
    name: str
    version: str = "0.1.0"
    description: str = ""
    author: str = ""
    plugin_type: str = ""  # "ingester", "compiler", "processor"
    

class PluginBase(ABC):
    """Abstract base for all BigBrain plugins."""
    
    @abstractmethod
    def info(self) -> PluginInfo:
        """Return plugin metadata."""
        ...
    
    def activate(self) -> None:
        """Called when the plugin is loaded. Override for setup."""
        pass
    
    def deactivate(self) -> None:
        """Called when the plugin is unloaded. Override for cleanup."""
        pass


class IngestPlugin(PluginBase):
    """Plugin interface for custom file ingesters."""
    
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Return file extensions this plugin handles (e.g., ['.csv', '.tsv'])."""
        ...
    
    @abstractmethod
    def ingest(self, path: Path) -> Document:
        """Ingest a file and return a Document."""
        ...
    
    def info(self) -> PluginInfo:
        return PluginInfo(name=self.__class__.__name__, plugin_type="ingester")


class CompilePlugin(PluginBase):
    """Plugin interface for custom output compilers."""
    
    @abstractmethod
    def format_name(self) -> str:
        """Return the output format name (e.g., 'html', 'anki')."""
        ...
    
    @abstractmethod
    def compile(self, doc: Document, summaries: list, entities: list, relationships: list) -> CompileOutput:
        """Compile distilled content into the plugin's output format."""
        ...
    
    def info(self) -> PluginInfo:
        return PluginInfo(name=self.__class__.__name__, plugin_type="compiler")


class ProcessorPlugin(PluginBase):
    """Plugin interface for custom document processors (post-ingest, pre-distill)."""
    
    @abstractmethod
    def process(self, doc: Document) -> Document:
        """Process a document (transform, enrich, filter, etc.)."""
        ...
    
    def info(self) -> PluginInfo:
        return PluginInfo(name=self.__class__.__name__, plugin_type="processor")
