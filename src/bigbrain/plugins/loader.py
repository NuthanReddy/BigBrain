"""Plugin loader — discovers, validates, and registers plugins."""

from __future__ import annotations

from bigbrain.config import BigBrainConfig, PluginConfig, load_config
from bigbrain.logging_config import get_logger
from bigbrain.plugins.base import (
    CompilePlugin,
    IngestPlugin,
    PluginBase,
    PluginInfo,
    ProcessorPlugin,
)
from bigbrain.plugins.discovery import discover_from_directory, discover_from_entry_points

logger = get_logger(__name__)


class PluginLoader:
    """Discovers, loads, and manages BigBrain plugins.

    Usage::

        loader = PluginLoader.from_config()
        loader.load_all()
        print(loader.list_plugins())
    """

    def __init__(self, config: PluginConfig | None = None) -> None:
        self._config = config or PluginConfig()
        self._plugins: list[PluginBase] = []
        self._ingest_plugins: list[IngestPlugin] = []
        self._compile_plugins: list[CompilePlugin] = []
        self._processor_plugins: list[ProcessorPlugin] = []

    @classmethod
    def from_config(cls, config: BigBrainConfig | None = None) -> PluginLoader:
        """Create a loader from an application config (or the default)."""
        if config is None:
            config = load_config()
        return cls(config=config.plugins)

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load_all(self) -> int:
        """Discover and load all plugins. Returns count of loaded plugins."""
        plugin_classes: list[type[PluginBase]] = []

        if self._config.auto_discover:
            plugin_classes.extend(discover_from_directory(self._config.plugins_dir))
            plugin_classes.extend(discover_from_entry_points())

        loaded = 0
        for cls in plugin_classes:
            try:
                instance = cls()
                info = instance.info()

                if self._config.disabled_plugins and info.name in self._config.disabled_plugins:
                    logger.debug("Plugin %s is disabled, skipping", info.name)
                    continue
                if self._config.enabled_plugins and info.name not in self._config.enabled_plugins:
                    logger.debug("Plugin %s not in enabled list, skipping", info.name)
                    continue

                instance.activate()
                self._plugins.append(instance)

                if isinstance(instance, IngestPlugin):
                    self._ingest_plugins.append(instance)
                if isinstance(instance, CompilePlugin):
                    self._compile_plugins.append(instance)
                if isinstance(instance, ProcessorPlugin):
                    self._processor_plugins.append(instance)

                loaded += 1
                logger.info(
                    "Loaded plugin: %s v%s (%s)",
                    info.name,
                    info.version,
                    info.plugin_type,
                )
            except Exception as exc:
                logger.warning("Failed to load plugin %s: %s", cls.__name__, exc)

        return loaded

    # ------------------------------------------------------------------
    # Ingest-registry integration
    # ------------------------------------------------------------------

    def register_with_ingest(self) -> int:
        """Register ingest plugins with the ingestion registry."""
        from bigbrain.ingest.registry import register_ingester

        count = 0
        for plugin in self._ingest_plugins:
            adapter = _IngestPluginAdapter(plugin)
            register_ingester(adapter)
            count += 1
            logger.info(
                "Registered ingest plugin: %s for %s",
                plugin.info().name,
                plugin.supported_extensions(),
            )
        return count

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def list_plugins(self) -> list[PluginInfo]:
        """Return info for all loaded plugins."""
        return [p.info() for p in self._plugins]

    @property
    def ingest_plugins(self) -> list[IngestPlugin]:
        return list(self._ingest_plugins)

    @property
    def compile_plugins(self) -> list[CompilePlugin]:
        return list(self._compile_plugins)

    @property
    def processor_plugins(self) -> list[ProcessorPlugin]:
        return list(self._processor_plugins)

    # ------------------------------------------------------------------
    # Teardown
    # ------------------------------------------------------------------

    def unload_all(self) -> None:
        """Deactivate all plugins."""
        for p in self._plugins:
            try:
                p.deactivate()
            except Exception:
                pass
        self._plugins.clear()
        self._ingest_plugins.clear()
        self._compile_plugins.clear()
        self._processor_plugins.clear()


# ---------------------------------------------------------------------------
# Internal adapter
# ---------------------------------------------------------------------------


class _IngestPluginAdapter:
    """Adapts an :class:`IngestPlugin` to the :class:`BaseIngester` interface
    expected by the ingestion registry."""

    def __init__(self, plugin: IngestPlugin) -> None:
        self._plugin = plugin

    def supported_extensions(self) -> list[str]:
        return self._plugin.supported_extensions()

    def ingest(self, path):  # noqa: ANN001
        return self._plugin.ingest(path)
