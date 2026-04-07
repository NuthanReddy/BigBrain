"""Tests for bigbrain.ingest.python_ingester."""

from pathlib import Path

import pytest

from bigbrain.ingest.python_ingester import PythonIngester
from bigbrain.kb.models import Document
from bigbrain.errors import FileAccessError

from tests.conftest import FIXTURES_DIR


class TestPythonIngester:
    """Tests for PythonIngester."""

    def setup_method(self):
        self.ingester = PythonIngester()

    def test_ingest_sample_py(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.py")
        assert isinstance(doc, Document)
        assert doc.content  # non-empty

    def test_extracts_symbols(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.py")
        symbols = doc.metadata.get("symbols", [])
        assert len(symbols) >= 2  # at least hello() and Calculator

        names = [s["name"] for s in symbols]
        assert "hello" in names
        assert "Calculator" in names

        types = {s["name"]: s["type"] for s in symbols}
        assert types["hello"] == "function"
        assert types["Calculator"] == "class"

    def test_extracts_module_docstring(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.py")
        module_doc = doc.metadata.get("module_docstring", "")
        assert "Sample Python module" in module_doc

    def test_language_is_python(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.py")
        assert doc.language == "python"

    def test_sections_correspond_to_definitions(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.py")
        assert len(doc.sections) >= 2
        section_titles = [s.title for s in doc.sections]
        assert any("hello" in t for t in section_titles)
        assert any("Calculator" in t for t in section_titles)

    def test_source_metadata(self):
        doc = self.ingester.ingest(FIXTURES_DIR / "sample.py")
        assert doc.source is not None
        assert doc.source.source_type == "py"
        assert doc.source.file_extension == ".py"

    def test_raises_file_access_error_for_nonexistent(self):
        with pytest.raises(FileAccessError):
            self.ingester.ingest(Path("/nonexistent/file.py"))
