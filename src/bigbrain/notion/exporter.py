"""Notion page exporter — exports KB content to Notion pages."""

from __future__ import annotations

from typing import Any

from bigbrain.kb.models import Document
from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger
from bigbrain.notion.client import NotionClient

logger = get_logger(__name__)


class NotionExporter:
    """Exports KB documents and distilled content to Notion pages."""

    def __init__(self, client: NotionClient, store: KBStore) -> None:
        self._client = client
        self._store = store

    def export_document(
        self,
        doc_id: str,
        *,
        parent_page_id: str = "",
        include_summary: bool = True,
        include_entities: bool = True,
        include_relationships: bool = True,
    ) -> str | None:
        """Export a document to Notion as a parent page with child pages per chunk.

        Creates a top-level page with summary/overview, then a child page
        for each chunk with its entities and content.
        """
        doc = self._store.get_document(doc_id)
        if doc is None:
            logger.warning("Document not found: %s", doc_id)
            return None

        mapping = self._store.get_sync_mapping(doc_id)

        if mapping and mapping.get("notion_page_id"):
            notion_page_id = mapping["notion_page_id"]
            logger.info("Updating existing Notion page %s for %s", notion_page_id, doc.title)
            try:
                blocks = self._build_overview_blocks(doc, include_summary, include_entities, include_relationships)
                self._client.update_page_blocks(notion_page_id, blocks)
            except Exception as exc:
                logger.error("Failed to update Notion page %s: %s", notion_page_id, exc)
                return None
        else:
            if not parent_page_id:
                logger.error("No parent_page_id for %s", doc_id)
                return None

            # Create parent page with overview
            overview_blocks = self._build_overview_blocks(doc, include_summary, include_entities, include_relationships)
            try:
                first_batch = overview_blocks[:100]
                remaining = overview_blocks[100:]
                page = self._client.create_page(parent_page_id, doc.title, children=first_batch)
                notion_page_id = page["id"]
                while remaining:
                    batch = remaining[:100]
                    remaining = remaining[100:]
                    try:
                        self._client._client.blocks.children.append(
                            block_id=notion_page_id, children=batch,
                        )
                    except Exception:
                        break
                logger.info("Created parent page %s for %s", notion_page_id, doc.title)
            except Exception as exc:
                logger.error("Failed to create Notion page for %s: %s", doc.title, exc)
                return None

        # Create child pages per chunk (section-level content)
        chunks = self._store.get_chunks(doc_id)
        if chunks:
            entities_by_chunk: dict[str, list] = {}
            all_entities = self._store.get_entities(doc_id)
            for e in all_entities:
                if e.source_chunk_id:
                    entities_by_chunk.setdefault(e.source_chunk_id, []).append(e)

            for chunk in chunks:
                title = chunk.section_title or f"Section {chunk.chunk_index + 1}"
                try:
                    chunk_blocks = self._build_chunk_blocks(chunk, entities_by_chunk.get(chunk.id, []))
                    first_batch = chunk_blocks[:100]
                    remaining_blocks = chunk_blocks[100:]
                    child = self._client.create_page(notion_page_id, title, children=first_batch)
                    child_id = child["id"]
                    while remaining_blocks:
                        batch = remaining_blocks[:100]
                        remaining_blocks = remaining_blocks[100:]
                        try:
                            self._client._client.blocks.children.append(
                                block_id=child_id, children=batch,
                            )
                        except Exception:
                            break
                    logger.debug("Created child page '%s' under %s", title, doc.title)
                except Exception as exc:
                    logger.warning("Failed to create child page '%s': %s", title, exc)

        self._store.save_sync_mapping(
            document_id=doc_id,
            notion_page_id=notion_page_id,
            sync_direction="export",
            status="synced",
        )

        return notion_page_id

    def export_all(
        self,
        *,
        parent_page_id: str,
        source_type: str | None = None,
        include_summary: bool = True,
        include_entities: bool = True,
    ) -> list[str]:
        """Export all KB documents to Notion. Returns list of Notion page IDs."""
        docs = self._store.list_documents(source_type=source_type, limit=9999)
        page_ids: list[str] = []
        for doc in docs:
            pid = self.export_document(
                doc.id,
                parent_page_id=parent_page_id,
                include_summary=include_summary,
                include_entities=include_entities,
            )
            if pid:
                page_ids.append(pid)
        return page_ids

    def _build_overview_blocks(
        self,
        doc: Document,
        include_summary: bool,
        include_entities: bool,
        include_relationships: bool,
    ) -> list[dict]:
        """Build Notion block children from a document and its distilled content."""
        blocks: list[dict] = []

        # BigBrain export marker (used to skip during import)
        blocks.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "🧠"},
                "rich_text": [{"type": "text", "text": {"content": "Generated by BigBrain — auto-imported pages will skip this page."}}],
                "color": "gray_background",
            },
        })

        # Source info
        if doc.source:
            blocks.append(
                _paragraph(f"\U0001f4c4 Source: {doc.source.file_path} ({doc.source.source_type})")
            )
            blocks.append(_divider())

        # Summary
        if include_summary:
            summaries = self._store.get_summaries(doc.id)
            if summaries:
                blocks.append(_heading("Summary", level=2))
                for s in summaries:
                    for para in _split_text(s.content, max_len=1900):
                        blocks.append(_paragraph(para))

        # Entities grouped by type
        if include_entities:
            entities = self._store.get_entities(doc.id)
            if entities:
                blocks.append(_heading("Key Concepts", level=2))
                by_type: dict[str, list] = {}
                for e in entities:
                    by_type.setdefault(e.entity_type, []).append(e)

                for etype, ents in sorted(by_type.items()):
                    blocks.append(_heading(etype.replace("_", " ").title(), level=3))
                    for e in sorted(ents, key=lambda x: x.name)[:30]:
                        desc = f" — {e.description}" if e.description else ""
                        blocks.append(_bulleted(f"{e.name}{desc}"))

        # Relationships
        if include_relationships:
            relationships = self._store.get_relationships(doc.id)
            if relationships:
                entities = self._store.get_entities(doc.id)
                entity_map = {e.id: e.name for e in entities}
                blocks.append(_heading("Relationships", level=2))
                for r in relationships[:30]:
                    src = entity_map.get(r.source_entity_id, "?")
                    tgt = entity_map.get(r.target_entity_id, "?")
                    blocks.append(_bulleted(f"{src} \u2192 {r.relationship_type} \u2192 {tgt}"))

        return blocks

    @staticmethod
    def _build_chunk_blocks(chunk: Any, entities: list) -> list[dict]:
        """Build blocks for a chunk child page."""
        blocks: list[dict] = []

        # BigBrain marker
        blocks.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "🧠"},
                "rich_text": [{"type": "text", "text": {"content": "Generated by BigBrain — auto-imported pages will skip this page."}}],
                "color": "gray_background",
            },
        })

        # Chunk content as paragraphs
        content = getattr(chunk, "content", "") or ""
        if content:
            for para in _split_text(content, max_len=1900):
                blocks.append(_paragraph(para))

        # Entities from this chunk
        if entities:
            blocks.append(_divider())
            blocks.append(_heading("Key Concepts", level=2))
            for e in sorted(entities, key=lambda x: x.name):
                desc = f" — {e.description}" if e.description else ""
                details = ""
                if e.metadata:
                    d = e.metadata.get("details", "")
                    if d:
                        details = f"\n{d}"
                blocks.append(_bulleted(f"**{e.name}**{desc}"))
                if details:
                    for para in _split_text(details.strip(), max_len=1900):
                        blocks.append(_paragraph(para))

        return blocks


# ------------------------------------------------------------------
# Notion block builders
# ------------------------------------------------------------------


def _paragraph(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def _heading(text: str, level: int = 2) -> dict:
    htype = f"heading_{level}"
    return {
        "object": "block",
        "type": htype,
        htype: {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def _bulleted(text: str) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def _divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def _split_text(text: str, max_len: int = 1900) -> list[str]:
    """Split text into chunks that fit Notion's block size limit."""
    if len(text) <= max_len:
        return [text]
    parts: list[str] = []
    while text:
        if len(text) <= max_len:
            parts.append(text)
            break
        split = text.rfind("\n", 0, max_len)
        if split == -1:
            split = text.rfind(" ", 0, max_len)
        if split == -1:
            split = max_len
        parts.append(text[:split])
        text = text[split:].lstrip()
    return parts


# ------------------------------------------------------------------
# Rich block builders
# ------------------------------------------------------------------


def _code_block(code: str, language: str = "mermaid") -> dict:
    """Create a code block (for Mermaid diagrams, etc.)."""
    return {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [{"type": "text", "text": {"content": code[:2000]}}],
            "language": language,
        },
    }


def _callout(text: str, emoji: str = "\U0001f4a1") -> dict:
    """Create a callout block for key concepts."""
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": text[:2000]}}],
            "icon": {"type": "emoji", "emoji": emoji},
        },
    }


def _toggle(title: str, children: list[dict] | None = None) -> dict:
    """Create a toggle block (expandable section)."""
    block: dict = {
        "object": "block",
        "type": "toggle",
        "toggle": {
            "rich_text": [{"type": "text", "text": {"content": title[:2000]}}],
        },
    }
    if children:
        block["toggle"]["children"] = children[:100]
    return block


def _table_row(cells: list[str]) -> dict:
    """Create a table row."""
    return {
        "type": "table_row",
        "table_row": {
            "cells": [[{"type": "text", "text": {"content": c[:2000]}}] for c in cells],
        },
    }


def _table(rows: list[list[str]], has_header: bool = True) -> dict:
    """Create a table block with rows."""
    if not rows:
        return _paragraph("(empty table)")
    width = len(rows[0])
    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": width,
            "has_column_header": has_header,
            "has_row_header": False,
            "children": [_table_row(row) for row in rows],
        },
    }


def _equation(expression: str) -> dict:
    """Create an equation block (KaTeX)."""
    return {
        "object": "block",
        "type": "equation",
        "equation": {"expression": expression},
    }
