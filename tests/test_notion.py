"""Comprehensive tests for Phase 6 — Notion integration.

Covers NotionClient, NotionImporter, NotionExporter, SyncEngine,
KBStore sync-mapping methods, NotionConfig, and NotionError.

All Notion API calls are mocked — no real Notion connection needed.
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from bigbrain.config import BigBrainConfig, NotionConfig
from bigbrain.errors import NotionError, UserError
from bigbrain.kb.models import Document, DocumentSection, SourceMetadata
from bigbrain.kb.store import KBStore
from bigbrain.notion.client import NotionClient
from bigbrain.notion.exporter import NotionExporter
from bigbrain.notion.importer import NotionImporter
from bigbrain.notion.sync import SyncEngine, SyncResult


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

_MOCK_PAGE = {
    "id": "page-1",
    "object": "page",
    "properties": {
        "title": {"title": [{"plain_text": "Test Page"}]},
    },
    "last_edited_time": "2026-01-01T00:00:00.000Z",
    "url": "https://notion.so/page-1",
}

_MOCK_BLOCKS = [
    {
        "type": "heading_1",
        "heading_1": {"rich_text": [{"plain_text": "Introduction"}]},
    },
    {
        "type": "paragraph",
        "paragraph": {"rich_text": [{"plain_text": "This is test content."}]},
    },
    {
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"plain_text": "Item one"}]},
    },
]


def _mock_notion_client() -> tuple[NotionClient, MagicMock]:
    """Create a NotionClient with a fully mocked SDK."""
    with patch("notion_client.Client") as MockSDK:
        mock_sdk = MockSDK.return_value
        mock_sdk.users.me.return_value = {"id": "user-1", "name": "Test"}
        mock_sdk.search.return_value = {"results": [_MOCK_PAGE]}
        mock_sdk.pages.retrieve.return_value = _MOCK_PAGE
        mock_sdk.pages.create.return_value = {
            "id": "new-page-1",
            "url": "https://notion.so/new-page-1",
        }
        mock_sdk.blocks.children.list.return_value = {
            "results": _MOCK_BLOCKS,
            "has_more": False,
        }
        mock_sdk.blocks.children.append.return_value = {}
        mock_sdk.blocks.delete.return_value = {}

        client = NotionClient("ntn_test_token_1234567890")
        client._client = mock_sdk
        return client, mock_sdk


def _make_document(
    file_path: str = "test/sample.txt",
    title: str = "Test Doc",
    content: str = "Hello world",
) -> Document:
    return Document(
        title=title,
        content=content,
        source=SourceMetadata(
            file_path=file_path,
            file_extension=".txt",
            source_type="txt",
            size_bytes=len(content),
        ),
        language="",
        sections=[
            DocumentSection(title="Section 1", content="First section", level=1),
        ],
    )


# ===================================================================
# 1. TestNotionConfig
# ===================================================================

class TestNotionConfig:

    def test_default_values(self):
        cfg = NotionConfig()
        assert cfg.enabled is False
        assert cfg.token == ""
        assert cfg.default_page_id == ""
        assert cfg.sync_direction == "bidirectional"
        assert cfg.auto_create_pages is True

    def test_config_in_bigbrain_config(self):
        cfg = BigBrainConfig()
        assert isinstance(cfg.notion, NotionConfig)
        assert cfg.notion.enabled is False

    def test_env_var_override_for_token(self, monkeypatch):
        monkeypatch.setenv("BIGBRAIN_NOTION_TOKEN", "ntn_from_env_12345")
        cfg = NotionConfig(token="")
        # The token from the env is resolved at NotionClient.from_config time
        with patch("notion_client.Client"):
            client = NotionClient.from_config(cfg)
        assert client._token == "ntn_from_env_12345"


# ===================================================================
# 2. TestNotionClient
# ===================================================================

class TestNotionClient:

    def test_is_available_true(self):
        client, _ = _mock_notion_client()
        assert client.is_available() is True

    def test_is_available_false_on_exception(self):
        client, mock_sdk = _mock_notion_client()
        mock_sdk.users.me.side_effect = RuntimeError("Network error")
        assert client.is_available() is False

    def test_search_pages(self):
        client, _ = _mock_notion_client()
        pages = client.search_pages("test")
        assert len(pages) == 1
        assert pages[0]["id"] == "page-1"

    def test_get_page(self):
        client, _ = _mock_notion_client()
        page = client.get_page("page-1")
        assert page["id"] == "page-1"

    def test_get_page_blocks_handles_pagination(self):
        client, mock_sdk = _mock_notion_client()
        # First call returns has_more=True with a cursor
        mock_sdk.blocks.children.list.side_effect = [
            {
                "results": [_MOCK_BLOCKS[0]],
                "has_more": True,
                "next_cursor": "cursor-abc",
            },
            {
                "results": [_MOCK_BLOCKS[1], _MOCK_BLOCKS[2]],
                "has_more": False,
            },
        ]
        blocks = client.get_page_blocks("page-1")
        assert len(blocks) == 3
        assert mock_sdk.blocks.children.list.call_count == 2

    def test_get_page_title(self):
        client, _ = _mock_notion_client()
        title = client.get_page_title(_MOCK_PAGE)
        assert title == "Test Page"

    def test_create_page(self):
        client, mock_sdk = _mock_notion_client()
        result = client.create_page("parent-1", "New Page", children=[])
        assert result["id"] == "new-page-1"
        mock_sdk.pages.create.assert_called_once()

    def test_no_token_raises_notion_error(self):
        with patch("notion_client.Client"):
            with pytest.raises(NotionError, match="No Notion token"):
                NotionClient("")

    def test_search_pages_raises_on_sdk_error(self):
        client, mock_sdk = _mock_notion_client()
        mock_sdk.search.side_effect = RuntimeError("API 500")
        with pytest.raises(NotionError, match="Failed to search"):
            client.search_pages("test")

    def test_get_page_raises_on_sdk_error(self):
        client, mock_sdk = _mock_notion_client()
        mock_sdk.pages.retrieve.side_effect = RuntimeError("Not found")
        with pytest.raises(NotionError, match="Failed to get page"):
            client.get_page("bad-id")


# ===================================================================
# 3. TestNotionImporter
# ===================================================================

class TestNotionImporter:

    def test_import_page_creates_document(self, tmp_path: Path):
        client, _ = _mock_notion_client()
        store = KBStore(tmp_path / "kb.db")
        importer = NotionImporter(client, store)

        doc = importer.import_page("page-1")
        assert doc is not None
        assert doc.title == "Test Page"
        assert "Introduction" in doc.content
        assert "This is test content." in doc.content
        store.close()

    def test_imported_doc_has_correct_source_metadata(self, tmp_path: Path):
        client, _ = _mock_notion_client()
        store = KBStore(tmp_path / "kb.db")
        importer = NotionImporter(client, store)

        doc = importer.import_page("page-1")
        assert doc is not None
        assert doc.source is not None
        assert doc.source.file_path == "notion://page-1"
        assert doc.source.source_type == "notion"
        assert doc.source.file_extension == ".notion"
        assert doc.source.extra["notion_page_id"] == "page-1"
        store.close()

    def test_sync_mapping_saved_after_import(self, tmp_path: Path):
        client, _ = _mock_notion_client()
        store = KBStore(tmp_path / "kb.db")
        importer = NotionImporter(client, store)

        doc = importer.import_page("page-1")
        assert doc is not None

        # The importer should have saved a sync mapping
        doc_id = store.make_document_id("notion://page-1")
        mapping = store.get_sync_mapping(doc_id)
        assert mapping is not None
        assert mapping["notion_page_id"] == "page-1"
        assert mapping["sync_direction"] == "import"
        assert mapping["status"] == "synced"
        store.close()

    def test_import_search_imports_multiple_pages(self, tmp_path: Path):
        client, mock_sdk = _mock_notion_client()
        page2 = {
            **_MOCK_PAGE,
            "id": "page-2",
            "properties": {"title": {"title": [{"plain_text": "Page Two"}]}},
            "url": "https://notion.so/page-2",
        }
        mock_sdk.search.return_value = {"results": [_MOCK_PAGE, page2]}

        # get_page must respond for both page IDs
        def retrieve_side_effect(page_id):
            if page_id == "page-2":
                return page2
            return _MOCK_PAGE
        mock_sdk.pages.retrieve.side_effect = retrieve_side_effect

        store = KBStore(tmp_path / "kb.db")
        importer = NotionImporter(client, store)
        docs = importer.import_search("test", max_pages=10)
        assert len(docs) == 2
        titles = {d.title for d in docs}
        assert "Test Page" in titles
        assert "Page Two" in titles
        store.close()

    def test_block_conversion_handles_types(self, tmp_path: Path):
        client, mock_sdk = _mock_notion_client()
        mock_sdk.blocks.children.list.return_value = {
            "results": [
                {"type": "heading_2", "heading_2": {"rich_text": [{"plain_text": "Sub"}]}},
                {"type": "paragraph", "paragraph": {"rich_text": [{"plain_text": "Body text"}]}},
                {"type": "bulleted_list_item", "bulleted_list_item": {"rich_text": [{"plain_text": "Bullet"}]}},
                {"type": "numbered_list_item", "numbered_list_item": {"rich_text": [{"plain_text": "Numbered"}]}},
                {"type": "to_do", "to_do": {"rich_text": [{"plain_text": "Task"}], "checked": True}},
                {"type": "code", "code": {"rich_text": [{"plain_text": "x = 1"}], "language": "python"}},
                {"type": "quote", "quote": {"rich_text": [{"plain_text": "Famous words"}]}},
                {"type": "divider", "divider": {}},
            ],
            "has_more": False,
        }

        store = KBStore(tmp_path / "kb.db")
        importer = NotionImporter(client, store)
        doc = importer.import_page("page-1")
        assert doc is not None
        assert "Body text" in doc.content
        assert "• Bullet" in doc.content
        assert "• Numbered" in doc.content
        assert "✓ Task" in doc.content
        assert "```python" in doc.content
        assert "> Famous words" in doc.content
        assert "---" in doc.content
        store.close()

    def test_import_page_returns_none_on_fetch_failure(self, tmp_path: Path):
        client, mock_sdk = _mock_notion_client()
        mock_sdk.pages.retrieve.side_effect = RuntimeError("Not found")
        store = KBStore(tmp_path / "kb.db")
        importer = NotionImporter(client, store)
        result = importer.import_page("bad-id")
        assert result is None
        store.close()


# ===================================================================
# 4. TestNotionExporter
# ===================================================================

class TestNotionExporter:

    def _save_doc(self, store: KBStore) -> str:
        doc = _make_document()
        return store.save_document(doc)

    def test_export_creates_new_notion_page(self, tmp_path: Path):
        client, mock_sdk = _mock_notion_client()
        store = KBStore(tmp_path / "kb.db")
        doc_id = self._save_doc(store)

        exporter = NotionExporter(client, store)
        page_id = exporter.export_document(doc_id, parent_page_id="parent-1")
        assert page_id == "new-page-1"
        mock_sdk.pages.create.assert_called_once()
        store.close()

    def test_export_updates_existing_page_via_sync_mapping(self, tmp_path: Path):
        client, mock_sdk = _mock_notion_client()
        store = KBStore(tmp_path / "kb.db")
        doc_id = self._save_doc(store)

        # Pre-create a sync mapping
        store.save_sync_mapping(doc_id, "existing-page-1", sync_direction="export")

        exporter = NotionExporter(client, store)
        page_id = exporter.export_document(doc_id)
        assert page_id == "existing-page-1"
        # Should have called update (get_page_blocks + delete + append), not create
        mock_sdk.pages.create.assert_not_called()
        store.close()

    def test_export_includes_summaries_and_entities(self, tmp_path: Path):
        from bigbrain.distill.models import Entity, Summary

        client, mock_sdk = _mock_notion_client()
        store = KBStore(tmp_path / "kb.db")
        doc_id = self._save_doc(store)

        store.save_summaries([
            Summary(document_id=doc_id, content="A great summary."),
        ])
        store.save_entities([
            Entity(document_id=doc_id, name="Widget", entity_type="concept", description="A thing"),
        ])

        exporter = NotionExporter(client, store)
        page_id = exporter.export_document(doc_id, parent_page_id="parent-1")
        assert page_id is not None

        # Inspect the children blocks passed to pages.create
        call_kwargs = mock_sdk.pages.create.call_args
        children = call_kwargs.kwargs.get("children") or call_kwargs[1].get("children", [])
        # Flatten all text content from the children blocks
        all_text = _extract_all_text(children)
        assert "A great summary." in all_text
        assert "Widget" in all_text
        store.close()

    def test_export_returns_none_for_nonexistent_doc(self, tmp_path: Path):
        client, _ = _mock_notion_client()
        store = KBStore(tmp_path / "kb.db")
        exporter = NotionExporter(client, store)
        result = exporter.export_document("nonexistent-id", parent_page_id="parent-1")
        assert result is None
        store.close()

    def test_export_returns_none_without_parent_or_mapping(self, tmp_path: Path):
        client, _ = _mock_notion_client()
        store = KBStore(tmp_path / "kb.db")
        doc_id = self._save_doc(store)
        exporter = NotionExporter(client, store)
        # No parent_page_id and no sync mapping → should return None
        result = exporter.export_document(doc_id)
        assert result is None
        store.close()


# ===================================================================
# 5. TestSyncEngine
# ===================================================================

class TestSyncEngine:

    def test_sync_returns_sync_result(self, tmp_path: Path):
        client, mock_sdk = _mock_notion_client()
        store = KBStore(tmp_path / "kb.db")
        config = NotionConfig(
            sync_direction="bidirectional",
            default_page_id="parent-1",
        )

        engine = SyncEngine(client=client, store=store, config=config)
        result = engine.sync()
        assert isinstance(result, SyncResult)
        # Should have imported the one page from search
        assert result.imported >= 1
        engine.close()

    def test_import_pages(self, tmp_path: Path):
        client, _ = _mock_notion_client()
        store = KBStore(tmp_path / "kb.db")
        engine = SyncEngine(client=client, store=store)

        result = engine.import_pages(query="test", max_pages=5)
        assert isinstance(result, SyncResult)
        assert result.imported == 1
        engine.close()

    def test_export_documents(self, tmp_path: Path):
        client, mock_sdk = _mock_notion_client()
        store = KBStore(tmp_path / "kb.db")

        # Save a document to export
        doc = _make_document()
        store.save_document(doc)

        engine = SyncEngine(client=client, store=store)
        result = engine.export_documents(parent_page_id="parent-1")
        assert isinstance(result, SyncResult)
        assert result.exported == 1
        engine.close()

    def test_get_sync_status(self, tmp_path: Path):
        client, _ = _mock_notion_client()
        store = KBStore(tmp_path / "kb.db")

        # Save doc and a sync mapping
        doc = _make_document()
        doc_id = store.save_document(doc)
        store.save_sync_mapping(doc_id, "page-1", sync_direction="import", status="synced")

        engine = SyncEngine(client=client, store=store)
        status = engine.get_sync_status()
        assert len(status) == 1
        assert status[0]["document_id"] == doc_id
        assert status[0]["notion_page_id"] == "page-1"
        assert status[0]["title"] == "Test Doc"
        engine.close()

    def test_sync_result_defaults(self):
        result = SyncResult()
        assert result.imported == 0
        assert result.exported == 0
        assert result.skipped == 0
        assert result.conflicts == 0
        assert result.errors == []

    def test_context_manager(self, tmp_path: Path):
        client, _ = _mock_notion_client()
        store = KBStore(tmp_path / "kb.db")
        with SyncEngine(client=client, store=store) as engine:
            assert engine is not None


# ===================================================================
# 6. TestKBNotionSync — KBStore sync mapping CRUD
# ===================================================================

class TestKBNotionSync:

    @staticmethod
    def _save_stub_doc(store: KBStore, file_path: str) -> str:
        """Save a minimal document and return its ID (for FK satisfaction)."""
        doc = _make_document(file_path=file_path, title=f"Doc for {file_path}")
        return store.save_document(doc)

    def test_save_and_get_sync_mapping_roundtrip(self, tmp_path: Path):
        store = KBStore(tmp_path / "kb.db")
        doc_id = self._save_stub_doc(store, "sync/doc1.txt")
        store.save_sync_mapping(
            doc_id, "notion-1",
            sync_direction="import",
            notion_last_edited="2026-01-01T00:00:00Z",
            local_last_edited="2026-01-01T00:00:00Z",
            status="synced",
        )
        mapping = store.get_sync_mapping(doc_id)
        assert mapping is not None
        assert mapping["document_id"] == doc_id
        assert mapping["notion_page_id"] == "notion-1"
        assert mapping["sync_direction"] == "import"
        assert mapping["status"] == "synced"
        assert mapping["notion_last_edited"] == "2026-01-01T00:00:00Z"
        assert mapping["last_synced_at"] != ""
        store.close()

    def test_get_sync_by_notion_id(self, tmp_path: Path):
        store = KBStore(tmp_path / "kb.db")
        doc_id = self._save_stub_doc(store, "sync/doc2.txt")
        store.save_sync_mapping(doc_id, "notion-2", sync_direction="export")

        mapping = store.get_sync_by_notion_id("notion-2")
        assert mapping is not None
        assert mapping["document_id"] == doc_id
        assert mapping["notion_page_id"] == "notion-2"

        # Non-existent Notion ID returns None
        assert store.get_sync_by_notion_id("nonexistent") is None
        store.close()

    def test_list_sync_mappings(self, tmp_path: Path):
        store = KBStore(tmp_path / "kb.db")
        doc_a = self._save_stub_doc(store, "sync/a.txt")
        doc_b = self._save_stub_doc(store, "sync/b.txt")
        store.save_sync_mapping(doc_a, "notion-a", sync_direction="import")
        store.save_sync_mapping(doc_b, "notion-b", sync_direction="export")

        mappings = store.list_sync_mappings()
        assert len(mappings) == 2
        ids = {m["document_id"] for m in mappings}
        assert ids == {doc_a, doc_b}
        store.close()

    def test_delete_sync_mapping(self, tmp_path: Path):
        store = KBStore(tmp_path / "kb.db")
        doc_id = self._save_stub_doc(store, "sync/del.txt")
        store.save_sync_mapping(doc_id, "notion-x", sync_direction="import")
        assert store.get_sync_mapping(doc_id) is not None

        deleted = store.delete_sync_mapping(doc_id)
        assert deleted is True
        assert store.get_sync_mapping(doc_id) is None

        # Deleting again returns False
        assert store.delete_sync_mapping(doc_id) is False
        store.close()

    def test_upsert_sync_mapping(self, tmp_path: Path):
        store = KBStore(tmp_path / "kb.db")
        doc_id = self._save_stub_doc(store, "sync/upsert.txt")
        store.save_sync_mapping(doc_id, "notion-u", status="pending")
        mapping1 = store.get_sync_mapping(doc_id)
        assert mapping1 is not None
        assert mapping1["status"] == "pending"

        # Update the same mapping
        store.save_sync_mapping(doc_id, "notion-u", status="synced")
        mapping2 = store.get_sync_mapping(doc_id)
        assert mapping2 is not None
        assert mapping2["status"] == "synced"

        # Should still be only one mapping
        assert len(store.list_sync_mappings()) == 1
        store.close()


# ===================================================================
# 7. TestNotionError
# ===================================================================

class TestNotionError:

    def test_is_subclass_of_user_error(self):
        assert issubclass(NotionError, UserError)

    def test_error_message_formats_correctly(self):
        err = NotionError("Token expired for workspace")
        assert str(err) == "Token expired for workspace"
        assert isinstance(err, UserError)

    def test_notion_error_raised_and_caught(self):
        with pytest.raises(NotionError):
            raise NotionError("Something broke")


# ===================================================================
# Utility
# ===================================================================

def _extract_all_text(blocks: list[dict]) -> str:
    """Recursively extract all plain text from a list of Notion blocks."""
    parts: list[str] = []
    for block in blocks:
        btype = block.get("type", "")
        data = block.get(btype, {})
        if isinstance(data, dict):
            for rt in data.get("rich_text", []):
                parts.append(rt.get("text", {}).get("content", ""))
    return " ".join(parts)
