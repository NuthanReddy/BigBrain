"""Comprehensive tests for Phase 5 knowledge compilation pipeline.

Covers: models, markdown compiler, flashcard compiler, cheatsheet compiler,
QA generator, study guide compiler, compilation pipeline, and CompileConfig.

All AI calls are mocked — no real LLM server needed.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest

from bigbrain.compile.cheatsheet import CheatsheetCompiler
from bigbrain.compile.flashcard import FlashcardCompiler
from bigbrain.compile.markdown import MarkdownCompiler
from bigbrain.compile.models import (
    CompileOutput,
    CompileResult,
    Flashcard,
    OutputFormat,
    QAPair,
)
from bigbrain.compile.pipeline import CompilePipeline
from bigbrain.compile.qa_generator import QAGenerator
from bigbrain.compile.study_guide import StudyGuideCompiler
from bigbrain.config import BigBrainConfig, CompileConfig
from bigbrain.distill.models import Entity, Relationship, Summary
from bigbrain.kb.models import Document, SourceMetadata
from bigbrain.kb.store import KBStore
from bigbrain.providers.base import BaseProvider, ProviderResponse
from bigbrain.providers.registry import ProviderRegistry


# ── Mock provider ────────────────────────────────────────────────────


class MockCompileProvider(BaseProvider):
    """Deterministic mock provider for compilation tests."""

    @property
    def name(self) -> str:
        return "mock"

    def is_available(self) -> bool:
        return True

    def complete(
        self, prompt: str, *, model: str = "", **kwargs: Any
    ) -> ProviderResponse:
        return ProviderResponse(text="Mock output", provider="mock", model="mock-1")

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str = "",
        **kwargs: Any,
    ) -> ProviderResponse:
        last = messages[-1]["content"] if messages else ""
        if "flashcard" in last.lower():
            return ProviderResponse(
                text=(
                    '[{"front": "What is a BST?", "back": "A binary search tree",'
                    ' "tags": ["data_structure"]}]'
                ),
                provider="mock",
                model="mock-1",
            )
        # Study guide prompt contains "study guide" — check before generic "question"
        if "study guide" in last.lower():
            return ProviderResponse(
                text="Mock study guide content.", provider="mock", model="mock-1"
            )
        if "question" in last.lower():
            return ProviderResponse(
                text=(
                    '[{"question": "Explain BST.", "answer": "A tree with ordered nodes.",'
                    ' "difficulty": "easy", "topic": "trees"}]'
                ),
                provider="mock",
                model="mock-1",
            )
        return ProviderResponse(
            text="Mock generic content.", provider="mock", model="mock-1"
        )


# ── Helper data ──────────────────────────────────────────────────────


def _make_test_data():
    """Create a complete set of test data for compilation tests."""
    doc = Document(
        title="Test Doc",
        content="Test content about data structures and algorithms.",
        source=SourceMetadata(
            file_path="test.txt",
            file_extension=".txt",
            source_type="txt",
            size_bytes=100,
        ),
    )
    summaries = [
        Summary(
            document_id=doc.id,
            content="This is a test summary about data structures.",
            summary_type="document",
        )
    ]
    entities = [
        Entity(
            document_id=doc.id,
            name="BST",
            entity_type="data_structure",
            description="Binary search tree",
        ),
        Entity(
            document_id=doc.id,
            name="Quicksort",
            entity_type="algorithm",
            description="Divide and conquer sort",
        ),
    ]
    relationships = [
        Relationship(
            source_entity_id=entities[0].id,
            target_entity_id=entities[1].id,
            relationship_type="related_to",
            description="Both use comparison",
            document_id=doc.id,
        ),
    ]
    return doc, summaries, entities, relationships


def _make_mock_registry() -> ProviderRegistry:
    """Create a ProviderRegistry with a mock provider registered."""
    registry = ProviderRegistry()
    registry.register(MockCompileProvider())
    return registry


def _setup_pipeline(tmp_path: Path) -> tuple[CompilePipeline, Document]:
    """Create a pipeline backed by a real SQLite store in tmp_path."""
    store = KBStore(tmp_path / "test.db")
    doc, summaries, entities, relationships = _make_test_data()

    # save_document generates a deterministic ID from file_path;
    # update distilled objects to reference that stored ID.
    stored_id = store.save_document(doc)
    for s in summaries:
        s.document_id = stored_id
    for e in entities:
        e.document_id = stored_id
    for r in relationships:
        r.document_id = stored_id

    store.save_summaries(summaries)
    store.save_entities(entities)
    store.save_relationships(relationships)

    # Retrieve the persisted doc (with the stored id) for later assertions
    stored_doc = store.get_document(stored_id)
    assert stored_doc is not None

    registry = _make_mock_registry()
    config = CompileConfig(output_dir=str(tmp_path / "output"))
    pipeline = CompilePipeline(store=store, registry=registry, config=config)
    return pipeline, stored_doc


# ── 1. TestCompileModels ─────────────────────────────────────────────


class TestCompileModels:
    """Tests for the data models in compile.models."""

    def test_output_format_enum_values(self):
        assert OutputFormat.MARKDOWN.value == "markdown"
        assert OutputFormat.FLASHCARD.value == "flashcard"
        assert OutputFormat.CHEATSHEET.value == "cheatsheet"
        assert OutputFormat.QA.value == "qa"
        assert OutputFormat.STUDY_GUIDE.value == "study_guide"

    def test_compile_output_defaults(self):
        output = CompileOutput()
        assert output.id  # uuid generated
        assert output.format == OutputFormat.MARKDOWN
        assert output.title == ""
        assert output.content == ""
        assert output.source_doc_id == ""
        assert output.flashcards == []
        assert output.qa_pairs == []
        assert output.generated_by_provider == ""
        assert output.generated_by_model == ""
        assert output.metadata == {}
        assert output.created_at is not None

    def test_compile_result_defaults(self):
        result = CompileResult()
        assert result.outputs == []
        assert result.errors == []
        assert result.total_documents == 0


# ── 2. TestMarkdownCompiler ──────────────────────────────────────────


class TestMarkdownCompiler:
    """Tests for the MarkdownCompiler."""

    def test_full_render(self):
        doc, summaries, entities, relationships = _make_test_data()
        compiler = MarkdownCompiler()
        output = compiler.compile(doc, summaries, entities, relationships)

        assert "# Test Doc" in output.content
        assert "## Summary" in output.content
        assert "test summary" in output.content
        assert "## Key Concepts" in output.content
        assert "**BST**" in output.content
        assert "**Quicksort**" in output.content
        assert "## Relationships" in output.content
        assert "related_to" in output.content
        assert output.source_doc_id == doc.id
        assert output.source_doc_title == doc.title

    def test_empty_entities(self):
        doc, summaries, _, _ = _make_test_data()
        compiler = MarkdownCompiler()
        output = compiler.compile(doc, summaries, [], [])

        assert "# Test Doc" in output.content
        assert "## Summary" in output.content
        assert "Key Concepts" not in output.content
        assert "Relationships" not in output.content

    def test_output_format_is_markdown(self):
        doc, summaries, entities, relationships = _make_test_data()
        compiler = MarkdownCompiler()
        output = compiler.compile(doc, summaries, entities, relationships)

        assert output.format == OutputFormat.MARKDOWN
        assert "Summary" in output.title


# ── 3. TestFlashcardCompiler ─────────────────────────────────────────


class TestFlashcardCompiler:
    """Tests for the FlashcardCompiler."""

    def test_template_mode_no_registry(self):
        doc, summaries, entities, _ = _make_test_data()
        compiler = FlashcardCompiler(registry=None)
        output = compiler.compile(doc, summaries, entities)

        assert output.format == OutputFormat.FLASHCARD
        assert len(output.flashcards) == 2  # BST + Quicksort
        assert output.flashcards[0].front == "What is BST?"
        assert output.flashcards[0].back == "Binary search tree"
        assert "data_structure" in output.flashcards[0].tags
        assert output.generated_by_provider == ""

    def test_ai_mode_with_mock_registry(self):
        doc, summaries, entities, _ = _make_test_data()
        registry = _make_mock_registry()
        compiler = FlashcardCompiler(registry=registry)
        output = compiler.compile(doc, summaries, entities)

        assert output.format == OutputFormat.FLASHCARD
        assert len(output.flashcards) >= 1
        assert output.flashcards[0].front == "What is a BST?"
        assert output.flashcards[0].back == "A binary search tree"
        assert output.generated_by_provider == "mock"
        assert output.generated_by_model == "mock-1"

    def test_output_has_flashcards_populated(self):
        doc, summaries, entities, _ = _make_test_data()
        compiler = FlashcardCompiler(registry=None)
        output = compiler.compile(doc, summaries, entities)

        assert isinstance(output.flashcards, list)
        assert all(isinstance(fc, Flashcard) for fc in output.flashcards)
        assert "Flashcards" in output.title
        assert "Card 1" in output.content


# ── 4. TestCheatsheetCompiler ────────────────────────────────────────


class TestCheatsheetCompiler:
    """Tests for the CheatsheetCompiler."""

    def test_groups_entities_by_type(self):
        doc, _, entities, relationships = _make_test_data()
        compiler = CheatsheetCompiler()
        output = compiler.compile(doc, entities, relationships)

        assert output.format == OutputFormat.CHEATSHEET
        assert "## Algorithm" in output.content
        assert "## Data Structure" in output.content
        assert "**BST**" in output.content
        assert "**Quicksort**" in output.content

    def test_empty_entities_message(self):
        doc, _, _, _ = _make_test_data()
        compiler = CheatsheetCompiler()
        output = compiler.compile(doc, [], None)

        assert "No entities extracted" in output.content
        assert "bigbrain distill" in output.content

    def test_includes_relationships_section(self):
        doc, _, entities, relationships = _make_test_data()
        compiler = CheatsheetCompiler()
        output = compiler.compile(doc, entities, relationships)

        assert "Quick Reference: Relationships" in output.content
        assert "related to" in output.content
        assert "Cheatsheet" in output.title


# ── 5. TestQAGenerator ───────────────────────────────────────────────


class TestQAGenerator:
    """Tests for the QAGenerator."""

    def test_template_mode_no_registry(self):
        doc, summaries, entities, _ = _make_test_data()
        generator = QAGenerator(registry=None)
        output = generator.compile(doc, summaries, entities)

        assert output.format == OutputFormat.QA
        assert len(output.qa_pairs) == 2  # BST + Quicksort
        assert output.qa_pairs[0].question == "Explain BST."
        assert output.qa_pairs[0].answer == "Binary search tree"
        assert output.qa_pairs[0].difficulty == "medium"
        assert output.generated_by_provider == ""

    def test_ai_mode_with_mock_registry(self):
        doc, summaries, entities, _ = _make_test_data()
        registry = _make_mock_registry()
        generator = QAGenerator(registry=registry)
        output = generator.compile(doc, summaries, entities)

        assert output.format == OutputFormat.QA
        assert len(output.qa_pairs) >= 1
        assert output.qa_pairs[0].question == "Explain BST."
        assert output.qa_pairs[0].answer == "A tree with ordered nodes."
        assert output.qa_pairs[0].difficulty == "easy"
        assert output.generated_by_provider == "mock"

    def test_output_has_qa_pairs_populated(self):
        doc, summaries, entities, _ = _make_test_data()
        generator = QAGenerator(registry=None)
        output = generator.compile(doc, summaries, entities)

        assert isinstance(output.qa_pairs, list)
        assert all(isinstance(qp, QAPair) for qp in output.qa_pairs)
        assert "Study Questions" in output.title
        assert "Q1" in output.content


# ── 6. TestStudyGuideCompiler ────────────────────────────────────────


class TestStudyGuideCompiler:
    """Tests for the StudyGuideCompiler."""

    def test_template_mode_generates_sections(self):
        doc, summaries, entities, relationships = _make_test_data()
        compiler = StudyGuideCompiler(registry=None)
        output = compiler.compile(doc, summaries, entities, relationships)

        assert output.format == OutputFormat.STUDY_GUIDE
        assert "## Overview" in output.content
        assert "## Core Concepts" in output.content
        assert "## How They Connect" in output.content
        assert "## Review Questions" in output.content
        assert "BST" in output.content
        assert output.generated_by_provider == ""

    def test_ai_mode_with_mock_registry(self):
        doc, summaries, entities, relationships = _make_test_data()
        registry = _make_mock_registry()
        compiler = StudyGuideCompiler(registry=registry)
        output = compiler.compile(doc, summaries, entities, relationships)

        assert output.format == OutputFormat.STUDY_GUIDE
        assert "Study Guide" in output.title
        assert output.generated_by_provider == "mock"
        assert output.generated_by_model == "mock-1"
        assert "Mock study guide content." in output.content

    def test_contains_expected_sections_template(self):
        doc, summaries, entities, relationships = _make_test_data()
        compiler = StudyGuideCompiler(registry=None)
        output = compiler.compile(doc, summaries, entities, relationships)

        assert "# Study Guide: Test Doc" in output.content
        assert "### BST" in output.content
        assert "### Quicksort" in output.content
        assert "related to" in output.content.lower() or "related_to" in output.content


# ── 7. TestCompilePipeline ───────────────────────────────────────────


class TestCompilePipeline:
    """Tests for the CompilePipeline orchestrator."""

    def test_compile_document_markdown(self, tmp_path):
        pipeline, doc = _setup_pipeline(tmp_path)
        try:
            output = pipeline.compile_document(doc.id, format="markdown")

            assert output is not None
            assert output.format == OutputFormat.MARKDOWN
            assert "# Test Doc" in output.content
            assert "## Summary" in output.content
        finally:
            pipeline.close()

    def test_compile_document_flashcard(self, tmp_path):
        pipeline, doc = _setup_pipeline(tmp_path)
        try:
            output = pipeline.compile_document(doc.id, format="flashcard")

            assert output is not None
            assert output.format == OutputFormat.FLASHCARD
            assert len(output.flashcards) >= 1
            assert output.generated_by_provider == "mock"
        finally:
            pipeline.close()

    def test_compile_document_not_found(self, tmp_path):
        pipeline, _ = _setup_pipeline(tmp_path)
        try:
            output = pipeline.compile_document("nonexistent-id", format="markdown")
            assert output is None
        finally:
            pipeline.close()

    def test_compile_all_processes_multiple_docs(self, tmp_path):
        store = KBStore(tmp_path / "multi.db")
        doc1, summaries1, entities1, rels1 = _make_test_data()
        doc2 = Document(
            title="Second Doc",
            content="More content.",
            source=SourceMetadata(
                file_path="second.txt",
                file_extension=".txt",
                source_type="txt",
                size_bytes=50,
            ),
        )
        id1 = store.save_document(doc1)
        store.save_document(doc2)

        for s in summaries1:
            s.document_id = id1
        for e in entities1:
            e.document_id = id1
        for r in rels1:
            r.document_id = id1

        store.save_summaries(summaries1)
        store.save_entities(entities1)
        store.save_relationships(rels1)

        registry = _make_mock_registry()
        config = CompileConfig(output_dir=str(tmp_path / "all_output"))
        pipeline = CompilePipeline(store=store, registry=registry, config=config)
        try:
            result = pipeline.compile_all(format="markdown")

            assert result.total_documents == 2
            assert len(result.outputs) == 2
            assert result.errors == []
        finally:
            pipeline.close()

    def test_output_files_written_to_disk(self, tmp_path):
        pipeline, doc = _setup_pipeline(tmp_path)
        try:
            output = pipeline.compile_document(doc.id, format="markdown")

            assert output is not None
            output_dir = tmp_path / "output"
            assert output_dir.exists()
            md_files = list(output_dir.glob("*.md"))
            assert len(md_files) >= 1
            content = md_files[0].read_text(encoding="utf-8")
            assert "# Test Doc" in content
        finally:
            pipeline.close()


# ── 8. TestCompileConfig ─────────────────────────────────────────────


class TestCompileConfig:
    """Tests for CompileConfig defaults and integration with BigBrainConfig."""

    def test_default_values(self):
        config = CompileConfig()
        assert config.output_dir == "build"
        assert config.default_format == "markdown"
        assert config.flashcard_count == 20
        assert config.qa_count == 15
        assert config.include_relationships is True
        assert config.include_entities is True

    def test_config_in_bigbrain_config(self):
        cfg = BigBrainConfig()
        assert isinstance(cfg.compile, CompileConfig)
        assert cfg.compile.default_format == "markdown"
        assert cfg.compile.flashcard_count == 20
