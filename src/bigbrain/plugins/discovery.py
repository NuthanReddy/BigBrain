"""Plugin discovery — finds plugins from directories and entry points."""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Type

from bigbrain.logging_config import get_logger
from bigbrain.plugins.base import PluginBase

logger = get_logger(__name__)


def discover_from_directory(plugins_dir: str | Path) -> list[Type[PluginBase]]:
    """Discover plugin classes from Python files in a directory.
    
    Scans for .py files, imports them, and finds classes that subclass PluginBase.
    """
    plugins_path = Path(plugins_dir)
    if not plugins_path.is_dir():
        return []
    
    found: list[Type[PluginBase]] = []
    
    for py_file in sorted(plugins_path.glob("*.py")):
        if py_file.name.startswith("_"):
            continue
        try:
            module_name = f"bigbrain_plugin_{py_file.stem}"
            spec = importlib.util.spec_from_file_location(module_name, str(py_file))
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, PluginBase)
                    and attr is not PluginBase
                    and not getattr(attr, '__abstractmethods__', None)
                ):
                    found.append(attr)
                    logger.debug("Discovered plugin: %s from %s", attr_name, py_file)
        except Exception as exc:
            logger.warning("Failed to load plugin from %s: %s", py_file, exc)
    
    return found


def discover_from_entry_points(group: str = "bigbrain.plugins") -> list[Type[PluginBase]]:
    """Discover plugins registered via setuptools entry_points."""
    found: list[Type[PluginBase]] = []
    
    try:
        if sys.version_info >= (3, 12):
            from importlib.metadata import entry_points
            eps = entry_points(group=group)
        else:
            from importlib.metadata import entry_points
            all_eps = entry_points()
            eps = all_eps.get(group, []) if isinstance(all_eps, dict) else all_eps.select(group=group) if hasattr(all_eps, 'select') else []
    except Exception:
        return found
    
    for ep in eps:
        try:
            plugin_cls = ep.load()
            if isinstance(plugin_cls, type) and issubclass(plugin_cls, PluginBase):
                found.append(plugin_cls)
                logger.debug("Discovered entry_point plugin: %s", ep.name)
        except Exception as exc:
            logger.warning("Failed to load entry_point plugin %s: %s", ep.name, exc)
    
    return found
