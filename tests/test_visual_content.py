"""Tests for visual content features: Mermaid diagrams, rich Notion blocks, OCR image import.

Covers:
- Diagram generation (flowchart, class diagram, mindmap, ER diagram, safe IDs)
- Rich Notion block builders (code, callout, toggle, table, equation)
- OCR image handling in Notion importer
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from bigbrain.compile.diagrams import (
    _safe_mermaid_id,
    generate_class_diagram,
    generate_entity_relationship_diagram,
    generate_flowchart,
    generate_mindmap,
)
from bigbrain.distill.models import Entity, Relationship
from bigbrain.notion.exporter import (
    _callout,
    _code_block,
    _equation,
    _table,
    _table_row,
    _toggle,
)
from bigbrain.notion.importer import NotionImporter


# ── Helper data ──────────────────────────────────────────────────────


def _make_entities() -> list[Entity]:
    return [
        Entity(
            id="ent-aaa-111",
            document_id="doc-1",
            name="BST",
            entity_type="data_structure",
            description="Binary search tree",
        ),
        Entity(
            id="ent-bbb-222",
            document_id="doc-1",
            name="Quicksort",
            entity_type="algorithm",
            description="Divide and conquer sort",
        ),
        Entity(
            id="ent-ccc-333",
            document_id="doc-1",
            name="Graph Theory",
            entity_type="concept",
            description="Study of graphs",
        ),
    ]


def _make_relationships(entities: list[Entity]) -> list[Relationship]:
    return [
        Relationship(
            source_entity_id=entities[0].id,
            target_entity_id=entities[1].id,
            relationship_type="related_to",
            description="Both use comparison",
            document_id="doc-1",
        ),
        Relationship(
            source_entity_id=entities[2].id,
            target_entity_id=entities[0].id,
            relationship_type="uses",
            description="Graph uses trees",
            document_id="doc-1",
        ),
    ]


# =====================================================================
# 1. TestDiagrams
# =====================================================================


class TestDiagrams:
    """Tests for Mermaid diagram generation in compile.diagrams."""

    def test_generate_flowchart(self):
        entities = _make_entities()
        rels = _make_relationships(entities)
        result = generate_flowchart(entities, rels)

        assert result.startswith("flowchart LR")
        assert "BST" in result
        assert "Quicksort" in result
        assert "Graph Theory" in result
        assert "related to" in result

    def test_generate_flowchart_empty(self):
        result = generate_flowchart([], [])
        assert result.strip() == "flowchart LR"

    def test_generate_flowchart_shapes_by_type(self):
        entities = _make_entities()
        rels = _make_relationships(entities)
        result = generate_flowchart(entities, rels)
        lines = result.split("\n")

        algo_lines = [l for l in lines if "Quicksort" in l]
        assert any("([" in l for l in algo_lines), "algorithm should use stadium shape"

        ds_lines = [l for l in lines if "BST" in l]
        assert any("[[" in l for l in ds_lines), "data_structure should use subroutine shape"

    def test_generate_class_diagram(self):
        entities = _make_entities()
        result = generate_class_diagram(entities)

        assert result.startswith("classDiagram")
        assert "Algorithm" in result
        assert "DataStructure" in result
        assert "Concept" in result
        assert "+BST" in result
        assert "+Quicksort" in result
        assert "+Graph Theory" in result

    def test_generate_class_diagram_empty(self):
        result = generate_class_diagram([])
        assert result.strip() == "classDiagram"

    def test_generate_mindmap(self):
        entities = _make_entities()
        result = generate_mindmap(entities, root_title="CS Knowledge")

        assert result.startswith("mindmap")
        assert "CS Knowledge" in result
        assert "Algorithm" in result
        assert "Data Structure" in result
        assert "BST" in result
        assert "Quicksort" in result

    def test_generate_mindmap_custom_root(self):
        entities = _make_entities()
        result = generate_mindmap(entities, root_title="My Study")
        assert "My Study" in result

    def test_generate_entity_relationship_diagram(self):
        entities = _make_entities()
        rels = _make_relationships(entities)
        result = generate_entity_relationship_diagram(entities, rels)

        assert result.startswith("graph TD")
        assert "BST" in result
        assert "Quicksort" in result
        assert "related to" in result
        assert "uses" in result

    def test_generate_entity_relationship_diagram_empty(self):
        result = generate_entity_relationship_diagram([], [])
        assert result.strip() == "graph TD"

    def test_generate_entity_relationship_diagram_skips_orphan_edges(self):
        entities = _make_entities()[:1]  # only BST
        rels = _make_relationships(_make_entities())  # refs to ent-bbb, ent-ccc
        result = generate_entity_relationship_diagram(entities, rels)

        assert "BST" in result
        # Edges referencing missing entities should be excluded
        assert "-->" not in result

    def test_safe_mermaid_id(self):
        assert _safe_mermaid_id("abc-def-123-456") == "nabcdef123456"
        assert _safe_mermaid_id("a-b-c") == "nabc"

    def test_safe_mermaid_id_uuid(self):
        uuid_str = "550e8400-e29b-41d4-a716-446655440000"
        safe = _safe_mermaid_id(uuid_str)
        assert safe.startswith("n")
        assert "-" not in safe
        assert len(safe) <= 13  # "n" + up to 12 chars

    def test_generate_flowchart_max_nodes(self):
        entities = [
            Entity(id=f"e-{i}", document_id="d", name=f"Ent{i}", entity_type="concept")
            for i in range(50)
        ]
        result = generate_flowchart(entities, [], max_nodes=5)
        lines = [l for l in result.split("\n") if l.strip() and l.strip() != "flowchart LR"]
        assert len(lines) <= 5


# =====================================================================
# 2. TestRichNotionBlocks
# =====================================================================


class TestRichNotionBlocks:
    """Tests for rich Notion block builders in notion.exporter."""

    def test_code_block(self):
        block = _code_block("flowchart LR\n  A --> B", language="mermaid")
        assert block["type"] == "code"
        assert block["object"] == "block"
        assert block["code"]["language"] == "mermaid"
        rt = block["code"]["rich_text"]
        assert len(rt) == 1
        assert "flowchart LR" in rt[0]["text"]["content"]

    def test_code_block_truncates_long_content(self):
        long_code = "x" * 3000
        block = _code_block(long_code)
        content = block["code"]["rich_text"][0]["text"]["content"]
        assert len(content) == 2000

    def test_callout(self):
        block = _callout("Key insight here", emoji="🔑")
        assert block["type"] == "callout"
        assert block["object"] == "block"
        assert block["callout"]["icon"]["type"] == "emoji"
        assert block["callout"]["icon"]["emoji"] == "🔑"
        rt = block["callout"]["rich_text"]
        assert rt[0]["text"]["content"] == "Key insight here"

    def test_callout_default_emoji(self):
        block = _callout("Default emoji callout")
        assert block["callout"]["icon"]["emoji"] == "💡"

    def test_toggle(self):
        child = {"object": "block", "type": "paragraph", "paragraph": {"rich_text": []}}
        block = _toggle("Click to expand", children=[child])
        assert block["type"] == "toggle"
        assert block["object"] == "block"
        rt = block["toggle"]["rich_text"]
        assert rt[0]["text"]["content"] == "Click to expand"
        assert block["toggle"]["children"] == [child]

    def test_toggle_no_children(self):
        block = _toggle("No kids")
        assert block["type"] == "toggle"
        assert "children" not in block["toggle"]

    def test_table(self):
        rows = [["Name", "Type"], ["BST", "Data Structure"], ["Quicksort", "Algorithm"]]
        block = _table(rows, has_header=True)
        assert block["type"] == "table"
        assert block["object"] == "block"
        assert block["table"]["table_width"] == 2
        assert block["table"]["has_column_header"] is True
        assert block["table"]["has_row_header"] is False
        assert len(block["table"]["children"]) == 3

    def test_table_row(self):
        row = _table_row(["cell1", "cell2", "cell3"])
        assert row["type"] == "table_row"
        cells = row["table_row"]["cells"]
        assert len(cells) == 3
        assert cells[0][0]["text"]["content"] == "cell1"
        assert cells[2][0]["text"]["content"] == "cell3"

    def test_table_empty(self):
        block = _table([], has_header=True)
        assert block["type"] == "paragraph"
        assert "empty table" in block["paragraph"]["rich_text"][0]["text"]["content"]

    def test_equation(self):
        block = _equation(r"E = mc^{2}")
        assert block["type"] == "equation"
        assert block["object"] == "block"
        assert block["equation"]["expression"] == r"E = mc^{2}"

    def test_equation_complex(self):
        expr = r"\int_{0}^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}"
        block = _equation(expr)
        assert block["equation"]["expression"] == expr


# =====================================================================
# 3. TestOCRImporter
# =====================================================================


class TestOCRImporter:
    """Tests for OCR image handling in notion.importer."""

    def test_image_block_with_caption(self):
        importer = NotionImporter.__new__(NotionImporter)
        block = {
            "type": "image",
            "image": {
                "type": "external",
                "external": {"url": "https://example.com/img.png"},
                "caption": [{"plain_text": "Architecture diagram"}],
            },
        }
        with patch.object(NotionImporter, "_ocr_image", return_value=""):
            result = importer._block_to_text(block)
        assert "[Image: Architecture diagram]" in result

    def test_image_block_with_ocr_text(self):
        importer = NotionImporter.__new__(NotionImporter)
        block = {
            "type": "image",
            "image": {
                "type": "external",
                "external": {"url": "https://example.com/img.png"},
                "caption": [{"plain_text": "Formula"}],
            },
        }
        with patch.object(NotionImporter, "_ocr_image", return_value="E=mc2"):
            result = importer._block_to_text(block)
        assert "[Image: Formula]" in result
        assert "[OCR: E=mc2]" in result

    def test_image_block_no_url(self):
        importer = NotionImporter.__new__(NotionImporter)
        block = {
            "type": "image",
            "image": {
                "type": "external",
                "external": {"url": ""},
                "caption": [],
            },
        }
        result = importer._block_to_text(block)
        assert result == "[Image]"

    def test_image_block_no_url_with_caption(self):
        importer = NotionImporter.__new__(NotionImporter)
        block = {
            "type": "image",
            "image": {
                "type": "external",
                "external": {"url": ""},
                "caption": [{"plain_text": "My diagram"}],
            },
        }
        result = importer._block_to_text(block)
        assert result == "[Image: My diagram]"

    def test_image_block_ocr_fallback(self):
        """When pytesseract is not available, OCR returns empty and caption is used."""
        importer = NotionImporter.__new__(NotionImporter)
        block = {
            "type": "image",
            "image": {
                "type": "file",
                "file": {"url": "https://example.com/uploaded.png"},
                "caption": [{"plain_text": "Uploaded chart"}],
            },
        }
        with patch.object(NotionImporter, "_ocr_image", return_value=""):
            result = importer._block_to_text(block)
        assert "[Image: Uploaded chart]" in result
        assert "OCR" not in result

    @patch("httpx.get", side_effect=Exception("network error"))
    def test_ocr_image_graceful_failure(self, mock_get):
        """Network errors in OCR return empty string gracefully."""
        result = NotionImporter._ocr_image("https://example.com/img.png")
        assert result == ""

    def test_ocr_image_returns_empty_on_bad_url(self):
        result = NotionImporter._ocr_image("")
        assert result == ""

    @patch("httpx.get")
    def test_ocr_image_with_mock_image(self, mock_get):
        """Full OCR path with mocked httpx and PIL but no tesseract."""
        import io

        from PIL import Image

        # Create a tiny valid image in memory
        img = Image.new("RGB", (10, 10), color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        image_bytes = buf.getvalue()

        mock_resp = MagicMock()
        mock_resp.content = image_bytes
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        # pytesseract likely not installed in test env → should return ""
        result = NotionImporter._ocr_image("https://example.com/img.png")
        assert isinstance(result, str)

    def test_image_block_no_caption_no_ocr(self):
        """Image with URL but no caption and no OCR text returns [Image]."""
        importer = NotionImporter.__new__(NotionImporter)
        block = {
            "type": "image",
            "image": {
                "type": "external",
                "external": {"url": "https://example.com/img.png"},
                "caption": [],
            },
        }
        with patch.object(NotionImporter, "_ocr_image", return_value=""):
            result = importer._block_to_text(block)
        assert result == "[Image]"
