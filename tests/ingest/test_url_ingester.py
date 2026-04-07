"""Tests for bigbrain.ingest.url_ingester."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx
import pytest

from bigbrain.errors import FileAccessError
from bigbrain.ingest.url_ingester import UrlIngester
from bigbrain.kb.models import Document

SAMPLE_HTML = """\
<html>
<head><title>Test Page</title></head>
<body>
<h1>Main Heading</h1>
<p>First paragraph of content.</p>
<h2>Sub Heading</h2>
<p>Second paragraph with details.</p>
<script>var x = 1;</script>
<nav><a href="/">Home</a></nav>
</body>
</html>
"""


def _mock_response(
    html: str = SAMPLE_HTML,
    status_code: int = 200,
    content_type: str = "text/html; charset=utf-8",
    url: str = "https://example.com/page",
) -> httpx.Response:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.text = html
    resp.content = html.encode("utf-8")
    resp.url = httpx.URL(url)
    resp.headers = {"content-type": content_type}
    resp.raise_for_status = MagicMock()
    return resp


class TestUrlIngester:
    """Tests for UrlIngester."""

    def setup_method(self):
        self.ingester = UrlIngester()

    @patch("bigbrain.ingest.url_ingester.httpx.get")
    def test_ingest_returns_document(self, mock_get):
        mock_get.return_value = _mock_response()
        doc = self.ingester.ingest("https://example.com/page")
        assert isinstance(doc, Document)
        assert doc.content  # non-empty
        assert doc.title == "Test Page"

    @patch("bigbrain.ingest.url_ingester.httpx.get")
    def test_source_metadata(self, mock_get):
        mock_get.return_value = _mock_response()
        doc = self.ingester.ingest("https://example.com/page")
        assert doc.source is not None
        assert doc.source.source_type == "url"
        assert doc.source.file_extension == ".html"
        assert doc.source.extra["url"] == "https://example.com/page"

    @patch("bigbrain.ingest.url_ingester.httpx.get")
    def test_extracts_sections_from_headings(self, mock_get):
        mock_get.return_value = _mock_response()
        doc = self.ingester.ingest("https://example.com/page")
        titles = [s.title for s in doc.sections]
        assert "Main Heading" in titles
        assert "Sub Heading" in titles

    @patch("bigbrain.ingest.url_ingester.httpx.get")
    def test_section_levels(self, mock_get):
        mock_get.return_value = _mock_response()
        doc = self.ingester.ingest("https://example.com/page")
        by_title = {s.title: s for s in doc.sections}
        assert by_title["Main Heading"].level == 1
        assert by_title["Sub Heading"].level == 2

    @patch("bigbrain.ingest.url_ingester.httpx.get")
    def test_strips_script_style_nav(self, mock_get):
        html = (
            "<html><head><title>T</title>"
            "<style>body { color: red; }</style></head>"
            "<body><nav><a>nav link</a></nav>"
            "<script>var x = 1;</script>"
            "<p>Real content here.</p></body></html>"
        )
        mock_get.return_value = _mock_response(html=html)
        doc = self.ingester.ingest("https://example.com/page")
        assert "var x = 1" not in doc.content
        assert "color: red" not in doc.content
        assert "nav link" not in doc.content
        assert "Real content" in doc.content

    @patch("bigbrain.ingest.url_ingester.httpx.get")
    def test_title_falls_back_to_h1(self, mock_get):
        html = "<html><body><h1>Fallback Title</h1><p>body</p></body></html>"
        mock_get.return_value = _mock_response(html=html)
        doc = self.ingester.ingest("https://example.com")
        assert doc.title == "Fallback Title"

    @patch("bigbrain.ingest.url_ingester.httpx.get")
    def test_title_falls_back_to_url(self, mock_get):
        html = "<html><body><p>no headings</p></body></html>"
        mock_get.return_value = _mock_response(html=html)
        doc = self.ingester.ingest("https://example.com/about")
        assert "example.com" in doc.title

    @patch("bigbrain.ingest.url_ingester.httpx.get")
    def test_raises_on_timeout(self, mock_get):
        mock_get.side_effect = httpx.TimeoutException("timed out")
        with pytest.raises(FileAccessError, match="timed out"):
            self.ingester.ingest("https://example.com")

    @patch("bigbrain.ingest.url_ingester.httpx.get")
    def test_raises_on_http_error(self, mock_get):
        resp = _mock_response(status_code=404)
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=MagicMock(), response=resp
        )
        mock_get.return_value = resp
        with pytest.raises(FileAccessError, match="HTTP 404"):
            self.ingester.ingest("https://example.com/missing")

    @patch("bigbrain.ingest.url_ingester.httpx.get")
    def test_raises_on_connect_error(self, mock_get):
        mock_get.side_effect = httpx.ConnectError("refused")
        with pytest.raises(FileAccessError, match="Cannot connect"):
            self.ingester.ingest("https://unreachable.test")

    @patch("bigbrain.ingest.url_ingester.httpx.get")
    def test_raises_on_unsupported_content_type(self, mock_get):
        mock_get.return_value = _mock_response(content_type="application/pdf")
        with pytest.raises(FileAccessError, match="Unsupported content type"):
            self.ingester.ingest("https://example.com/file.pdf")

    @patch("bigbrain.ingest.url_ingester.httpx.get")
    def test_raises_on_oversized_response(self, mock_get):
        ingester = UrlIngester(max_size_mb=0)  # 0 MB limit
        mock_get.return_value = _mock_response()
        with pytest.raises(FileAccessError, match="too large"):
            ingester.ingest("https://example.com")

    @patch("bigbrain.ingest.url_ingester.httpx.get")
    def test_metadata_contains_url_and_fetched_at(self, mock_get):
        mock_get.return_value = _mock_response()
        doc = self.ingester.ingest("https://example.com/page")
        assert doc.metadata["url"] == "https://example.com/page"
        assert "fetched_at" in doc.metadata
