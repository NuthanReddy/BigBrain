"""Wiki page generators — create WikiPage objects from KB data."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bigbrain.distill.models import Entity, Relationship, Summary
from bigbrain.kb.models import Document
from bigbrain.wiki.models import WikiPage, PageType
from bigbrain.wiki.slugger import make_slug, make_entity_slug, make_source_slug, title_to_wikilink
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


class EntityPageGenerator:
    """Generates a wiki page for a single entity."""

    def generate(
        self,
        entity: Entity,
        related_entities: list[Entity] | None = None,
        relationships: list[Relationship] | None = None,
        all_entities: dict[str, Entity] | None = None,
    ) -> WikiPage:
        slug = make_entity_slug(entity.name, entity.entity_type)

        sections = []

        # Description
        if entity.description:
            sections.append(f"## Description\n\n{entity.description}")

        # Type badge
        if entity.entity_type:
            sections.append(f"**Type:** {entity.entity_type}")

        # Relationships
        if relationships:
            all_ents = all_entities or {}
            rel_lines = []
            for r in sorted(relationships, key=lambda x: x.relationship_type):
                if r.source_entity_id == entity.id:
                    target = all_ents.get(r.target_entity_id)
                    if target:
                        link = title_to_wikilink(target.name)
                        rel_lines.append(f"- {r.relationship_type.replace('_', ' ')} → {link}")
                elif r.target_entity_id == entity.id:
                    source = all_ents.get(r.source_entity_id)
                    if source:
                        link = title_to_wikilink(source.name)
                        rel_lines.append(f"- {link} → {r.relationship_type.replace('_', ' ')}")
            if rel_lines:
                sections.append("## Relationships\n\n" + "\n".join(rel_lines))

        # Related entities (same type or same document)
        if related_entities:
            see_also = []
            for re_ent in sorted(related_entities, key=lambda x: x.name)[:15]:
                if re_ent.id != entity.id:
                    see_also.append(f"- {title_to_wikilink(re_ent.name)}")
            if see_also:
                sections.append("## See Also\n\n" + "\n".join(see_also))

        content = "\n\n".join(sections)

        return WikiPage(
            slug=slug,
            title=entity.name,
            page_type=PageType.ENTITY,
            content=content,
            entity_type=entity.entity_type,
            tags=[entity.entity_type] if entity.entity_type else [],
            source_doc_ids=[entity.document_id] if entity.document_id else [],
            source_count=1,
        )


class SourcePageGenerator:
    """Generates a wiki page summarizing a source document."""

    def generate(
        self,
        doc: Document,
        summaries: list[Summary] | None = None,
        entities: list[Entity] | None = None,
    ) -> WikiPage:
        slug = make_source_slug(doc.title)

        sections = []

        # Source info
        if doc.source:
            sections.append(f"**Source:** `{doc.source.file_path}`  ")
            sections.append(f"**Type:** {doc.source.source_type}  ")
            sections.append(f"**Size:** {doc.source.size_bytes:,} bytes")

        # Summary
        if summaries:
            sections.append("## Summary\n")
            for s in summaries:
                sections.append(s.content)

        # Key entities from this source
        if entities:
            sections.append("## Key Concepts\n")
            by_type: dict[str, list[Entity]] = {}
            for e in entities:
                by_type.setdefault(e.entity_type, []).append(e)
            for etype, ents in sorted(by_type.items()):
                sections.append(f"### {etype.replace('_', ' ').title()}\n")
                for e in sorted(ents, key=lambda x: x.name)[:20]:
                    sections.append(f"- {title_to_wikilink(e.name)}: {e.description[:100] if e.description else ''}")

        content = "\n\n".join(sections)

        return WikiPage(
            slug=slug,
            title=f"Source: {doc.title}",
            page_type=PageType.SOURCE,
            content=content,
            tags=["source", doc.source.source_type if doc.source else ""],
            source_doc_ids=[doc.id],
            source_count=1,
        )


class OverviewPageGenerator:
    """Generates a wiki overview page listing all sources and top entities."""

    def generate(
        self,
        docs: list[Document],
        all_entities: list[Entity],
    ) -> WikiPage:
        sections = []

        sections.append("Welcome to the BigBrain knowledge wiki. This wiki is auto-generated and maintained from your knowledge base.\n")

        # Sources
        if docs:
            sections.append("## Sources\n")
            for doc in sorted(docs, key=lambda d: d.title):
                link = f"[[{make_source_slug(doc.title)}|{doc.title}]]"
                stype = f" ({doc.source.source_type})" if doc.source else ""
                sections.append(f"- {link}{stype}")

        # Entity stats
        if all_entities:
            by_type: dict[str, int] = {}
            for e in all_entities:
                by_type[e.entity_type] = by_type.get(e.entity_type, 0) + 1

            sections.append("\n## Knowledge Map\n")
            for etype, count in sorted(by_type.items(), key=lambda x: -x[1]):
                sections.append(f"- **{etype.replace('_', ' ').title()}**: {count} entities")

        content = "\n".join(sections)

        return WikiPage(
            slug="overview",
            title="Knowledge Overview",
            page_type=PageType.OVERVIEW,
            content=content,
            tags=["overview", "index"],
            source_count=len(docs),
        )
