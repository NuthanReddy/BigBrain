"""Tests for the Phase 9 plugin system."""

from __future__ import annotations

from pathlib import Path

import pytest

from bigbrain.plugins.base import (
    CompilePlugin,
    IngestPlugin,
    PluginBase,
    PluginInfo,
    ProcessorPlugin,
)
from bigbrain.plugins.discovery import discover_from_directory, discover_from_entry_points
from bigbrain.plugins.loader import PluginLoader
from bigbrain.config import PluginConfig
from bigbrain.kb.models import Document, DocumentSection, SourceMetadata
from bigbrain.compile.models import CompileOutput
from bigbrain.distill.models import Summary, Entity


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _create_test_plugin(tmp_path: Path) -> Path:
    """Write a minimal IngestPlugin file into *tmp_path* and return the dir."""
    plugin_code = """\
from bigbrain.plugins.base import IngestPlugin, PluginInfo
from bigbrain.kb.models import Document, SourceMetadata
from pathlib import Path

class TestPlugin(IngestPlugin):
    def info(self):
        return PluginInfo(name="test_plugin", version="0.1.0", plugin_type="ingester")
    def supported_extensions(self):
        return [".test"]
    def ingest(self, path):
        return Document(
            title="Test",
            content="test",
            source=SourceMetadata(
                file_path=str(path), file_extension=".test", source_type="test",
            ),
        )
"""
    (tmp_path / "test_plugin.py").write_text(plugin_code, encoding="utf-8")
    return tmp_path


def _create_test_csv(tmp_path: Path) -> Path:
    csv_content = "name,age,city\nAlice,30,NYC\nBob,25,LA\n"
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(csv_content, encoding="utf-8")
    return csv_path


# ===================================================================
# PluginInfo
# ===================================================================

class TestPluginInfo:
    def test_default_values(self):
        info = PluginInfo(name="demo")
        assert info.name == "demo"
        assert info.version == "0.1.0"
        assert info.description == ""
        assert info.author == ""
        assert info.plugin_type == ""

    def test_custom_values(self):
        info = PluginInfo(
            name="custom",
            version="2.0.0",
            description="A custom plugin",
            author="Tester",
            plugin_type="ingester",
        )
        assert info.name == "custom"
        assert info.version == "2.0.0"
        assert info.description == "A custom plugin"
        assert info.author == "Tester"
        assert info.plugin_type == "ingester"


# ===================================================================
# PluginBase / IngestPlugin / CompilePlugin / ProcessorPlugin
# ===================================================================

class TestPluginBase:
    def test_ingest_plugin_interface(self):
        """Concrete IngestPlugin returns sensible info()."""

        class MyIngester(IngestPlugin):
            def supported_extensions(self):
                return [".xyz"]

            def ingest(self, path):
                return Document(title="x", content="y", source=SourceMetadata(
                    file_path=str(path), file_extension=".xyz", source_type="xyz",
                ))

        p = MyIngester()
        info = p.info()
        assert info.plugin_type == "ingester"
        assert info.name == "MyIngester"
        assert p.supported_extensions() == [".xyz"]

    def test_compile_plugin_interface(self):
        class MyCompiler(CompilePlugin):
            def format_name(self):
                return "custom"

            def compile(self, doc, summaries, entities, relationships):
                return CompileOutput(title="out", content="compiled")

        p = MyCompiler()
        info = p.info()
        assert info.plugin_type == "compiler"
        assert info.name == "MyCompiler"
        assert p.format_name() == "custom"

    def test_processor_plugin_interface(self):
        class MyProcessor(ProcessorPlugin):
            def process(self, doc):
                return doc

        p = MyProcessor()
        info = p.info()
        assert info.plugin_type == "processor"
        assert info.name == "MyProcessor"

    def test_activate_deactivate(self):
        """Default activate/deactivate are harmless no-ops."""

        class Dummy(IngestPlugin):
            def supported_extensions(self):
                return []

            def ingest(self, path):
                return Document()

        d = Dummy()
        d.activate()   # should not raise
        d.deactivate()  # should not raise


# ===================================================================
# Plugin discovery
# ===================================================================

class TestPluginDiscovery:
    def test_discover_from_directory(self, tmp_path):
        _create_test_plugin(tmp_path)
        classes = discover_from_directory(tmp_path)
        assert len(classes) >= 1
        names = [c.__name__ for c in classes]
        assert "TestPlugin" in names

    def test_discover_empty_directory(self, tmp_path):
        assert discover_from_directory(tmp_path) == []

    def test_discover_nonexistent_directory(self, tmp_path):
        assert discover_from_directory(tmp_path / "no_such_dir") == []

    def test_discover_skips_underscored_files(self, tmp_path):
        _create_test_plugin(tmp_path)
        (tmp_path / "_private.py").write_text(
            "from bigbrain.plugins.base import IngestPlugin, PluginInfo\n"
            "from bigbrain.kb.models import Document, SourceMetadata\n"
            "from pathlib import Path\n"
            "class HiddenPlugin(IngestPlugin):\n"
            "    def info(self): return PluginInfo(name='hidden')\n"
            "    def supported_extensions(self): return ['.hid']\n"
            "    def ingest(self, path): return Document()\n",
            encoding="utf-8",
        )
        classes = discover_from_directory(tmp_path)
        names = [c.__name__ for c in classes]
        assert "HiddenPlugin" not in names

    def test_discover_from_entry_points(self):
        """Should return a list (possibly empty) without crashing."""
        result = discover_from_entry_points()
        assert isinstance(result, list)


# ===================================================================
# PluginLoader
# ===================================================================

class TestPluginLoader:
    def test_load_all_from_directory(self, tmp_path):
        _create_test_plugin(tmp_path)
        config = PluginConfig(plugins_dir=str(tmp_path), auto_discover=True)
        loader = PluginLoader(config=config)
        count = loader.load_all()
        assert count >= 1
        assert len(loader.ingest_plugins) >= 1

    def test_disabled_plugin_skipped(self, tmp_path):
        _create_test_plugin(tmp_path)
        config = PluginConfig(
            plugins_dir=str(tmp_path),
            auto_discover=True,
            disabled_plugins=["test_plugin"],
        )
        loader = PluginLoader(config=config)
        count = loader.load_all()
        assert count == 0

    def test_enabled_plugins_filter(self, tmp_path):
        _create_test_plugin(tmp_path)
        config = PluginConfig(
            plugins_dir=str(tmp_path),
            auto_discover=True,
            enabled_plugins=["nonexistent_plugin"],
        )
        loader = PluginLoader(config=config)
        count = loader.load_all()
        assert count == 0

    def test_list_plugins(self, tmp_path):
        _create_test_plugin(tmp_path)
        config = PluginConfig(plugins_dir=str(tmp_path), auto_discover=True)
        loader = PluginLoader(config=config)
        loader.load_all()
        infos = loader.list_plugins()
        assert len(infos) >= 1
        assert all(isinstance(i, PluginInfo) for i in infos)

    def test_unload_all(self, tmp_path):
        _create_test_plugin(tmp_path)
        config = PluginConfig(plugins_dir=str(tmp_path), auto_discover=True)
        loader = PluginLoader(config=config)
        loader.load_all()
        assert len(loader.list_plugins()) >= 1
        loader.unload_all()
        assert loader.list_plugins() == []
        assert loader.ingest_plugins == []
        assert loader.compile_plugins == []
        assert loader.processor_plugins == []

    def test_register_with_ingest(self, tmp_path):
        """After register_with_ingest the ingestion registry knows the extension."""
        _create_test_plugin(tmp_path)
        config = PluginConfig(plugins_dir=str(tmp_path), auto_discover=True)
        loader = PluginLoader(config=config)
        loader.load_all()

        from bigbrain.ingest import registry as reg
        # save original state
        original = dict(reg._registry)
        try:
            registered = loader.register_with_ingest()
            assert registered >= 1
            assert reg.get_ingester(".test") is not None
        finally:
            reg._registry.clear()
            reg._registry.update(original)


# ===================================================================
# CsvIngesterPlugin
# ===================================================================

class TestCsvIngesterPlugin:
    @pytest.fixture()
    def plugin(self):
        from plugins.csv_ingester import CsvIngesterPlugin
        return CsvIngesterPlugin()

    def test_info(self, plugin):
        info = plugin.info()
        assert info.name == "csv_ingester"
        assert info.plugin_type == "ingester"
        assert info.version == "1.0.0"

    def test_supported_extensions(self, plugin):
        assert plugin.supported_extensions() == [".csv"]

    def test_ingest_csv(self, plugin, tmp_path):
        csv_path = _create_test_csv(tmp_path)
        doc = plugin.ingest(csv_path)
        assert isinstance(doc, Document)
        assert doc.title == "Test"
        assert "Alice" in doc.content
        assert "Bob" in doc.content
        assert doc.source.file_extension == ".csv"
        assert doc.source.source_type == "csv"
        assert doc.metadata["row_count"] == 2
        assert doc.metadata["column_count"] == 3

    def test_ingest_csv_sections(self, plugin, tmp_path):
        csv_path = _create_test_csv(tmp_path)
        doc = plugin.ingest(csv_path)
        assert len(doc.sections) == 1
        section = doc.sections[0]
        assert section.title == "Data"
        assert section.metadata["rows"] == 2
        assert section.metadata["columns"] == 3
        assert section.metadata["headers"] == ["name", "age", "city"]


# ===================================================================
# HtmlCompilerPlugin
# ===================================================================

class TestHtmlCompilerPlugin:
    @pytest.fixture()
    def plugin(self):
        from plugins.html_compiler import HtmlCompilerPlugin
        return HtmlCompilerPlugin()

    def test_info(self, plugin):
        info = plugin.info()
        assert info.name == "html_compiler"
        assert info.plugin_type == "compiler"
        assert info.version == "1.0.0"

    def test_format_name(self, plugin):
        assert plugin.format_name() == "html"

    def test_compile_output(self, plugin):
        doc = Document(title="My Doc", content="Some content")
        summaries = [Summary(content="This is a summary")]
        entities = [Entity(name="Python", entity_type="language", description="A programming language")]
        result = plugin.compile(doc, summaries, entities, relationships=[])

        assert isinstance(result, CompileOutput)
        assert "My Doc" in result.title
        assert "<h1>My Doc</h1>" in result.content
        assert "This is a summary" in result.content
        assert "<strong>Python</strong>" in result.content
        assert "(language)" in result.content
        assert "A programming language" in result.content
        assert result.content.startswith("<!DOCTYPE html>")
