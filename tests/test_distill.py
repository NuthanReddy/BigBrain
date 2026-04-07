"""Comprehensive tests for Phase 4 distillation pipeline.

Covers: models, chunker, summarizer, entity extractor, relationship builder,
pipeline orchestration, DistillConfig, and KB schema v2 round-trips.

All AI calls are mocked — no real LLM server needed.
"""

from __future__ import annotations

import os
import uuid
from typing import Any
from unittest.mock import patch

import pytest

from bigbrain.config import BigBrainConfig, DistillConfig, load_config
from bigbrain.distill.chunker import (
    chunk_by_paragraph,
    chunk_by_section,
    chunk_document,
    chunk_sliding_window,
)
from bigbrain.distill.entities import EntityExtractor, _parse_json_response
from bigbrain.distill.models import Chunk, DistillResult, Entity, Relationship, Summary
from bigbrain.distill.pipeline import DistillPipeline
from bigbrain.distill.relationships import RelationshipBuilder
from bigbrain.distill.summarizer import Summarizer
from bigbrain.kb.models import Document, DocumentSection, SourceMetadata
from bigbrain.kb.store import KBStore
from bigbrain.providers.base import BaseProvider, ProviderResponse
from bigbrain.providers.registry import ProviderRegistry

# ── Mock provider ────────────────────────────────────────────────────


class MockDistillProvider(BaseProvider):
    """Deterministic mock provider for distill tests."""

    @property
    def name(self) -> str:
        return "mock"

    def is_available(self) -> bool:
        return True

    def complete(self, prompt: str, *, model: str = "", **kwargs: Any) -> ProviderResponse:
        return ProviderResponse(text="Mock summary", provider="mock", model="mock-1")

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str = "",
        **kwargs: Any,
    ) -> ProviderResponse:
        last = messages[-1]["content"] if messages else ""
        # Entity extraction prompt
        if "Extract" in last and "entities" in last.lower():
            return ProviderResponse(
                text=(
                    '[{"name": "Binary Search", "type": "algorithm",'
                    ' "description": "Efficient search on sorted array"},'
                    ' {"name": "Array", "type": "data_structure",'
                    ' "description": "Contiguous memory block"}]'
                ),
                provider="mock",
                model="mock-1",
            )
        # Relationship extraction prompt
        if "relationships" in last.lower() and "source" in last.lower():
            return ProviderResponse(
                text=(
                    '[{"source": "binary search", "target": "array",'
                    ' "type": "uses",'
                    ' "description": "Binary search operates on sorted arrays"}]'
                ),
                provider="mock",
                model="mock-1",
            )
        # Default: summary
        return ProviderResponse(
            text="This is a mock summary of the content.",
            provider="mock",
            model="mock-1",
        )


# ── Helpers ──────────────────────────────────────────────────────────


def _make_doc(sections: bool = True) -> Document:
    """Create a test document with optional sections."""
    doc = Document(
        title="Test Algorithms",
        content=(
            "Binary search is an efficient algorithm for finding items in sorted arrays. "
            "It works by repeatedly dividing the search interval in half. "
            "Quicksort is a divide-and-conquer sorting algorithm."
        ),
        source=SourceMetadata(
            file_path="algo.txt",
            file_extension=".txt",
            source_type="txt",
            size_bytes=200,
        ),
    )
    if sections:
        doc.sections = [
            DocumentSection(
                title="Binary Search",
                content=(
                    "Binary search is an efficient algorithm for finding items "
                    "in sorted arrays. It works by repeatedly dividing the search "
                    "interval in half until the target is found or the interval is empty."
                ),
                level=1,
            ),
            DocumentSection(
                title="Quicksort",
                content=(
                    "Quicksort is a divide-and-conquer sorting algorithm. It picks "
                    "a pivot and partitions the array. Average case O(n log n), "
                    "worst case O(n^2)."
                ),
                level=1,
            ),
        ]
    return doc


def _make_registry() -> ProviderRegistry:
    registry = ProviderRegistry()
    registry.register(MockDistillProvider())
    return registry


def _make_pipeline(tmp_path) -> DistillPipeline:
    store = KBStore(tmp_path / "test.db")
    registry = _make_registry()
    return DistillPipeline(store=store, registry=registry)


# =====================================================================
# 1. TestDistillModels
# =====================================================================


class TestDistillModels:
    """Verify dataclass defaults, UUID generation, and field types."""

    def test_chunk_defaults(self):
        c = Chunk()
        assert c.content == ""
        assert c.document_id == ""
        assert c.start_offset == 0
        assert c.end_offset == 0
        assert c.section_title == ""
        assert c.chunk_index == 0
        assert c.metadata == {}
        # id should be a valid UUID
        uuid.UUID(c.id)

    def test_summary_defaults(self):
        s = Summary()
        assert s.content == ""
        assert s.document_id == ""
        assert s.chunk_id == ""
        assert s.summary_type == "document"
        assert s.generated_by_provider == ""
        assert s.created_at is not None
        uuid.UUID(s.id)

    def test_entity_defaults(self):
        e = Entity()
        assert e.name == ""
        assert e.entity_type == ""
        assert e.description == ""
        assert e.source_chunk_id == ""
        uuid.UUID(e.id)

    def test_relationship_defaults(self):
        r = Relationship()
        assert r.source_entity_id == ""
        assert r.target_entity_id == ""
        assert r.relationship_type == ""
        assert r.confidence == 1.0
        uuid.UUID(r.id)

    def test_distill_result_defaults(self):
        dr = DistillResult()
        assert dr.document_id == ""
        assert dr.chunks == []
        assert dr.summaries == []
        assert dr.entities == []
        assert dr.relationships == []
        assert dr.errors == []

    def test_unique_ids_per_instance(self):
        """Each new model gets a distinct UUID."""
        ids = {Chunk().id, Summary().id, Entity().id, Relationship().id}
        assert len(ids) == 4


# =====================================================================
# 2. TestChunker
# =====================================================================


class TestChunker:
    """Test all chunking strategies and the main dispatcher."""

    def test_chunk_by_section_two_sections(self):
        doc = _make_doc(sections=True)
        chunks = chunk_by_section(doc)
        assert len(chunks) == 2
        assert chunks[0].section_title == "Binary Search"
        assert chunks[1].section_title == "Quicksort"
        assert chunks[0].chunk_index == 0
        assert chunks[1].chunk_index == 1
        assert all(c.document_id == doc.id for c in chunks)

    def test_chunk_by_section_merges_short(self):
        doc = _make_doc(sections=False)
        doc.sections = [
            DocumentSection(title="Short", content="hi", level=1),
            DocumentSection(title="Long", content="x" * 100, level=1),
        ]
        chunks = chunk_by_section(doc, min_length=50)
        # "hi" is <50 chars → merged with next section
        assert len(chunks) == 1
        assert "hi" in chunks[0].content
        assert "x" * 100 in chunks[0].content

    def test_chunk_by_section_no_sections_fallback(self):
        doc = _make_doc(sections=False)
        doc.sections = []
        chunks = chunk_by_section(doc)
        # Fallback to by_paragraph — at least 1 chunk from content
        assert len(chunks) >= 1

    def test_chunk_sliding_window(self):
        doc = _make_doc()
        chunks = chunk_sliding_window(doc, chunk_size=50, overlap=10)
        assert len(chunks) >= 2
        # Overlapping: second chunk starts before end of first
        if len(chunks) >= 2:
            assert chunks[1].start_offset < chunks[0].end_offset

    def test_chunk_sliding_window_size(self):
        doc = _make_doc()
        chunks = chunk_sliding_window(doc, chunk_size=80, overlap=20)
        for c in chunks:
            assert len(c.content) <= 80

    def test_chunk_by_paragraph(self):
        doc = Document(
            title="Paragraphs",
            content="Paragraph one is sufficiently long to exceed the minimum length.\n\nParagraph two is also long enough to satisfy the minimum length requirement.",
            source=SourceMetadata(
                file_path="p.txt", file_extension=".txt", source_type="txt", size_bytes=100,
            ),
        )
        chunks = chunk_by_paragraph(doc, min_length=10)
        assert len(chunks) == 2

    def test_chunk_document_dispatch(self):
        doc = _make_doc()
        # by_section
        c1 = chunk_document(doc, strategy="by_section")
        assert len(c1) == 2
        # sliding_window
        c2 = chunk_document(doc, strategy="sliding_window", chunk_size=60, overlap=10)
        assert len(c2) >= 2
        # by_paragraph
        c3 = chunk_document(doc, strategy="by_paragraph")
        assert len(c3) >= 1

    def test_chunk_document_max_chunks(self):
        doc = _make_doc()
        chunks = chunk_document(
            doc, strategy="sliding_window", chunk_size=20, overlap=5, max_chunks=2,
        )
        assert len(chunks) <= 2


# =====================================================================
# 3. TestSummarizer
# =====================================================================


class TestSummarizer:
    """Test AI-powered summarizer with MockDistillProvider."""

    def test_summarize_document(self):
        registry = _make_registry()
        summarizer = Summarizer(registry)
        doc = _make_doc()
        result = summarizer.summarize_document(doc)
        assert isinstance(result, Summary)
        assert result.content == "This is a mock summary of the content."
        assert result.generated_by_provider == "mock"
        assert result.generated_by_model == "mock-1"
        assert result.summary_type == "document"
        assert result.document_id == doc.id

    def test_summarize_chunk(self):
        registry = _make_registry()
        summarizer = Summarizer(registry)
        chunk = Chunk(document_id="doc-1", content="Some content here.")
        result = summarizer.summarize_chunk(chunk)
        assert isinstance(result, Summary)
        assert result.summary_type == "chunk"
        assert result.chunk_id == chunk.id
        assert result.document_id == "doc-1"

    def test_summarize_chunks_batch(self):
        registry = _make_registry()
        summarizer = Summarizer(registry)
        chunks = [
            Chunk(document_id="doc-1", content="Chunk one."),
            Chunk(document_id="doc-1", content="Chunk two."),
        ]
        results = summarizer.summarize_chunks(chunks)
        assert len(results) == 2
        assert all(isinstance(s, Summary) for s in results)


# =====================================================================
# 4. TestEntityExtractor
# =====================================================================


class TestEntityExtractor:
    """Test AI-powered entity extraction with MockDistillProvider."""

    def test_extract_from_chunk(self):
        registry = _make_registry()
        extractor = EntityExtractor(registry)
        chunk = Chunk(
            document_id="doc-1",
            content="Extract the key entities from this text about algorithms.",
        )
        entities = extractor.extract_from_chunk(chunk)
        assert len(entities) == 2
        names = {e.name for e in entities}
        assert "Binary Search" in names
        assert "Array" in names
        for e in entities:
            assert e.document_id == "doc-1"
            assert e.source_chunk_id == chunk.id
            assert e.generated_by_provider == "mock"

    def test_extract_from_chunks_deduplicates(self):
        registry = _make_registry()
        extractor = EntityExtractor(registry)
        chunks = [
            Chunk(
                document_id="doc-1",
                content="Extract the key entities from chunk 1.",
            ),
            Chunk(
                document_id="doc-1",
                content="Extract more entities from chunk 2.",
            ),
        ]
        entities = extractor.extract_from_chunks(chunks)
        # Both chunks return the same entity names; dedup keeps only one of each
        names = [e.name for e in entities]
        assert names.count("Binary Search") == 1
        assert names.count("Array") == 1

    def test_parse_json_response_markdown(self):
        raw = '```json\n[{"name": "X", "type": "concept"}]\n```'
        result = _parse_json_response(raw)
        assert len(result) == 1
        assert result[0]["name"] == "X"

    def test_parse_json_response_invalid(self):
        result = _parse_json_response("not json at all")
        assert result == []


# =====================================================================
# 5. TestRelationshipBuilder
# =====================================================================


class TestRelationshipBuilder:
    """Test AI-powered relationship building with MockDistillProvider."""

    def _make_entities(self) -> list[Entity]:
        return [
            Entity(name="Binary Search", entity_type="algorithm", description="Search algo"),
            Entity(name="Array", entity_type="data_structure", description="Data struct"),
        ]

    def test_build_relationships(self):
        registry = _make_registry()
        builder = RelationshipBuilder(registry)
        entities = self._make_entities()
        rels = builder.build_relationships(entities, document_id="doc-1")
        assert len(rels) >= 1
        r = rels[0]
        assert r.relationship_type == "uses"
        assert r.document_id == "doc-1"
        assert r.generated_by_provider == "mock"

    def test_build_relationships_too_few_entities(self):
        registry = _make_registry()
        builder = RelationshipBuilder(registry)
        rels = builder.build_relationships([Entity(name="Lonely")])
        assert rels == []

    def test_build_relationships_filters_unknown(self):
        """Relationships referencing entities not in the list are skipped."""
        registry = ProviderRegistry()

        class UnknownEntityProvider(BaseProvider):
            @property
            def name(self) -> str:
                return "unknown_entity"

            def is_available(self) -> bool:
                return True

            def complete(self, prompt, *, model="", **kw):
                return ProviderResponse(text="", provider="test", model="t")

            def chat(self, messages, *, model="", **kw):
                return ProviderResponse(
                    text=(
                        '[{"source": "binary search", "target": "linked list",'
                        ' "type": "uses", "description": "nope"}]'
                    ),
                    provider="test",
                    model="t",
                )

        registry.register(UnknownEntityProvider())
        builder = RelationshipBuilder(registry)
        entities = self._make_entities()
        rels = builder.build_relationships(entities)
        # "linked list" is not in the entity list, so filtered out
        assert rels == []


# =====================================================================
# 6. TestDistillPipeline
# =====================================================================


class TestDistillPipeline:
    """Test the full distillation pipeline orchestration."""

    def test_distill_document_full(self, tmp_path):
        pipeline = _make_pipeline(tmp_path)
        doc = _make_doc()
        # save_document returns a deterministic ID; sync it to doc.id
        doc_id = pipeline._store.save_document(doc)
        doc.id = doc_id
        result = pipeline.distill_document(doc)
        assert isinstance(result, DistillResult)
        assert result.document_id == doc.id
        assert len(result.chunks) >= 1
        assert len(result.summaries) >= 1
        assert len(result.entities) >= 1
        assert len(result.relationships) >= 1
        assert result.provider == "mock"
        assert result.model == "mock-1"
        assert result.errors == []
        pipeline.close()

    def test_distill_empty_document(self, tmp_path):
        pipeline = _make_pipeline(tmp_path)
        doc = Document(
            title="Empty",
            content="",
            source=SourceMetadata(
                file_path="empty.txt", file_extension=".txt",
                source_type="txt", size_bytes=0,
            ),
        )
        doc_id = pipeline._store.save_document(doc)
        doc.id = doc_id
        result = pipeline.distill_document(doc)
        assert result.chunks == []
        assert result.summaries == []
        pipeline.close()

    def test_distill_persists_to_kb(self, tmp_path):
        pipeline = _make_pipeline(tmp_path)
        doc = _make_doc()
        doc_id = pipeline._store.save_document(doc)
        doc.id = doc_id
        pipeline.distill_document(doc)

        # Verify data was persisted
        chunks = pipeline._store.get_chunks(doc_id)
        assert len(chunks) >= 1
        summaries = pipeline._store.get_summaries(doc_id)
        assert len(summaries) >= 1
        entities = pipeline._store.get_entities(doc_id)
        assert len(entities) >= 1
        relationships = pipeline._store.get_relationships(doc_id)
        assert len(relationships) >= 1
        pipeline.close()

    def test_distill_by_id(self, tmp_path):
        pipeline = _make_pipeline(tmp_path)
        doc = _make_doc()
        doc_id = pipeline._store.save_document(doc)
        result = pipeline.distill_by_id(doc_id)
        assert result is not None
        assert result.document_id == doc_id
        assert len(result.chunks) >= 1
        pipeline.close()

    def test_distill_by_id_not_found(self, tmp_path):
        pipeline = _make_pipeline(tmp_path)
        result = pipeline.distill_by_id("nonexistent-id")
        assert result is None
        pipeline.close()

    def test_distill_all(self, tmp_path):
        pipeline = _make_pipeline(tmp_path)
        doc1 = _make_doc()
        doc2 = Document(
            title="Second Doc",
            content="Some interesting content about data structures and algorithms.",
            source=SourceMetadata(
                file_path="second.txt", file_extension=".txt",
                source_type="txt", size_bytes=80,
            ),
        )
        doc1.id = pipeline._store.save_document(doc1)
        doc2.id = pipeline._store.save_document(doc2)
        results = pipeline.distill_all()
        assert len(results) == 2
        assert all(isinstance(r, DistillResult) for r in results)
        pipeline.close()

    def test_pipeline_context_manager(self, tmp_path):
        with _make_pipeline(tmp_path) as pipeline:
            doc = _make_doc()
            doc_id = pipeline._store.save_document(doc)
            doc.id = doc_id
            result = pipeline.distill_document(doc)
            assert len(result.chunks) >= 1


# =====================================================================
# 7. TestDistillConfig
# =====================================================================


class TestDistillConfig:
    """Test DistillConfig defaults, nesting, and env var overrides."""

    def test_default_values(self):
        cfg = DistillConfig()
        assert cfg.chunk_strategy == "by_section"
        assert cfg.chunk_size == 1000
        assert cfg.chunk_overlap == 200
        assert cfg.summary_max_length == 500
        assert cfg.entity_extraction is True
        assert cfg.relationship_extraction is True
        assert cfg.max_chunks_per_doc == 50

    def test_config_in_bigbrain_config(self):
        cfg = BigBrainConfig()
        assert isinstance(cfg.distillation, DistillConfig)
        assert cfg.distillation.chunk_strategy == "by_section"

    def test_distill_env_overrides(self, monkeypatch):
        monkeypatch.setenv("BIGBRAIN_DISTILL_CHUNK_SIZE", "2000")
        monkeypatch.setenv("BIGBRAIN_DISTILL_ENTITY_EXTRACTION", "false")
        monkeypatch.setenv("BIGBRAIN_DISTILL_CHUNK_STRATEGY", "sliding_window")
        cfg = load_config(config_path="nonexistent.yaml")
        assert cfg.distillation.chunk_size == 2000
        assert cfg.distillation.entity_extraction is False
        assert cfg.distillation.chunk_strategy == "sliding_window"


# =====================================================================
# 8. TestKBSchemaV2
# =====================================================================


class TestKBSchemaV2:
    """Verify round-trip persistence for Phase 4 KB tables."""

    def test_save_and_get_chunks(self, tmp_path):
        store = KBStore(tmp_path / "test.db")
        doc = _make_doc()
        doc_id = store.save_document(doc)
        chunks = [
            Chunk(document_id=doc_id, content="Chunk one", chunk_index=0, section_title="S1"),
            Chunk(document_id=doc_id, content="Chunk two", chunk_index=1, section_title="S2"),
        ]
        count = store.save_chunks(chunks)
        assert count == 2
        loaded = store.get_chunks(doc_id)
        assert len(loaded) == 2
        assert loaded[0].content == "Chunk one"
        assert loaded[1].content == "Chunk two"
        assert loaded[0].section_title == "S1"
        store.close()

    def test_save_and_get_summaries(self, tmp_path):
        store = KBStore(tmp_path / "test.db")
        doc = _make_doc()
        doc_id = store.save_document(doc)
        summaries = [
            Summary(
                document_id=doc_id, content="Doc summary",
                summary_type="document", generated_by_provider="mock",
                generated_by_model="mock-1",
            ),
        ]
        count = store.save_summaries(summaries)
        assert count == 1
        loaded = store.get_summaries(doc_id)
        assert len(loaded) == 1
        assert loaded[0].content == "Doc summary"
        assert loaded[0].summary_type == "document"
        assert loaded[0].generated_by_provider == "mock"
        store.close()

    def test_save_and_get_entities(self, tmp_path):
        store = KBStore(tmp_path / "test.db")
        doc = _make_doc()
        doc_id = store.save_document(doc)
        entities = [
            Entity(
                document_id=doc_id, name="Binary Search",
                entity_type="algorithm", description="Search algo",
                generated_by_provider="mock", generated_by_model="mock-1",
            ),
            Entity(
                document_id=doc_id, name="Array",
                entity_type="data_structure", description="Data struct",
                generated_by_provider="mock", generated_by_model="mock-1",
            ),
        ]
        count = store.save_entities(entities)
        assert count == 2
        loaded = store.get_entities(doc_id)
        assert len(loaded) == 2
        names = {e.name for e in loaded}
        assert "Array" in names
        assert "Binary Search" in names
        store.close()

    def test_save_and_get_relationships(self, tmp_path):
        store = KBStore(tmp_path / "test.db")
        doc = _make_doc()
        doc_id = store.save_document(doc)
        rels = [
            Relationship(
                source_entity_id="e1", target_entity_id="e2",
                relationship_type="uses",
                description="Binary search uses arrays",
                document_id=doc_id,
                generated_by_provider="mock", generated_by_model="mock-1",
                confidence=0.95,
            ),
        ]
        count = store.save_relationships(rels)
        assert count == 1
        loaded = store.get_relationships(doc_id)
        assert len(loaded) == 1
        assert loaded[0].relationship_type == "uses"
        assert loaded[0].confidence == 0.95
        assert loaded[0].source_entity_id == "e1"
        store.close()
