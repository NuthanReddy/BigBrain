"""Knowledge base service — high-level API for KB operations.

Provides :class:`KBService` as the primary interface for later pipeline
phases (distill, compile, orchestrator) to interact with stored documents.
Wraps :class:`KBStore` and adds convenience methods.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from bigbrain.config import BigBrainConfig, load_config
from bigbrain.kb.models import Document, IngestionResult
from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


class KBService:
    """High-level knowledge base service.

    Usage::

        svc = KBService.from_config()
        svc.store_ingestion_result(result, source_path="/docs")
        docs = svc.search("algorithms")
        stats = svc.get_stats()
        svc.close()

    Or as context manager::

        with KBService.from_config() as svc:
            svc.store_ingestion_result(result)
    """

    def __init__(self, store: KBStore) -> None:
        self._store = store

    @classmethod
    def from_config(cls, config: BigBrainConfig | None = None) -> KBService:
        """Create a KBService from application config.

        Loads config if not provided, resolves the DB path, and opens
        the underlying KBStore.
        """
        if config is None:
            config = load_config()
        store = KBStore(config.kb_db_path)
        return cls(store)

    def close(self) -> None:
        """Close the underlying store."""
        self._store.close()

    def __enter__(self) -> KBService:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Ingestion integration
    # ------------------------------------------------------------------

    def store_ingestion_result(
        self, result: IngestionResult, source_path: str = ""
    ) -> tuple[int, str]:
        """Persist all documents from an ingestion result and record the run.

        Returns:
            tuple of (stored_count, run_id)
        """
        stored = 0
        for doc in result.documents:
            try:
                self._store.save_document(doc)
                stored += 1
            except Exception as exc:
                logger.warning(
                    "Failed to store document %s: %s", doc.title, exc
                )

        run_id = self._store.save_ingestion_run(
            result, source_path=source_path
        )
        logger.info(
            "Stored %d/%d documents, run_id=%s",
            stored,
            len(result.documents),
            run_id,
        )
        return stored, run_id

    # ------------------------------------------------------------------
    # Document access
    # ------------------------------------------------------------------

    def get_document(self, doc_id: str) -> Document | None:
        """Retrieve a document by ID."""
        return self._store.get_document(doc_id)

    def get_document_by_path(self, file_path: str) -> Document | None:
        """Retrieve a document by its source file path."""
        return self._store.get_document_by_source_path(file_path)

    def list_documents(
        self,
        source_type: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Document]:
        """List documents with optional filtering."""
        return self._store.list_documents(
            source_type=source_type, limit=limit, offset=offset
        )

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document by ID."""
        return self._store.delete_document(doc_id)

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, query: str, limit: int = 20) -> list[Document]:
        """Full-text search over the knowledge base."""
        return self._store.search_documents(query, limit=limit)

    # ------------------------------------------------------------------
    # Stats & reporting
    # ------------------------------------------------------------------

    def get_stats(self) -> dict:
        """Return aggregate KB statistics."""
        return self._store.get_stats()

    def list_ingestion_runs(self, limit: int = 10) -> list[dict]:
        """List recent ingestion runs."""
        return self._store.list_ingestion_runs(limit=limit)

    # ------------------------------------------------------------------
    # Export / Import
    # ------------------------------------------------------------------

    def export_jsonl(self, output_path: str | Path) -> int:
        """Export all documents to JSONL format.

        Each line is a JSON object with keys: ``id``, ``title``,
        ``content``, ``language``, ``source``, ``sections``, ``metadata``.

        Returns the number of documents written.
        """
        return self._store.export_jsonl(output_path)

    def import_jsonl(
        self, input_path: str | Path, *, upsert: bool = True
    ) -> tuple[int, int]:
        """Import documents from JSONL format.

        Each line must be a JSON object compatible with the format
        produced by :meth:`export_jsonl`.

        Args:
            input_path: Path to the JSONL file.
            upsert: When *True* (default), existing documents are updated.
                When *False*, lines whose source path already exists are
                skipped.

        Returns:
            tuple of (imported_count, skipped_count)
        """
        return self._store.import_jsonl(input_path, upsert=upsert)

    # ------------------------------------------------------------------
    # Existence / readiness checks
    # ------------------------------------------------------------------

    @staticmethod
    def db_exists(config: BigBrainConfig | None = None) -> bool:
        """Check whether the KB database file exists."""
        if config is None:
            config = load_config()
        return Path(config.kb_db_path).exists()
