"""Retrieval stage — searches KB and extracts relevant chunks."""

from __future__ import annotations

from dataclasses import dataclass

from bigbrain.kb.models import Document
from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger
from bigbrain.stores.base import EntityStoreBackend

logger = get_logger(__name__)


@dataclass
class RetrievedChunk:
    """A chunk of text retrieved from the KB with provenance."""

    text: str
    source_title: str
    source_path: str
    section_title: str = ""
    score: float = 0.0  # relevance ranking (lower = more relevant in FTS5)
    retrieval_method: str = "fts5"


class Retriever:
    """Retrieves and chunks relevant content from the knowledge base."""

    def __init__(
        self,
        store: KBStore,
        entity_store: EntityStoreBackend | None = None,
    ) -> None:
        self._store = store
        self._entity_store = entity_store

    def _extract_document_chunks(
        self,
        doc: Document,
        *,
        min_chunk_length: int,
        retrieval_method: str,
    ) -> list[RetrievedChunk]:
        """Extract chunks from a document for a specific retrieval method."""
        chunks: list[RetrievedChunk] = []
        source_path = doc.source.file_path if doc.source else ""

        if doc.sections:
            for sec in doc.sections:
                text = sec.content.strip()
                if len(text) >= min_chunk_length:
                    chunks.append(
                        RetrievedChunk(
                            text=text,
                            source_title=doc.title,
                            source_path=source_path,
                            section_title=sec.title,
                            retrieval_method=retrieval_method,
                        )
                    )
        elif doc.content.strip():
            text = doc.content.strip()[:5000]
            chunks.append(
                RetrievedChunk(
                    text=text,
                    source_title=doc.title,
                    source_path=source_path,
                    retrieval_method=retrieval_method,
                )
            )

        return chunks

    def retrieve(
        self,
        query: str,
        *,
        max_docs: int = 5,
        max_chunks: int = 15,
        min_chunk_length: int = 50,
    ) -> list[RetrievedChunk]:
        """Search KB and extract relevant chunks.

        Strategy:
        1. FTS5 search for top documents
        2. Extract sections from each document
        3. Filter out very short/empty sections
        4. Return up to max_chunks chunks
        """
        docs = self._store.search_documents(query, limit=max_docs)
        if not docs:
            return []

        chunks: list[RetrievedChunk] = []
        for doc in docs:
            chunks.extend(
                self._extract_document_chunks(
                    doc,
                    min_chunk_length=min_chunk_length,
                    retrieval_method="fts5",
                )
            )

        return chunks[:max_chunks]

    def retrieve_hybrid(
        self,
        query: str,
        *,
        max_docs: int = 5,
        max_chunks: int = 15,
        min_chunk_length: int = 50,
    ) -> list[RetrievedChunk]:
        """Search KB with FTS5 and entity-store similarity, then merge results.

        Vector-backed entity matches are prioritized ahead of FTS5 matches. If the
        same document appears in both result sets, only one set of chunks is kept
        for that document and its provenance is marked as ``hybrid``.
        """
        vector_chunks_by_doc: dict[str, list[RetrievedChunk]] = {}
        vector_doc_order: list[str] = []

        if self._entity_store is not None:
            try:
                entities = self._entity_store.search_similar(query, limit=max_docs)
            except Exception:
                logger.exception("Entity-store similarity search failed for query: %r", query)
                entities = []

            for entity in entities:
                doc_id = entity.document_id
                if not doc_id or doc_id in vector_chunks_by_doc:
                    continue

                doc = self._store.get_document(doc_id)
                if doc is None:
                    logger.debug("Skipping entity %s; document %s not found", entity.id, doc_id)
                    continue

                chunks = self._extract_document_chunks(
                    doc,
                    min_chunk_length=min_chunk_length,
                    retrieval_method="vector",
                )
                if not chunks:
                    continue

                vector_chunks_by_doc[doc_id] = chunks
                vector_doc_order.append(doc_id)

        fts_docs = self._store.search_documents(query, limit=max_docs)
        fts_chunks_by_doc: dict[str, list[RetrievedChunk]] = {}
        fts_doc_order: list[str] = []

        for doc in fts_docs:
            if doc.id in vector_chunks_by_doc:
                for chunk in vector_chunks_by_doc[doc.id]:
                    chunk.retrieval_method = "hybrid"
                continue

            chunks = self._extract_document_chunks(
                doc,
                min_chunk_length=min_chunk_length,
                retrieval_method="fts5",
            )
            if not chunks:
                continue

            fts_chunks_by_doc[doc.id] = chunks
            fts_doc_order.append(doc.id)

        combined: list[RetrievedChunk] = []
        for doc_id in vector_doc_order:
            combined.extend(vector_chunks_by_doc[doc_id])
        for doc_id in fts_doc_order:
            combined.extend(fts_chunks_by_doc[doc_id])

        return combined[:max_chunks]
