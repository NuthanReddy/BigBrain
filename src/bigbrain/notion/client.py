"""Notion API client wrapper with error handling."""

from __future__ import annotations

import os
from typing import Any

from bigbrain.config import NotionConfig
from bigbrain.errors import NotionError
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


class NotionClient:
    """Wrapper around the Notion SDK with convenience methods.

    Usage::
        client = NotionClient.from_config(config.notion)
        pages = client.list_pages()
        content = client.get_page_content(page_id)
    """

    def __init__(self, token: str) -> None:
        if not token:
            raise NotionError("No Notion token configured. Set BIGBRAIN_NOTION_TOKEN env var.")
        from notion_client import Client

        self._client = Client(auth=token)
        self._token = token

    @classmethod
    def from_config(cls, config: NotionConfig) -> NotionClient:
        """Create from NotionConfig, resolving token from config or env."""
        token = config.token or os.environ.get("BIGBRAIN_NOTION_TOKEN", "")
        return cls(token)

    def is_available(self) -> bool:
        """Check if Notion API is reachable and token is valid."""
        try:
            self._client.users.me()
            return True
        except Exception:
            return False

    def search_pages(self, query: str = "", page_size: int = 20) -> list[dict]:
        """Search for pages in the workspace."""
        try:
            params: dict[str, Any] = {
                "page_size": page_size,
                "filter": {"property": "object", "value": "page"},
            }
            if query:
                params["query"] = query
            result = self._client.search(**params)
            return result.get("results", [])
        except Exception as exc:
            raise NotionError(f"Failed to search pages: {exc}") from exc

    def get_page(self, page_id: str) -> dict:
        """Get page metadata."""
        try:
            return self._client.pages.retrieve(page_id=page_id)
        except Exception as exc:
            raise NotionError(f"Failed to get page {page_id}: {exc}") from exc

    def get_page_blocks(self, page_id: str) -> list[dict]:
        """Get all content blocks from a page (handles pagination)."""
        blocks: list[dict] = []
        try:
            cursor: str | None = None
            while True:
                params: dict[str, Any] = {"block_id": page_id, "page_size": 100}
                if cursor:
                    params["start_cursor"] = cursor
                result = self._client.blocks.children.list(**params)
                blocks.extend(result.get("results", []))
                if not result.get("has_more"):
                    break
                cursor = result.get("next_cursor")
        except Exception as exc:
            raise NotionError(f"Failed to get blocks for {page_id}: {exc}") from exc
        return blocks

    def create_page(
        self,
        parent_id: str,
        title: str,
        children: list[dict] | None = None,
    ) -> dict:
        """Create a new page under a parent page."""
        try:
            page_data: dict[str, Any] = {
                "parent": {"page_id": parent_id},
                "properties": {
                    "title": [{"text": {"content": title}}],
                },
            }
            if children:
                page_data["children"] = children
            return self._client.pages.create(**page_data)
        except Exception as exc:
            raise NotionError(f"Failed to create page '{title}': {exc}") from exc

    def update_page_blocks(self, page_id: str, children: list[dict]) -> None:
        """Replace page content by appending new blocks.

        Note: Notion API doesn't have a "replace all" — we delete existing
        blocks then append new ones.
        """
        try:
            existing = self.get_page_blocks(page_id)
            for block in existing:
                try:
                    self._client.blocks.delete(block_id=block["id"])
                except Exception:
                    pass  # Some blocks may not be deletable

            if children:
                self._client.blocks.children.append(
                    block_id=page_id,
                    children=children,
                )
        except NotionError:
            raise
        except Exception as exc:
            raise NotionError(f"Failed to update page {page_id}: {exc}") from exc

    def get_page_title(self, page: dict) -> str:
        """Extract title from a page object."""
        props = page.get("properties", {})
        title_prop = props.get("title", props.get("Name", {}))
        if isinstance(title_prop, dict):
            title_arr = title_prop.get("title", [])
        elif isinstance(title_prop, list):
            title_arr = title_prop
        else:
            return ""
        return "".join(
            t.get("plain_text", "") for t in title_arr if isinstance(t, dict)
        )

    def get_page_last_edited(self, page: dict) -> str:
        """Extract last_edited_time from a page object (ISO-8601)."""
        return page.get("last_edited_time", "")
