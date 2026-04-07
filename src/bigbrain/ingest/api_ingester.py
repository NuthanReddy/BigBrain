"""REST API JSON ingester — fetches and flattens JSON from API endpoints."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

import httpx

from bigbrain.errors import FileAccessError
from bigbrain.kb.models import Document, DocumentSection, SourceMetadata
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


class ApiIngester:
    """Ingests content from REST API JSON endpoints."""

    def __init__(
        self,
        *,
        timeout: int = 30,
        headers: dict[str, str] | None = None,
        auth_token: str = "",
    ) -> None:
        self._timeout = timeout
        self._headers = headers or {}
        if auth_token:
            self._headers["Authorization"] = f"Bearer {auth_token}"

    def ingest(self, url: str, *, json_path: str = "") -> Document:
        """Fetch a JSON API endpoint and return a Document.

        Args:
            url: The API endpoint URL
            json_path: Dot-separated path to extract content from response
                       (e.g., "data.content" or "results"). Empty = use full response.

        Returns:
            Document with flattened JSON as content

        Raises:
            FileAccessError: On fetch failures or invalid responses
        """
        request_headers = {
            "Accept": "application/json",
            "User-Agent": "BigBrain/1.0",
            **self._headers,
        }
        try:
            resp = httpx.get(
                url,
                follow_redirects=True,
                timeout=self._timeout,
                headers=request_headers,
            )
            resp.raise_for_status()
        except httpx.TimeoutException:
            raise FileAccessError(url, f"Request timed out after {self._timeout}s")
        except httpx.HTTPStatusError as exc:
            raise FileAccessError(url, f"HTTP {exc.response.status_code}")
        except httpx.ConnectError:
            raise FileAccessError(url, "Cannot connect")
        except Exception as exc:
            raise FileAccessError(url, str(exc))

        try:
            data = resp.json()
        except Exception:
            raise FileAccessError(url, "Response is not valid JSON")

        if json_path:
            data = self._extract_path(data, json_path)

        content = self._flatten_json(data)
        sections = self._json_to_sections(data)

        parsed = urlparse(url)
        title = self._extract_title(data) or f"API: {parsed.netloc}{parsed.path}"

        source = SourceMetadata(
            file_path=url,
            file_extension=".json",
            source_type="api",
            modified_at=datetime.now(timezone.utc),
            size_bytes=len(content.encode("utf-8")),
            extra={
                "url": url,
                "status_code": resp.status_code,
                "json_path": json_path,
            },
        )

        return Document(
            title=title,
            content=content,
            source=source,
            language="json",
            sections=sections,
            metadata={"url": url, "fetched_at": datetime.now(timezone.utc).isoformat()},
        )

    def ingest_paginated(
        self,
        url: str,
        *,
        results_key: str = "results",
        next_key: str = "next",
        max_pages: int = 10,
    ) -> list[Document]:
        """Ingest from a paginated API endpoint.

        Returns one Document per page of results.
        """
        docs: list[Document] = []
        current_url = url
        request_headers = {
            "Accept": "application/json",
            "User-Agent": "BigBrain/1.0",
            **self._headers,
        }

        for page_num in range(max_pages):
            try:
                doc = self.ingest(current_url, json_path=results_key)
                doc.title = f"{doc.title} (page {page_num + 1})"
                docs.append(doc)

                resp = httpx.get(
                    current_url,
                    follow_redirects=True,
                    timeout=self._timeout,
                    headers=request_headers,
                )
                data = resp.json()
                next_url = data.get(next_key)
                if not next_url:
                    break
                current_url = next_url
            except Exception as exc:
                logger.warning("Pagination stopped at page %d: %s", page_num + 1, exc)
                break

        return docs

    @staticmethod
    def _extract_path(data: Any, path: str) -> Any:
        """Extract a value from nested dict using dot-separated path."""
        parts = path.split(".")
        current = data
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list) and part.isdigit():
                idx = int(part)
                current = current[idx] if idx < len(current) else None
            else:
                return None
            if current is None:
                return None
        return current

    @staticmethod
    def _flatten_json(data: Any, indent: int = 0) -> str:
        """Flatten JSON data to readable plain text."""
        if isinstance(data, str):
            return data
        if isinstance(data, (int, float, bool)):
            return str(data)
        if data is None:
            return ""
        if isinstance(data, list):
            parts = []
            for i, item in enumerate(data):
                prefix = f"[{i}] " if not isinstance(item, str) else "• "
                parts.append(f"{prefix}{ApiIngester._flatten_json(item, indent + 1)}")
            return "\n".join(parts)
        if isinstance(data, dict):
            parts = []
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    parts.append(f"{key}:")
                    parts.append(ApiIngester._flatten_json(value, indent + 1))
                else:
                    parts.append(f"{key}: {value}")
            return "\n".join(parts)
        return str(data)

    @staticmethod
    def _json_to_sections(data: Any) -> list[DocumentSection]:
        """Convert top-level JSON keys to document sections."""
        if not isinstance(data, dict):
            return []
        sections = []
        for key, value in data.items():
            content = ApiIngester._flatten_json(value)
            if content and len(content) > 10:
                sections.append(DocumentSection(
                    title=str(key),
                    content=content,
                    level=1,
                ))
        return sections

    @staticmethod
    def _extract_title(data: Any) -> str:
        """Try to extract a title from common JSON fields."""
        if isinstance(data, dict):
            for key in ("title", "name", "heading", "subject", "label"):
                val = data.get(key)
                if isinstance(val, str) and val:
                    return val
        return ""
