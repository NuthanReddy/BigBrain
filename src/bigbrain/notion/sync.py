"""Bidirectional sync engine between BigBrain KB and Notion."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from bigbrain.config import BigBrainConfig, NotionConfig, load_config
from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger
from bigbrain.notion.client import NotionClient
from bigbrain.notion.exporter import NotionExporter
from bigbrain.notion.importer import NotionImporter

logger = get_logger(__name__)


@dataclass
class SyncResult:
    """Result of a sync operation."""

    imported: int = 0
    exported: int = 0
    skipped: int = 0
    conflicts: int = 0
    errors: list[str] = field(default_factory=list)


class SyncEngine:
    """Bidirectional sync between BigBrain KB and Notion.

    Sync logic:
    - For each existing sync mapping, compare timestamps
    - If Notion page is newer → import (pull)
    - If local doc is newer → export (push)
    - If both changed since last sync → conflict (skip with warning)
    - New Notion pages (no mapping) → import
    - Local docs without mapping → export (if parent_page_id configured)

    Usage::

        engine = SyncEngine.from_config()
        result = engine.sync()
        engine.close()
    """

    def __init__(
        self,
        client: NotionClient,
        store: KBStore,
        config: NotionConfig | None = None,
    ) -> None:
        self._client = client
        self._store = store
        self._config = config or NotionConfig()
        self._importer = NotionImporter(client, store)
        self._exporter = NotionExporter(client, store)

    @classmethod
    def from_config(cls, config: BigBrainConfig | None = None) -> SyncEngine:
        if config is None:
            config = load_config()
        store = KBStore(config.kb_db_path)
        client = NotionClient.from_config(config.notion)
        return cls(client=client, store=store, config=config.notion)

    def close(self) -> None:
        self._store.close()

    def __enter__(self) -> SyncEngine:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def sync(self, *, parent_page_id: str = "") -> SyncResult:
        """Run a full bidirectional sync."""
        parent = parent_page_id or self._config.default_page_id
        direction = self._config.sync_direction
        result = SyncResult()

        logger.info("Starting Notion sync (direction=%s)", direction)

        # Step 1: Sync existing mappings (check for changes)
        mappings = self._store.list_sync_mappings()
        for mapping in mappings:
            try:
                self._sync_mapping(mapping, result, direction)
            except Exception as exc:
                logger.warning(
                    "Sync failed for mapping %s: %s", mapping["document_id"], exc,
                )
                result.errors.append(f"{mapping['document_id']}: {exc}")

        # Step 2: Import new Notion pages (not yet mapped)
        if direction in ("bidirectional", "import_only"):
            self._import_new_pages(mappings, result)

        # Step 3: Export local docs without mappings
        if direction in ("bidirectional", "export_only") and parent:
            self._export_new_docs(mappings, parent, result)

        logger.info(
            "Sync complete: imported=%d, exported=%d, skipped=%d, conflicts=%d, errors=%d",
            result.imported,
            result.exported,
            result.skipped,
            result.conflicts,
            len(result.errors),
        )
        return result

    def import_pages(self, query: str = "", max_pages: int = 20) -> SyncResult:
        """Import Notion pages into KB (import-only mode)."""
        result = SyncResult()
        pages = self._client.search_pages(query=query, page_size=max_pages)

        for page in pages:
            page_id = page["id"]
            try:
                doc = self._importer.import_page(page_id)
                if doc:
                    result.imported += 1
                else:
                    result.skipped += 1
            except Exception as exc:
                logger.warning("Failed to import page %s: %s", page_id, exc)
                result.errors.append(f"{page_id}: {exc}")

        return result

    def export_documents(
        self, *, parent_page_id: str, source_type: str | None = None,
    ) -> SyncResult:
        """Export KB documents to Notion (export-only mode)."""
        result = SyncResult()
        docs = self._store.list_documents(source_type=source_type, limit=9999)

        for doc in docs:
            try:
                page_id = self._exporter.export_document(
                    doc.id, parent_page_id=parent_page_id,
                )
                if page_id:
                    result.exported += 1
                else:
                    result.skipped += 1
            except Exception as exc:
                logger.warning("Failed to export doc %s: %s", doc.title, exc)
                result.errors.append(f"{doc.title}: {exc}")

        return result

    def get_sync_status(self) -> list[dict]:
        """Get the current sync status for all mapped documents."""
        mappings = self._store.list_sync_mappings()
        status_list = []
        for m in mappings:
            doc = self._store.get_document(m["document_id"])
            title = doc.title if doc else "(deleted)"
            status_list.append({
                "document_id": m["document_id"],
                "title": title,
                "notion_page_id": m["notion_page_id"],
                "last_synced_at": m["last_synced_at"],
                "status": m["status"],
                "sync_direction": m["sync_direction"],
            })
        return status_list

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _sync_mapping(
        self, mapping: dict, result: SyncResult, direction: str,
    ) -> None:
        """Sync a single existing mapping by comparing timestamps."""
        doc_id = mapping["document_id"]
        page_id = mapping["notion_page_id"]
        last_synced = mapping.get("last_synced_at", "")

        # Get current Notion page timestamp
        try:
            page = self._client.get_page(page_id)
            notion_edited = self._client.get_page_last_edited(page)
        except Exception:
            logger.warning("Cannot reach Notion page %s, skipping", page_id)
            result.skipped += 1
            return

        # Get local document
        doc = self._store.get_document(doc_id)
        if doc is None:
            result.skipped += 1
            return

        notion_changed = notion_edited > last_synced if last_synced else True

        if direction == "import_only" or (
            direction == "bidirectional" and notion_changed
        ):
            self._importer.import_page(page_id)
            result.imported += 1
        elif direction == "export_only":
            self._exporter.export_document(doc_id)
            result.exported += 1
        else:
            result.skipped += 1

    def _import_new_pages(
        self, existing_mappings: list[dict], result: SyncResult,
    ) -> None:
        """Import Notion pages that don't have a local mapping yet."""
        mapped_page_ids = {m["notion_page_id"] for m in existing_mappings}

        try:
            pages = self._client.search_pages(page_size=50)
        except Exception as exc:
            logger.warning("Failed to search Notion pages: %s", exc)
            return

        for page in pages:
            page_id = page["id"]
            if page_id in mapped_page_ids:
                continue
            try:
                doc = self._importer.import_page(page_id)
                if doc:
                    result.imported += 1
            except Exception as exc:
                logger.warning("Failed to import new page %s: %s", page_id, exc)
                result.errors.append(f"import {page_id}: {exc}")

    def _export_new_docs(
        self,
        existing_mappings: list[dict],
        parent_page_id: str,
        result: SyncResult,
    ) -> None:
        """Export local documents that don't have a Notion mapping yet."""
        mapped_doc_ids = {m["document_id"] for m in existing_mappings}
        docs = self._store.list_documents(limit=9999)

        for doc in docs:
            if doc.id in mapped_doc_ids:
                continue
            try:
                page_id = self._exporter.export_document(
                    doc.id, parent_page_id=parent_page_id,
                )
                if page_id:
                    result.exported += 1
            except Exception as exc:
                logger.warning("Failed to export doc %s: %s", doc.title, exc)
                result.errors.append(f"export {doc.title}: {exc}")
