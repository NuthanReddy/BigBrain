"""RAG pipeline — orchestrates retrieve → assemble → generate."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger
from bigbrain.providers.base import ProviderResponse
from bigbrain.providers.registry import ProviderRegistry
from bigbrain.rag.context import assemble_context
from bigbrain.rag.prompts import (
    build_explain_messages,
    build_qa_messages,
    build_qa_prompt,
    build_summarize_prompt,
)
from bigbrain.rag.retriever import Retriever, RetrievedChunk

logger = get_logger(__name__)


@dataclass
class RAGResponse:
    """Response from the RAG pipeline."""
    answer: str
    provider: str = ""
    model: str = ""
    chunks_used: int = 0
    docs_searched: int = 0
    sources: list[str] = field(default_factory=list)  # unique source paths
    usage: dict[str, int] = field(default_factory=dict)


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline.

    Orchestrates: KB search → chunk extraction → context assembly → LLM generation.

    Usage::

        pipeline = RAGPipeline(store=store, registry=registry)
        response = pipeline.ask("What is a binary search tree?")
        print(response.answer)

    Or from config::

        pipeline = RAGPipeline.from_config()
        response = pipeline.ask("Explain quicksort")
    """

    def __init__(self, store: KBStore, registry: ProviderRegistry) -> None:
        self._store = store
        self._registry = registry
        self._retriever = Retriever(store)

    @classmethod
    def from_config(cls) -> RAGPipeline:
        """Create pipeline from application config."""
        from bigbrain.config import load_config
        cfg = load_config()
        store = KBStore(cfg.kb_db_path)
        registry = ProviderRegistry.from_config(cfg.providers)
        return cls(store=store, registry=registry)

    def close(self) -> None:
        """Close the underlying store."""
        self._store.close()

    def __enter__(self) -> RAGPipeline:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def ask(
        self,
        question: str,
        *,
        max_docs: int = 5,
        max_chunks: int = 15,
        max_context_chars: int = 12000,
        model: str = "",
        use_chat: bool = True,
    ) -> RAGResponse:
        """Answer a question using KB context + AI provider.

        Args:
            question: The user's question
            max_docs: Max documents to retrieve from KB
            max_chunks: Max chunks to extract
            max_context_chars: Max chars for context assembly
            model: Override AI model
            use_chat: Use chat API (True) or completion API (False)

        Returns:
            RAGResponse with the answer and provenance
        """
        # Step 1: Retrieve
        chunks = self._retriever.retrieve(
            question, max_docs=max_docs, max_chunks=max_chunks
        )
        if not chunks:
            return RAGResponse(
                answer="I couldn't find any relevant information in the knowledge base for your question.",
                chunks_used=0,
                docs_searched=0,
            )

        # Step 2: Assemble context
        context = assemble_context(chunks, max_chars=max_context_chars)
        sources = list(dict.fromkeys(c.source_path for c in chunks if c.source_path))

        # Step 3: Generate
        if use_chat:
            messages = build_qa_messages(question, context)
            provider_resp = self._registry.chat(messages, model=model)
        else:
            prompt = build_qa_prompt(question, context)
            provider_resp = self._registry.complete(prompt, model=model)

        return RAGResponse(
            answer=provider_resp.text,
            provider=provider_resp.provider,
            model=provider_resp.model,
            chunks_used=len(chunks),
            docs_searched=max_docs,
            sources=sources,
            usage=provider_resp.usage,
        )

    def summarize_document(self, doc_id: str, *, model: str = "") -> RAGResponse:
        """Summarize a specific document from the KB."""
        doc = self._store.get_document(doc_id)
        if doc is None:
            return RAGResponse(answer="Document not found.")

        text = doc.content[:8000]  # Truncate for context window
        prompt = build_summarize_prompt(text)
        resp = self._registry.complete(prompt, model=model)

        source_path = doc.source.file_path if doc.source else ""
        return RAGResponse(
            answer=resp.text,
            provider=resp.provider,
            model=resp.model,
            chunks_used=1,
            docs_searched=1,
            sources=[source_path] if source_path else [],
            usage=resp.usage,
        )

    def explain(
        self,
        concept: str,
        *,
        max_docs: int = 3,
        model: str = "",
    ) -> RAGResponse:
        """Explain a concept using KB context."""
        chunks = self._retriever.retrieve(concept, max_docs=max_docs)
        if not chunks:
            return RAGResponse(answer="No relevant context found for this concept.")

        context = assemble_context(chunks)
        sources = list(dict.fromkeys(c.source_path for c in chunks if c.source_path))

        messages = build_explain_messages(concept, context)
        resp = self._registry.chat(messages, model=model)

        return RAGResponse(
            answer=resp.text,
            provider=resp.provider,
            model=resp.model,
            chunks_used=len(chunks),
            sources=sources,
            usage=resp.usage,
        )
