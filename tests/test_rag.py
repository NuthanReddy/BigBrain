"""Comprehensive tests for the BigBrain RAG pipeline.

Covers: Retriever, context assembly, prompt building, RAGPipeline, RAGResponse.
"""

from __future__ import annotations

import pytest
from typing import Any

from bigbrain.kb.models import Document, DocumentSection, SourceMetadata
from bigbrain.kb.store import KBStore
from bigbrain.rag.retriever import Retriever, RetrievedChunk
from bigbrain.rag.context import assemble_context
from bigbrain.rag.prompts import (
    build_qa_messages,
    build_qa_prompt,
    build_summarize_prompt,
    build_explain_messages,
)
from bigbrain.rag.pipeline import RAGPipeline, RAGResponse
from bigbrain.providers.base import BaseProvider, ProviderResponse
from bigbrain.providers.registry import ProviderRegistry
from bigbrain.errors import ProviderError


# ---------------------------------------------------------------------------
# Mock provider
# ---------------------------------------------------------------------------

class MockRAGProvider(BaseProvider):
    """Deterministic provider for testing RAG pipeline."""

    @property
    def name(self) -> str:
        return "mock"

    def is_available(self) -> bool:
        return True

    def complete(self, prompt: str, *, model: str = "", **kwargs: Any) -> ProviderResponse:
        return ProviderResponse(
            text=f"Answer about: {prompt[:50]}",
            provider="mock",
            model="mock-1",
        )

    def chat(self, messages: list[dict[str, str]], *, model: str = "", **kwargs: Any) -> ProviderResponse:
        last_msg = messages[-1]["content"] if messages else ""
        return ProviderResponse(
            text=f"Chat answer for: {last_msg[:50]}",
            provider="mock",
            model="mock-1",
        )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _populate_store(store: KBStore) -> list[str]:
    """Add sample documents and return their IDs for later lookup."""
    docs = [
        Document(
            title="Binary Search Trees",
            content=(
                "A binary search tree is a data structure where each node has at most "
                "two children. The left subtree contains only nodes with keys less than "
                "the parent. The right subtree contains only nodes with keys greater "
                "than the parent. This property makes search operations efficient with "
                "O(log n) average time."
            ),
            source=SourceMetadata(
                file_path="bst.txt",
                file_extension=".txt",
                source_type="txt",
                size_bytes=200,
            ),
            sections=[
                DocumentSection(
                    title="Definition",
                    content=(
                        "A binary search tree (BST) is a rooted binary tree where each "
                        "node stores a key greater than all keys in its left subtree and "
                        "less than all keys in its right subtree."
                    ),
                    level=1,
                ),
                DocumentSection(
                    title="Operations",
                    content=(
                        "Search, insert, and delete operations on a BST run in O(h) time "
                        "where h is the height. For balanced BSTs, h = O(log n)."
                    ),
                    level=1,
                ),
            ],
        ),
        Document(
            title="Sorting Algorithms",
            content=(
                "Quicksort uses a divide-and-conquer strategy. It picks a pivot element, "
                "partitions the array around the pivot, then recursively sorts the "
                "sub-arrays. Average case is O(n log n)."
            ),
            source=SourceMetadata(
                file_path="sorting.txt",
                file_extension=".txt",
                source_type="txt",
                size_bytes=150,
            ),
            sections=[
                DocumentSection(
                    title="Quicksort",
                    content=(
                        "Quicksort picks a pivot, partitions elements around it, and "
                        "recursively sorts. Average O(n log n), worst O(n^2)."
                    ),
                    level=1,
                ),
                DocumentSection(
                    title="Mergesort",
                    content=(
                        "Mergesort divides the array in half, recursively sorts both "
                        "halves, then merges. Always O(n log n) but uses O(n) extra space."
                    ),
                    level=1,
                ),
            ],
        ),
    ]
    ids = []
    for doc in docs:
        ids.append(store.save_document(doc))
    return ids


def _make_registry() -> ProviderRegistry:
    """Create a ProviderRegistry with the mock provider."""
    registry = ProviderRegistry()
    registry.register(MockRAGProvider())
    return registry


# ---------------------------------------------------------------------------
# 1. TestRetriever
# ---------------------------------------------------------------------------

class TestRetriever:
    """Tests for bigbrain.rag.retriever.Retriever."""

    def test_retrieve_finds_relevant_chunks(self, tmp_path):
        db = tmp_path / "ret.db"
        store = KBStore(db)
        _populate_store(store)
        retriever = Retriever(store)

        chunks = retriever.retrieve("binary search")
        assert len(chunks) > 0
        assert any("binary" in c.text.lower() or "search" in c.text.lower() for c in chunks)
        store.close()

    def test_retrieve_returns_empty_for_no_match(self, tmp_path):
        db = tmp_path / "ret.db"
        store = KBStore(db)
        _populate_store(store)
        retriever = Retriever(store)

        chunks = retriever.retrieve("xyznonexistentterm123")
        assert chunks == []
        store.close()

    def test_retrieve_extracts_sections(self, tmp_path):
        db = tmp_path / "ret.db"
        store = KBStore(db)
        _populate_store(store)
        retriever = Retriever(store)

        chunks = retriever.retrieve("binary search tree")
        section_titles = [c.section_title for c in chunks if c.section_title]
        assert len(section_titles) > 0, "Expected chunks from document sections"
        store.close()

    def test_retrieve_respects_max_chunks(self, tmp_path):
        db = tmp_path / "ret.db"
        store = KBStore(db)
        _populate_store(store)
        retriever = Retriever(store)

        chunks = retriever.retrieve("binary search tree", max_chunks=2)
        assert len(chunks) <= 2
        store.close()

    def test_retrieve_filters_short_sections(self, tmp_path):
        """Sections shorter than min_chunk_length should be excluded."""
        db = tmp_path / "ret.db"
        store = KBStore(db)
        # Create a document with one short and one long section
        doc = Document(
            title="Short Section Doc",
            content="Content for the short section document.",
            source=SourceMetadata(
                file_path="short.txt",
                file_extension=".txt",
                source_type="txt",
                size_bytes=100,
            ),
            sections=[
                DocumentSection(title="Tiny", content="Too short.", level=1),
                DocumentSection(
                    title="Long Enough",
                    content="A" * 200,  # well above any reasonable min_chunk_length
                    level=1,
                ),
            ],
        )
        store.save_document(doc)
        retriever = Retriever(store)

        chunks = retriever.retrieve("short section", min_chunk_length=50)
        texts = [c.text for c in chunks]
        assert not any(t == "Too short." for t in texts), "Short section should be filtered"
        store.close()

    def test_retrieve_falls_back_to_content(self, tmp_path):
        """Documents with no sections should use content directly."""
        db = tmp_path / "ret.db"
        store = KBStore(db)
        doc = Document(
            title="No Sections",
            content="This document has no sections but does have content that is long enough for chunking purposes and testing.",
            source=SourceMetadata(
                file_path="nosec.txt",
                file_extension=".txt",
                source_type="txt",
                size_bytes=100,
            ),
            sections=[],
        )
        store.save_document(doc)
        retriever = Retriever(store)

        chunks = retriever.retrieve("no sections")
        assert len(chunks) > 0
        assert chunks[0].section_title == ""
        assert "no sections" in chunks[0].text.lower() or "content" in chunks[0].text.lower()
        store.close()


# ---------------------------------------------------------------------------
# 2. TestContextAssembly
# ---------------------------------------------------------------------------

class TestContextAssembly:
    """Tests for bigbrain.rag.context.assemble_context."""

    def _make_chunks(self, n: int = 3) -> list[RetrievedChunk]:
        return [
            RetrievedChunk(
                text=f"Content for chunk {i}. " * 10,
                source_title=f"Source {i}",
                source_path=f"source{i}.txt",
                section_title=f"Section {i}",
            )
            for i in range(n)
        ]

    def test_assemble_basic(self):
        chunks = self._make_chunks(2)
        result = assemble_context(chunks)
        assert "[Source 0 — Section 0]" in result
        assert "Content for chunk 0" in result
        assert "[Source 1 — Section 1]" in result

    def test_assemble_respects_max_chars(self):
        chunks = self._make_chunks(5)
        result = assemble_context(chunks, max_chars=300)
        assert len(result) <= 400  # some tolerance for label overhead

    def test_assemble_empty_chunks(self):
        result = assemble_context([])
        assert result == ""

    def test_assemble_labels_include_source(self):
        chunks = [
            RetrievedChunk(
                text="Some text content here that is long enough to pass filters.",
                source_title="My Title",
                source_path="myfile.txt",
                section_title="My Section",
            )
        ]
        result = assemble_context(chunks)
        assert "[My Title — My Section]" in result

    def test_assemble_label_without_section(self):
        """Chunks without section_title get label with just the source title."""
        chunks = [
            RetrievedChunk(
                text="Some text content here that is long enough.",
                source_title="Only Title",
                source_path="only.txt",
                section_title="",
            )
        ]
        result = assemble_context(chunks)
        assert "[Only Title]" in result
        assert "—" not in result

    def test_assemble_separator(self):
        chunks = self._make_chunks(2)
        sep = "\n===\n"
        result = assemble_context(chunks, separator=sep)
        assert sep in result


# ---------------------------------------------------------------------------
# 3. TestPrompts
# ---------------------------------------------------------------------------

class TestPrompts:
    """Tests for bigbrain.rag.prompts template builders."""

    def test_build_qa_messages(self):
        msgs = build_qa_messages("What is a BST?", "A BST is a tree...")
        assert len(msgs) == 2
        assert msgs[0]["role"] == "system"
        assert msgs[1]["role"] == "user"
        assert "A BST is a tree" in msgs[1]["content"]
        assert "What is a BST?" in msgs[1]["content"]

    def test_build_qa_prompt(self):
        prompt = build_qa_prompt("What is quicksort?", "Quicksort is...")
        assert isinstance(prompt, str)
        assert "Quicksort is..." in prompt
        assert "What is quicksort?" in prompt

    def test_build_summarize_prompt(self):
        prompt = build_summarize_prompt("Some long text here.")
        assert isinstance(prompt, str)
        assert "Some long text here." in prompt
        assert "Summarize" in prompt or "Summary" in prompt

    def test_build_explain_messages(self):
        msgs = build_explain_messages("recursion", "Recursion is when...")
        assert len(msgs) == 2
        assert msgs[0]["role"] == "system"
        assert msgs[1]["role"] == "user"
        assert "recursion" in msgs[1]["content"]
        assert "Recursion is when..." in msgs[1]["content"]

    def test_qa_messages_system_contains_instructions(self):
        msgs = build_qa_messages("q", "c")
        assert "context" in msgs[0]["content"].lower() or "answer" in msgs[0]["content"].lower()

    def test_explain_messages_contains_explain_directive(self):
        msgs = build_explain_messages("trees", "Trees are...")
        assert "explain" in msgs[1]["content"].lower() or "Explain" in msgs[1]["content"]


# ---------------------------------------------------------------------------
# 4. TestRAGPipeline
# ---------------------------------------------------------------------------

class TestRAGPipeline:
    """Tests for bigbrain.rag.pipeline.RAGPipeline."""

    def test_ask_returns_answer(self, tmp_path):
        db = tmp_path / "rag.db"
        store = KBStore(db)
        _populate_store(store)
        registry = _make_registry()

        pipeline = RAGPipeline(store=store, registry=registry)
        response = pipeline.ask("binary search tree")

        assert response.answer
        assert response.chunks_used > 0
        assert len(response.sources) > 0
        pipeline.close()

    def test_ask_no_results(self, tmp_path):
        """Empty KB should return a 'couldn't find' message."""
        db = tmp_path / "rag_empty.db"
        store = KBStore(db)
        registry = _make_registry()

        pipeline = RAGPipeline(store=store, registry=registry)
        response = pipeline.ask("anything at all")

        assert "couldn't find" in response.answer.lower() or "no relevant" in response.answer.lower()
        assert response.chunks_used == 0
        pipeline.close()

    def test_ask_includes_provenance(self, tmp_path):
        db = tmp_path / "rag.db"
        store = KBStore(db)
        _populate_store(store)
        registry = _make_registry()

        pipeline = RAGPipeline(store=store, registry=registry)
        response = pipeline.ask("binary search tree")

        assert response.provider == "mock"
        assert response.model == "mock-1"
        assert any("bst.txt" in s for s in response.sources)
        pipeline.close()

    def test_ask_uses_completion_api(self, tmp_path):
        """use_chat=False should route through complete() instead of chat()."""
        db = tmp_path / "rag.db"
        store = KBStore(db)
        _populate_store(store)
        registry = _make_registry()

        pipeline = RAGPipeline(store=store, registry=registry)
        response = pipeline.ask("binary search tree", use_chat=False)

        # MockRAGProvider.complete returns "Answer about: ..."
        assert response.answer.startswith("Answer about:")
        pipeline.close()

    def test_explain_returns_answer(self, tmp_path):
        db = tmp_path / "rag.db"
        store = KBStore(db)
        _populate_store(store)
        registry = _make_registry()

        pipeline = RAGPipeline(store=store, registry=registry)
        response = pipeline.explain("binary search tree")

        assert response.answer
        assert response.chunks_used > 0
        pipeline.close()

    def test_explain_no_context(self, tmp_path):
        """explain() on empty KB returns 'no relevant context' message."""
        db = tmp_path / "rag_empty.db"
        store = KBStore(db)
        registry = _make_registry()

        pipeline = RAGPipeline(store=store, registry=registry)
        response = pipeline.explain("nonexistent concept")

        assert "no relevant" in response.answer.lower()
        pipeline.close()

    def test_summarize_document(self, tmp_path):
        db = tmp_path / "rag.db"
        store = KBStore(db)
        doc_ids = _populate_store(store)
        registry = _make_registry()

        pipeline = RAGPipeline(store=store, registry=registry)
        response = pipeline.summarize_document(doc_ids[0])

        assert response.answer
        assert response.chunks_used == 1
        assert response.docs_searched == 1
        pipeline.close()

    def test_summarize_document_not_found(self, tmp_path):
        db = tmp_path / "rag.db"
        store = KBStore(db)
        registry = _make_registry()

        pipeline = RAGPipeline(store=store, registry=registry)
        response = pipeline.summarize_document("nonexistent-id")

        assert "not found" in response.answer.lower()
        pipeline.close()

    def test_context_manager(self, tmp_path):
        db = tmp_path / "rag.db"
        store = KBStore(db)
        _populate_store(store)
        registry = _make_registry()

        with RAGPipeline(store=store, registry=registry) as pipeline:
            response = pipeline.ask("binary search tree")
            assert response.answer


# ---------------------------------------------------------------------------
# 5. TestRAGResponse
# ---------------------------------------------------------------------------

class TestRAGResponse:
    """Tests for the RAGResponse dataclass."""

    def test_default_values(self):
        r = RAGResponse(answer="hello")
        assert r.answer == "hello"
        assert r.provider == ""
        assert r.model == ""
        assert r.chunks_used == 0
        assert r.docs_searched == 0
        assert r.sources == []
        assert r.usage == {}

    def test_custom_values(self):
        r = RAGResponse(
            answer="some answer",
            provider="ollama",
            model="llama3",
            chunks_used=5,
            docs_searched=3,
            sources=["a.txt", "b.txt"],
            usage={"tokens_in": 100, "tokens_out": 50},
        )
        assert r.answer == "some answer"
        assert r.provider == "ollama"
        assert r.model == "llama3"
        assert r.chunks_used == 5
        assert r.docs_searched == 3
        assert r.sources == ["a.txt", "b.txt"]
        assert r.usage["tokens_in"] == 100
        assert r.usage["tokens_out"] == 50
