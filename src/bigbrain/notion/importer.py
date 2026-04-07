"""Notion page importer — imports Notion pages into the knowledge base."""

from __future__ import annotations

from typing import Any

from bigbrain.kb.models import Document, DocumentSection, SourceMetadata
from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger
from bigbrain.notion.client import NotionClient

logger = get_logger(__name__)


class NotionImporter:
    """Imports Notion pages into the knowledge base."""

    def __init__(self, client: NotionClient, store: KBStore) -> None:
        self._client = client
        self._store = store

    def import_page(self, page_id: str) -> Document | None:
        """Import a single Notion page into the KB.

        Returns the Document created/updated, or None on failure.
        """
        try:
            page = self._client.get_page(page_id)
            blocks = self._client.get_page_blocks(page_id)
        except Exception as exc:
            logger.error("Failed to fetch Notion page %s: %s", page_id, exc)
            return None

        title = self._client.get_page_title(page) or f"Notion Page {page_id[:8]}"
        last_edited = self._client.get_page_last_edited(page)

        sections, full_text = self._blocks_to_sections(blocks)

        source_path = f"notion://{page_id}"
        doc = Document(
            title=title,
            content=full_text,
            source=SourceMetadata(
                file_path=source_path,
                file_extension=".notion",
                source_type="notion",
                size_bytes=len(full_text.encode("utf-8")),
                extra={"notion_page_id": page_id, "notion_url": page.get("url", "")},
            ),
            language="",
            sections=sections,
            metadata={"notion_page_id": page_id, "notion_last_edited": last_edited},
        )

        doc_id = self._store.save_document(doc)

        self._store.save_sync_mapping(
            document_id=doc_id,
            notion_page_id=page_id,
            sync_direction="import",
            notion_last_edited=last_edited,
            local_last_edited=(
                doc.created_at.isoformat()
                if hasattr(doc.created_at, "isoformat")
                else str(doc.created_at)
            ),
            status="synced",
        )

        logger.info("Imported Notion page '%s' → doc %s", title, doc_id)
        return doc

    def import_search(self, query: str = "", max_pages: int = 20) -> list[Document]:
        """Import pages matching a search query."""
        pages = self._client.search_pages(query=query, page_size=max_pages)
        docs: list[Document] = []
        for page in pages:
            page_id = page["id"]
            doc = self.import_page(page_id)
            if doc:
                docs.append(doc)
        return docs

    # ------------------------------------------------------------------
    # Block → section/text conversion
    # ------------------------------------------------------------------

    def _blocks_to_sections(
        self, blocks: list[dict[str, Any]]
    ) -> tuple[list[DocumentSection], str]:
        """Convert Notion blocks to DocumentSections and full text.

        Returns (sections, full_text).
        """
        sections: list[DocumentSection] = []
        text_parts: list[str] = []
        current_section_title = ""
        current_section_lines: list[str] = []
        current_level = 0

        for block in blocks:
            btype = block.get("type", "")

            if btype in ("heading_1", "heading_2", "heading_3"):
                # Flush previous section
                if current_section_title or current_section_lines:
                    sections.append(
                        DocumentSection(
                            title=current_section_title,
                            content="\n".join(current_section_lines).strip(),
                            level=current_level,
                        )
                    )

                heading_text = self._extract_rich_text(
                    block.get(btype, {}).get("rich_text", [])
                )
                current_section_title = heading_text
                current_level = {"heading_1": 1, "heading_2": 2, "heading_3": 3}[btype]
                current_section_lines = []
                text_parts.append(f"\n{'#' * current_level} {heading_text}\n")
            else:
                line = self._block_to_text(block)
                if line:
                    current_section_lines.append(line)
                    text_parts.append(line)

        # Flush last section
        if current_section_title or current_section_lines:
            sections.append(
                DocumentSection(
                    title=current_section_title,
                    content="\n".join(current_section_lines).strip(),
                    level=current_level,
                )
            )

        return sections, "\n".join(text_parts).strip()

    def _block_to_text(self, block: dict[str, Any]) -> str:
        """Convert a single Notion block to plain text."""
        btype = block.get("type", "")
        data = block.get(btype, {})

        if btype == "paragraph":
            return self._extract_rich_text(data.get("rich_text", []))
        if btype in ("bulleted_list_item", "numbered_list_item"):
            text = self._extract_rich_text(data.get("rich_text", []))
            return f"• {text}" if text else ""
        if btype == "to_do":
            text = self._extract_rich_text(data.get("rich_text", []))
            checked = "✓" if data.get("checked") else "☐"
            return f"{checked} {text}" if text else ""
        if btype == "code":
            text = self._extract_rich_text(data.get("rich_text", []))
            lang = data.get("language", "")
            return f"```{lang}\n{text}\n```" if text else ""
        if btype == "quote":
            text = self._extract_rich_text(data.get("rich_text", []))
            return f"> {text}" if text else ""
        if btype == "callout":
            text = self._extract_rich_text(data.get("rich_text", []))
            return f"💡 {text}" if text else ""
        if btype == "divider":
            return "---"
        if btype == "toggle":
            return self._extract_rich_text(data.get("rich_text", []))
        if btype in ("heading_1", "heading_2", "heading_3"):
            text = self._extract_rich_text(data.get("rich_text", []))
            level = {"heading_1": 1, "heading_2": 2, "heading_3": 3}[btype]
            return f"{'#' * level} {text}"

        return ""

    @staticmethod
    def _extract_rich_text(rich_text: list[dict[str, Any]]) -> str:
        """Extract plain text from Notion rich text array."""
        return "".join(
            t.get("plain_text", "") for t in rich_text if isinstance(t, dict)
        )
