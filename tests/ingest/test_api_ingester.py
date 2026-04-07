"""Tests for bigbrain.ingest.api_ingester."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import httpx
import pytest

from bigbrain.errors import FileAccessError
from bigbrain.ingest.api_ingester import ApiIngester
from bigbrain.kb.models import Document


def _mock_json_response(
    data: object,
    status_code: int = 200,
    content_type: str = "application/json",
    url: str = "https://api.example.com/v1/items",
) -> httpx.Response:
    """Build a mock httpx.Response that returns *data* from .json()."""
    body = json.dumps(data)
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = data
    resp.text = body
    resp.content = body.encode("utf-8")
    resp.url = httpx.URL(url)
    resp.headers = {"content-type": content_type}
    resp.raise_for_status = MagicMock()
    return resp


SAMPLE_PAYLOAD = {
    "title": "Sample API Result",
    "description": "A longer description field that is meaningful.",
    "items": [
        {"id": 1, "name": "alpha"},
        {"id": 2, "name": "beta"},
    ],
    "count": 2,
}


class TestApiIngester:
    """Tests for ApiIngester."""

    def setup_method(self):
        self.ingester = ApiIngester()

    # ------------------------------------------------------------------
    # Core ingest
    # ------------------------------------------------------------------

    @patch("bigbrain.ingest.api_ingester.httpx.get")
    def test_ingest_json_endpoint(self, mock_get):
        mock_get.return_value = _mock_json_response(SAMPLE_PAYLOAD)
        doc = self.ingester.ingest("https://api.example.com/v1/items")
        assert isinstance(doc, Document)
        assert doc.title == "Sample API Result"
        assert doc.content  # non-empty
        assert doc.source is not None
        assert doc.source.source_type == "api"
        assert doc.source.file_extension == ".json"
        assert doc.language == "json"

    @patch("bigbrain.ingest.api_ingester.httpx.get")
    def test_ingest_with_json_path(self, mock_get):
        payload = {"data": {"content": {"text": "nested value"}}}
        mock_get.return_value = _mock_json_response(payload)
        doc = self.ingester.ingest(
            "https://api.example.com/v1/items", json_path="data.content"
        )
        assert "nested value" in doc.content

    @patch("bigbrain.ingest.api_ingester.httpx.get")
    def test_ingest_with_auth_token(self, mock_get):
        mock_get.return_value = _mock_json_response({"title": "auth test", "body": "some longer body text here."})
        ingester = ApiIngester(auth_token="secret-tok")
        ingester.ingest("https://api.example.com/secure")
        _, kwargs = mock_get.call_args
        assert kwargs["headers"]["Authorization"] == "Bearer secret-tok"

    @patch("bigbrain.ingest.api_ingester.httpx.get")
    def test_ingest_non_json_raises(self, mock_get):
        resp = _mock_json_response({})
        resp.json.side_effect = ValueError("not JSON")
        mock_get.return_value = resp
        with pytest.raises(FileAccessError, match="not valid JSON"):
            self.ingester.ingest("https://api.example.com/text")

    @patch("bigbrain.ingest.api_ingester.httpx.get")
    def test_ingest_timeout_raises(self, mock_get):
        mock_get.side_effect = httpx.TimeoutException("timed out")
        with pytest.raises(FileAccessError, match="timed out"):
            self.ingester.ingest("https://api.example.com/slow")

    @patch("bigbrain.ingest.api_ingester.httpx.get")
    def test_ingest_http_error_raises(self, mock_get):
        resp = _mock_json_response({}, status_code=404)
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=MagicMock(), response=resp
        )
        mock_get.return_value = resp
        with pytest.raises(FileAccessError, match="HTTP 404"):
            self.ingester.ingest("https://api.example.com/missing")

    @patch("bigbrain.ingest.api_ingester.httpx.get")
    def test_ingest_http_500_raises(self, mock_get):
        resp = _mock_json_response({}, status_code=500)
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server Error", request=MagicMock(), response=resp
        )
        mock_get.return_value = resp
        with pytest.raises(FileAccessError, match="HTTP 500"):
            self.ingester.ingest("https://api.example.com/broken")

    @patch("bigbrain.ingest.api_ingester.httpx.get")
    def test_ingest_connect_error_raises(self, mock_get):
        mock_get.side_effect = httpx.ConnectError("refused")
        with pytest.raises(FileAccessError, match="Cannot connect"):
            self.ingester.ingest("https://unreachable.test/api")

    # ------------------------------------------------------------------
    # _flatten_json
    # ------------------------------------------------------------------

    def test_flatten_json_dict(self):
        data = {"name": "Alice", "age": 30}
        result = ApiIngester._flatten_json(data)
        assert "name: Alice" in result
        assert "age: 30" in result

    def test_flatten_json_list(self):
        data = ["apple", "banana", "cherry"]
        result = ApiIngester._flatten_json(data)
        assert "• apple" in result
        assert "• banana" in result
        assert "• cherry" in result

    def test_flatten_json_nested(self):
        data = {
            "user": {"name": "Bob", "scores": [10, 20]},
        }
        result = ApiIngester._flatten_json(data)
        assert "user:" in result
        assert "name: Bob" in result

    def test_flatten_json_string(self):
        assert ApiIngester._flatten_json("hello") == "hello"

    def test_flatten_json_number(self):
        assert ApiIngester._flatten_json(42) == "42"

    def test_flatten_json_none(self):
        assert ApiIngester._flatten_json(None) == ""

    # ------------------------------------------------------------------
    # _extract_path
    # ------------------------------------------------------------------

    def test_extract_path_simple(self):
        data = {"a": {"b": {"c": "deep"}}}
        assert ApiIngester._extract_path(data, "a.b.c") == "deep"

    def test_extract_path_list_index(self):
        data = {"items": ["zero", "one", "two"]}
        assert ApiIngester._extract_path(data, "items.1") == "one"

    def test_extract_path_missing_key(self):
        data = {"a": 1}
        assert ApiIngester._extract_path(data, "a.b.c") is None

    def test_extract_path_top_level(self):
        data = {"key": "value"}
        assert ApiIngester._extract_path(data, "key") == "value"

    # ------------------------------------------------------------------
    # _extract_title
    # ------------------------------------------------------------------

    def test_extract_title_from_title_field(self):
        assert ApiIngester._extract_title({"title": "My Title"}) == "My Title"

    def test_extract_title_from_name_field(self):
        assert ApiIngester._extract_title({"name": "My Name"}) == "My Name"

    def test_extract_title_from_heading_field(self):
        assert ApiIngester._extract_title({"heading": "A Heading"}) == "A Heading"

    def test_extract_title_prefers_title_over_name(self):
        assert (
            ApiIngester._extract_title({"title": "T", "name": "N"}) == "T"
        )

    def test_extract_title_returns_empty_for_no_match(self):
        assert ApiIngester._extract_title({"foo": "bar"}) == ""

    def test_extract_title_returns_empty_for_non_dict(self):
        assert ApiIngester._extract_title([1, 2, 3]) == ""

    # ------------------------------------------------------------------
    # _json_to_sections
    # ------------------------------------------------------------------

    def test_json_to_sections_from_dict(self):
        data = {
            "overview": "A longer overview of the topic at hand.",
            "details": "More detailed information about the subject.",
            "short": "tiny",  # too short, should be excluded
        }
        sections = ApiIngester._json_to_sections(data)
        titles = [s.title for s in sections]
        assert "overview" in titles
        assert "details" in titles
        assert "short" not in titles  # content len <= 10

    def test_json_to_sections_from_non_dict(self):
        assert ApiIngester._json_to_sections(["a", "b"]) == []

    def test_json_to_sections_level(self):
        data = {"section": "Enough content here to pass the threshold."}
        sections = ApiIngester._json_to_sections(data)
        assert sections[0].level == 1

    # ------------------------------------------------------------------
    # Source metadata
    # ------------------------------------------------------------------

    @patch("bigbrain.ingest.api_ingester.httpx.get")
    def test_source_metadata_fields(self, mock_get):
        mock_get.return_value = _mock_json_response(SAMPLE_PAYLOAD)
        doc = self.ingester.ingest("https://api.example.com/v1/items")
        src = doc.source
        assert src.file_path == "https://api.example.com/v1/items"
        assert src.extra["url"] == "https://api.example.com/v1/items"
        assert src.extra["status_code"] == 200
        assert src.extra["json_path"] == ""
        assert src.size_bytes > 0

    @patch("bigbrain.ingest.api_ingester.httpx.get")
    def test_metadata_contains_fetched_at(self, mock_get):
        mock_get.return_value = _mock_json_response(SAMPLE_PAYLOAD)
        doc = self.ingester.ingest("https://api.example.com/v1/items")
        assert "fetched_at" in doc.metadata
        assert doc.metadata["url"] == "https://api.example.com/v1/items"

    # ------------------------------------------------------------------
    # Fallback title (no title/name/heading field)
    # ------------------------------------------------------------------

    @patch("bigbrain.ingest.api_ingester.httpx.get")
    def test_title_falls_back_to_url(self, mock_get):
        payload = {"data": "some content that is long enough."}
        mock_get.return_value = _mock_json_response(payload)
        doc = self.ingester.ingest("https://api.example.com/v1/items")
        assert "api.example.com" in doc.title
