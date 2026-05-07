"""RAG pipeline — orchestrates retrieve → assemble → generate."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from bigbrain.config import BigBrainConfig, load_config
from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger
from bigbrain.providers.registry import ProviderRegistry
from bigbrain.rag.context import assemble_context
from bigbrain.rag.prompts import (
    build_explain_messages,
    build_qa_messages,
    build_qa_prompt,
    build_summarize_prompt,
)
from bigbrain.rag.retriever import Retriever
from bigbrain.stores.base import EntityStoreBackend

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
    retrieval_method: str = "fts5"


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

    def __init__(
        self,
        store: KBStore,
        registry: ProviderRegistry,
        entity_store: EntityStoreBackend | None = None,
    ) -> None:
        self._store = store
        self._registry = registry
        self._entity_store = entity_store
        self._retriever = Retriever(store, entity_store=entity_store)

    @classmethod
    def from_config(cls, config: BigBrainConfig | None = None) -> RAGPipeline:
        """Create pipeline from application config."""
        if config is None:
            config = load_config()

        store = KBStore(config.kb_db_path)
        registry = ProviderRegistry.from_config(config.providers)

        entity_store = None
        store_config = config.entity_store
        non_default_store = store_config.backend.lower() != "sqlite" or any(
            (
                store_config.postgres_url,
                store_config.neo4j_url,
                store_config.neo4j_password,
                store_config.qdrant_url,
                store_config.weaviate_url,
                store_config.pinecone_api_key,
                store_config.pinecone_environment,
            )
        )
        if non_default_store:
            from bigbrain.stores.factory import create_entity_store

            entity_store = create_entity_store(store_config, store)

        return cls(store=store, registry=registry, entity_store=entity_store)

    def close(self) -> None:
        """Close the underlying store."""
        if self._entity_store is not None:
            self._entity_store.close()
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
        use_hybrid: bool = False,
    ) -> RAGResponse:
        """Answer a question using KB context + AI provider.

        Args:
            question: The user's question
            max_docs: Max documents to retrieve from KB
            max_chunks: Max chunks to extract
            max_context_chars: Max chars for context assembly
            model: Override AI model
            use_chat: Use chat API (True) or completion API (False)
            use_hybrid: Use hybrid retrieval with the entity store when available

        Returns:
            RAGResponse with the answer and provenance
        """
        retrieval_method = "hybrid" if use_hybrid and self._entity_store is not None else "fts5"

        if use_hybrid:
            chunks = self._retriever.retrieve_hybrid(
                question, max_docs=max_docs, max_chunks=max_chunks
            )
        else:
            chunks = self._retriever.retrieve(
                question, max_docs=max_docs, max_chunks=max_chunks
            )

        if not chunks:
            return RAGResponse(
                answer="I couldn't find any relevant information in the knowledge base for your question.",
                chunks_used=0,
                docs_searched=0,
                retrieval_method=retrieval_method,
            )

        context = assemble_context(chunks, max_chars=max_context_chars)
        sources = list(dict.fromkeys(c.source_path for c in chunks if c.source_path))

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
            retrieval_method=retrieval_method,
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
