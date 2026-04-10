"""Wiki builder — orchestrates page generation, linking, and writing."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from bigbrain.config import BigBrainConfig, load_config
from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger
from bigbrain.wiki.generators import EntityPageGenerator, SourcePageGenerator, OverviewPageGenerator
from bigbrain.wiki.linker import WikiLinker, LinkGraph
from bigbrain.wiki.models import WikiPage
from bigbrain.wiki.writer import WikiWriter

logger = get_logger(__name__)

_DEFAULT_WIKI_DIR = "wiki"


@dataclass
class WikiBuildResult:
    """Result of a wiki build operation."""
    total_pages: int = 0
    written: int = 0
    skipped_unchanged: int = 0
    entity_pages: int = 0
    source_pages: int = 0
    total_links: int = 0
    orphan_pages: int = 0
    errors: list[str] = field(default_factory=list)


class WikiBuilder:
    """Orchestrates wiki generation from the knowledge base.

    Usage::
        builder = WikiBuilder.from_config()
        result = builder.build()
        builder.close()
    """

    def __init__(
        self,
        store: KBStore,
        wiki_dir: str | Path = _DEFAULT_WIKI_DIR,
        registry: Any | None = None,
    ) -> None:
        self._store = store
        self._writer = WikiWriter(wiki_dir)
        self._registry = registry
        self._entity_gen = EntityPageGenerator(registry=registry)
        self._source_gen = SourcePageGenerator()
        self._overview_gen = OverviewPageGenerator()

    @classmethod
    def from_config(cls, config: BigBrainConfig | None = None) -> WikiBuilder:
        if config is None:
            config = load_config()
        store = KBStore(config.kb_db_path)
        registry = None
        try:
            from bigbrain.providers.registry import ProviderRegistry
            registry = ProviderRegistry.from_app_config(config)
        except Exception as exc:
            logger.debug("Could not create ProviderRegistry for wiki enrichment: %s", exc)
        return cls(store=store, registry=registry)

    def close(self) -> None:
        self._store.close()

    def __enter__(self) -> WikiBuilder:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def build(
        self,
        *,
        doc_id: str = "",
        clean: bool = False,
        dry_run: bool = False,
        enrich: bool = False,
        model: str = "",
    ) -> WikiBuildResult:
        """Build the complete wiki from KB data.

        Args:
            doc_id: If set, only build pages related to this document.
            clean: Remove wiki files not in the generated set.
            dry_run: Generate pages but don't write to disk.
            enrich: Use AI to expand entity descriptions on wiki pages.
            model: Override AI model for enrichment.
        """
        result = WikiBuildResult()
        pages: list[WikiPage] = []

        # Load KB data
        if doc_id:
            docs = [self._store.get_document(doc_id)]
            docs = [d for d in docs if d is not None]
        else:
            docs = self._store.list_documents(limit=9999)

        if not docs:
            logger.warning("No documents in KB — nothing to build")
            return result

        # Collect all entities and relationships across docs
        all_entities: dict[str, Any] = {}
        all_relationships: list[Any] = []
        doc_entities: dict[str, list[Any]] = {}
        doc_summaries: dict[str, list[Any]] = {}

        for doc in docs:
            entities = self._store.get_entities(doc.id)
            summaries = self._store.get_summaries(doc.id)
            relationships = self._store.get_relationships(doc.id)

            doc_entities[doc.id] = entities
            doc_summaries[doc.id] = summaries
            all_relationships.extend(relationships)

            for e in entities:
                all_entities[e.id] = e

        logger.info("Building wiki: %d docs, %d entities, %d relationships",
                     len(docs), len(all_entities), len(all_relationships))

        # Generate entity pages
        seen_slugs: set[str] = set()
        for entity in sorted(all_entities.values(), key=lambda e: e.name.lower()):
            try:
                entity_rels = [r for r in all_relationships
                               if r.source_entity_id == entity.id or r.target_entity_id == entity.id]
                related = [e for e in all_entities.values()
                           if e.document_id == entity.document_id and e.id != entity.id][:15]

                page = self._entity_gen.generate(
                    entity,
                    related_entities=related,
                    relationships=entity_rels,
                    all_entities=all_entities,
                    enrich=enrich,
                    model=model,
                )

                if page.slug not in seen_slugs:
                    pages.append(page)
                    seen_slugs.add(page.slug)
                    result.entity_pages += 1
            except Exception as exc:
                result.errors.append(f"entity '{entity.name}': {exc}")
                logger.warning("Failed to generate entity page for %s: %s", entity.name, exc)

        # Generate source pages
        for doc in sorted(docs, key=lambda d: d.title.lower()):
            try:
                page = self._source_gen.generate(
                    doc,
                    summaries=doc_summaries.get(doc.id, []),
                    entities=doc_entities.get(doc.id, []),
                )
                if page.slug not in seen_slugs:
                    pages.append(page)
                    seen_slugs.add(page.slug)
                    result.source_pages += 1
            except Exception as exc:
                result.errors.append(f"source '{doc.title}': {exc}")

        # Generate overview page
        all_entity_list = sorted(all_entities.values(), key=lambda e: e.name.lower())
        overview = self._overview_gen.generate(docs, all_entity_list)
        if overview.slug not in seen_slugs:
            pages.append(overview)
            seen_slugs.add(overview.slug)

        result.total_pages = len(pages)

        # Cross-link pages
        linker = WikiLinker(pages)
        graph = linker.link_pages()
        result.total_links = graph.total_edges
        result.orphan_pages = len(graph.get_orphans(seen_slugs))

        logger.info("Wiki: %d pages, %d links, %d orphans",
                     result.total_pages, result.total_links, result.orphan_pages)

        # Write to disk
        if not dry_run:
            written, skipped = self._writer.write_all(pages, clean=clean)
            result.written = written
            result.skipped_unchanged = skipped
            logger.info("Written: %d, unchanged: %d", written, skipped)
        else:
            result.written = 0
            result.skipped_unchanged = len(pages)
            logger.info("Dry run: %d pages would be written", len(pages))

        return result
