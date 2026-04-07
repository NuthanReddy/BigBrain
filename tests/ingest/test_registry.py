"""Tests for bigbrain.ingest.registry."""

from pathlib import Path

from bigbrain.ingest.registry import (
    BaseIngester,
    get_ingester,
    get_registered_extensions,
    register_ingester,
    _registry,
)
from bigbrain.kb.models import Document, SourceMetadata

# Ensure default ingesters are loaded (service.py triggers this at import).
from bigbrain.ingest.service import _init_default_ingesters  # noqa: F401


class TestRegistry:
    """Tests for the ingester registry."""

    def test_default_ingesters_registered(self):
        exts = get_registered_extensions()
        for ext in [".txt", ".md", ".pdf", ".py"]:
            assert ext in exts, f"Expected '{ext}' in registered extensions"

    def test_get_ingester_returns_correct_type_for_txt(self):
        from bigbrain.ingest.text_ingester import TextIngester
        ing = get_ingester(".txt")
        assert isinstance(ing, TextIngester)

    def test_get_ingester_returns_correct_type_for_md(self):
        from bigbrain.ingest.markdown_ingester import MarkdownIngester
        ing = get_ingester(".md")
        assert isinstance(ing, MarkdownIngester)

    def test_get_ingester_returns_correct_type_for_pdf(self):
        from bigbrain.ingest.pdf_ingester import PdfIngester
        ing = get_ingester(".pdf")
        assert isinstance(ing, PdfIngester)

    def test_get_ingester_returns_correct_type_for_py(self):
        from bigbrain.ingest.python_ingester import PythonIngester
        ing = get_ingester(".py")
        assert isinstance(ing, PythonIngester)

    def test_get_ingester_returns_none_for_unknown(self):
        assert get_ingester(".xyz") is None
        assert get_ingester(".unknown") is None

    def test_get_registered_extensions_returns_sorted(self):
        exts = get_registered_extensions()
        assert exts == sorted(exts)

    def test_custom_ingester_can_be_registered(self):
        class DummyIngester(BaseIngester):
            def supported_extensions(self):
                return [".dummy"]

            def ingest(self, path: Path) -> Document:
                return Document(title="dummy", content="", source=None)

        register_ingester(DummyIngester())
        assert get_ingester(".dummy") is not None
        assert isinstance(get_ingester(".dummy"), DummyIngester)

        # Cleanup: remove our dummy from the global registry
        _registry.pop(".dummy", None)
