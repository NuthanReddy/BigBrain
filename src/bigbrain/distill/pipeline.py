"""Distillation pipeline — orchestrates chunk → summarize → extract → relate.

Supports parallel execution within a document (summarize + extract run
concurrently) and across documents (configurable worker pool).
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, TYPE_CHECKING

from bigbrain.config import BigBrainConfig, DistillConfig, load_config
from bigbrain.distill.chunker import chunk_document
from bigbrain.distill.entities import EntityExtractor
from bigbrain.distill.models import DistillResult
from bigbrain.distill.relationships import RelationshipBuilder
from bigbrain.distill.summarizer import Summarizer
from bigbrain.kb.models import Document
from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger
from bigbrain.progress import progress_bar
from bigbrain.providers.registry import ProviderRegistry

if TYPE_CHECKING:
    from bigbrain.stores.base import EntityStoreBackend

logger = get_logger(__name__)

_DEFAULT_WORKERS = 2


class DistillPipeline:
    """Orchestrates the full distillation pipeline for a document.

    Steps:
    1. Chunk — split document into processable chunks
    2. Summarize + Extract entities — run concurrently
    3. Build relationships — requires entities from step 2
    4. Persist — save all results to KB

    Usage::
        pipeline = DistillPipeline.from_config()
        result = pipeline.distill_document(doc)
        pipeline.close()
    """

    def __init__(
        self,
        store: KBStore,
        registry: ProviderRegistry,
        config: DistillConfig | None = None,
        *,
        workers: int = _DEFAULT_WORKERS,
        entity_store: EntityStoreBackend | None = None,
    ) -> None:
        self._store = store
        self._registry = registry
        self._config = config or DistillConfig()
        self._workers = max(1, workers)
        self._summarizer = Summarizer(registry)
        self._extractor = EntityExtractor(registry)
        self._relationship_builder = RelationshipBuilder(registry)
        self._entity_store = entity_store  # lazy-init to SqliteBackend if None

    @property
    def entity_store(self) -> EntityStoreBackend:
        """Return the configured entity store, defaulting to SqliteBackend."""
        if self._entity_store is None:
            from bigbrain.stores.sqlite_backend import SqliteBackend
            self._entity_store = SqliteBackend(self._store)
        return self._entity_store

    @classmethod
    def from_config(cls, config: BigBrainConfig | None = None) -> DistillPipeline:
        """Create pipeline from application config."""
        if config is None:
            config = load_config()
        store = KBStore(config.kb_db_path)
        registry = ProviderRegistry.from_config(config.providers)
        from bigbrain.stores.factory import create_entity_store
        entity_backend = create_entity_store(config.entity_store, store)
        return cls(
            store=store, registry=registry, config=config.distillation,
            entity_store=entity_backend,
        )

    def close(self) -> None:
        if self._entity_store is not None:
            self._entity_store.close()
        self._store.close()

    def __enter__(self) -> DistillPipeline:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def distill_document(
        self,
        doc: Document,
        *,
        model: str = "",
        force: bool = False,
        steps: set[str] | None = None,
    ) -> DistillResult:
        """Run the distillation pipeline on a document.
        
        Args:
            doc: Document to distill
            model: Override AI model
            force: If True, re-distill all chunks even if unchanged
            steps: If set, run only these steps: {"chunk", "summarize", "entities", "relationships"}
                   If None, run all steps.
        """
        run_all = steps is None
        steps = steps or {"chunk", "summarize", "entities", "relationships"}

        result = DistillResult(document_id=doc.id)

        # Step 1: Chunk (always needed as input for other steps)
        logger.info("Chunking document: %s", doc.title)
        chunks = chunk_document(
            doc,
            strategy=self._config.chunk_strategy,
            chunk_size=self._config.chunk_size,
            overlap=self._config.chunk_overlap,
            max_chunks=self._config.max_chunks_per_doc,
        )
        result.chunks = chunks
        logger.info("  → %d chunks", len(chunks))

        if not chunks:
            logger.warning("No chunks produced for document %s", doc.id)
            return result

        # Incremental check — filter to only changed chunks
        chunks_to_process = chunks
        if not force and run_all:
            existing_hashes = self._store.get_chunk_hashes(doc.id)
            if existing_hashes:
                chunks_to_process = [
                    c for c in chunks
                    if existing_hashes.get(c.chunk_index) != c.content_hash
                ]
                skipped = len(chunks) - len(chunks_to_process)
                if skipped > 0:
                    logger.info("  → %d unchanged chunks skipped (incremental)", skipped)

        if not chunks_to_process and run_all:
            logger.info("All chunks unchanged for %s — skipping AI calls", doc.title)
            self._store.save_chunks(chunks)
            return result

        # Step 2: Summarize + Extract entities in parallel
        do_summarize = "summarize" in steps
        do_entities = "entities" in steps and self._config.entity_extraction

        # Load existing entity names for dedup in incremental mode
        existing_names: set[str] = set()
        if do_entities and not force:
            existing = self.entity_store.get_entities(doc.id)
            existing_names = {" ".join(e.name.lower().strip().split()) for e in existing}

        with ThreadPoolExecutor(max_workers=2) as pool:
            summary_future = None
            entity_future = None

            if do_summarize:
                summary_future = pool.submit(self._run_summarize, doc, model)
            if do_entities:
                entity_future = pool.submit(
                    self._run_entity_extraction, chunks_to_process, model, existing_names,
                )

            if summary_future is not None:
                summaries, sum_errors = summary_future.result()
                result.summaries = summaries
                result.errors.extend(sum_errors)
                if summaries:
                    result.provider = summaries[0].generated_by_provider
                    result.model = summaries[0].generated_by_model

            if entity_future is not None:
                entities, ent_errors = entity_future.result()
                result.entities = entities
                result.errors.extend(ent_errors)

        # Step 3: Build relationships
        do_relationships = "relationships" in steps and self._config.relationship_extraction
        if do_relationships:
            # Load existing entities from KB if we didn't extract fresh ones
            entities_for_rels = result.entities
            if not entities_for_rels and "entities" not in steps:
                entities_for_rels = self.entity_store.get_entities(doc.id)
                logger.info("Loaded %d existing entities from KB", len(entities_for_rels))

            if entities_for_rels:
                logger.info("Building relationships for %d entities", len(entities_for_rels))
                try:
                    relationships = self._relationship_builder.build_relationships(
                        entities_for_rels, document_id=doc.id, model=model
                    )
                    result.relationships = relationships
                    logger.info("  → %d relationships", len(relationships))
                except Exception as exc:
                    logger.warning("Relationship extraction failed: %s", exc)
                    result.errors.append(f"relationship_extraction: {exc}")

        # Step 4: Persist
        logger.info("Persisting distillation results to KB")
        self._store.save_chunks(chunks)
        if result.summaries:
            self._store.save_summaries(result.summaries)
        if result.entities:
            self.entity_store.save_entities(result.entities)
        if result.relationships:
            self.entity_store.save_relationships(result.relationships)

        return result

    def _run_summarize(self, doc: Document, model: str) -> tuple[list, list]:
        """Summarize document. Returns (summaries, errors)."""
        logger.info("Summarizing document: %s", doc.title)
        try:
            doc_summary = self._summarizer.summarize_document(
                doc, max_length=self._config.summary_max_length, model=model
            )
            return [doc_summary], []
        except Exception as exc:
            logger.warning("Document summarization failed: %s", exc)
            return [], [f"summarization: {exc}"]

    def _run_entity_extraction(self, chunks: list, model: str, existing_names: set[str] | None = None) -> tuple[list, list]:
        """Extract entities from chunks. Returns (entities, errors)."""
        logger.info("Extracting entities from %d chunks", len(chunks))
        try:
            entities = self._extractor.extract_from_chunks(
                chunks, model=model, existing_names=existing_names,
            )
            logger.info("  → %d entities", len(entities))
            return entities, []
        except Exception as exc:
            logger.warning("Entity extraction failed: %s", exc)
            return [], [f"entity_extraction: {exc}"]

    def distill_by_id(self, document_id: str, *, model: str = "", force: bool = False, steps: set[str] | None = None) -> DistillResult | None:
        """Distill a document by its KB ID."""
        doc = self._store.get_document(document_id)
        if doc is None:
            logger.warning("Document not found: %s", document_id)
            return None
        return self.distill_document(doc, model=model, force=force, steps=steps)

    def distill_all(
        self, *, model: str = "", source_type: str | None = None, force: bool = False, steps: set[str] | None = None,
    ) -> list[DistillResult]:
        """Distill all documents in the KB, processing multiple docs concurrently."""
        docs = self._store.list_documents(source_type=source_type, limit=9999)
        if not docs:
            return []

        results: list[DistillResult] = []

        if self._workers <= 1 or len(docs) == 1:
            with progress_bar(len(docs), "Distilling") as update:
                for doc in docs:
                    try:
                        results.append(self.distill_document(doc, model=model, force=force, steps=steps))
                    except Exception as exc:
                        logger.error("Failed to distill %s: %s", doc.title, exc)
                        results.append(DistillResult(document_id=doc.id, errors=[str(exc)]))
                    update(1)
            return results

        with ThreadPoolExecutor(max_workers=self._workers) as pool:
            future_to_doc = {
                pool.submit(self._distill_safe, doc, model, force, steps): doc
                for doc in docs
            }
            for future in as_completed(future_to_doc):
                results.append(future.result())

        return results

    def _distill_safe(self, doc: Document, model: str, force: bool = False, steps: set[str] | None = None) -> DistillResult:
        """Distill with error wrapping for thread pool."""
        try:
            return self.distill_document(doc, model=model, force=force, steps=steps)
        except Exception as exc:
            logger.error("Failed to distill %s: %s", doc.title, exc)
            return DistillResult(document_id=doc.id, errors=[str(exc)])
