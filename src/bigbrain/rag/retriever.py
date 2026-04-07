"""Retrieval stage — searches KB and extracts relevant chunks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from bigbrain.kb.models import Document, DocumentSection
from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class RetrievedChunk:
    """A chunk of text retrieved from the KB with provenance."""
    text: str
    source_title: str
    source_path: str
    section_title: str = ""
    score: float = 0.0  # relevance ranking (lower = more relevant in FTS5)


class Retriever:
    """Retrieves and chunks relevant content from the knowledge base."""

    def __init__(self, store: KBStore) -> None:
        self._store = store

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
            source_path = doc.source.file_path if doc.source else ""

            if doc.sections:
                for sec in doc.sections:
                    text = sec.content.strip()
                    if len(text) >= min_chunk_length:
                        chunks.append(RetrievedChunk(
                            text=text,
                            source_title=doc.title,
                            source_path=source_path,
                            section_title=sec.title,
                        ))
            elif doc.content.strip():
                # No sections — use content directly (truncate if huge)
                text = doc.content.strip()[:5000]
                chunks.append(RetrievedChunk(
                    text=text,
                    source_title=doc.title,
                    source_path=source_path,
                ))

        return chunks[:max_chunks]
