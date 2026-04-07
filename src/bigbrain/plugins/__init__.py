"""Plugin system — extensibility for custom ingesters, compilers, and more."""

from bigbrain.plugins.base import (
    CompilePlugin,
    IngestPlugin,
    PluginBase,
    PluginInfo,
    ProcessorPlugin,
)
from bigbrain.plugins.loader import PluginLoader

__all__ = [
    "CompilePlugin",
    "IngestPlugin",
    "PluginBase",
    "PluginInfo",
    "PluginLoader",
    "ProcessorPlugin",
]
