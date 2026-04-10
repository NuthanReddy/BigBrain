"""Wiki page generators — create WikiPage objects from KB data.

Generates **concept pages** (one per high-level concept or topic) that
group related entities (algorithms, data structures, theorems, etc.)
as sections within the page.  Source pages and the overview page remain
as before.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

from bigbrain.distill.models import Entity, Relationship, Summary
from bigbrain.kb.models import Document
from bigbrain.wiki.models import WikiPage, PageType
from bigbrain.wiki.slugger import make_slug, make_entity_slug, make_source_slug, title_to_wikilink
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)

_EXPAND_SYSTEM = (
    "You are a knowledgeable technical writer. "
    "Write clear, detailed explanations of concepts, algorithms, and definitions."
)

_EXPAND_TEMPLATE = (
    "Write 2-4 paragraphs explaining the following {entity_type} in detail:\n\n"
    "Name: {name}\n"
    "Brief description: {description}\n"
    "{details_section}"
    "\nExplanation:"
)

# Entity types that get their own wiki page (concepts = top-level topics)
CONCEPT_TYPES = {"concept", "topic"}

# Entity types grouped as subsections within a concept page
SUBSECTION_TYPES = {
    "algorithm", "data_structure", "theorem", "definition",
    "technique", "property", "formula", "person", "example", "other",
}


def group_entities_into_concepts(
    entities: list[Entity],
    relationships: list[Relationship],
) -> dict[str, list[Entity]]:
    """Group entities into concept clusters.

    Strategy:
    1. Entities with type 'concept' become cluster heads.
    2. Other entities are assigned to the concept they're related to
       (via relationships or metadata 'related' field).
    3. Unrelated entities are grouped under their source document title.
    """
    concepts: dict[str, Entity] = {}
    non_concepts: list[Entity] = []

    for e in entities:
        if e.entity_type in CONCEPT_TYPES:
            concepts[e.id] = e
        else:
            non_concepts.append(e)

    # Build name→concept_id lookup
    concept_by_name: dict[str, str] = {}
    for cid, c in concepts.items():
        concept_by_name[c.name.lower().strip()] = cid

    # Build relationship mapping: entity_id → set of related entity_ids
    rel_map: dict[str, set[str]] = defaultdict(set)
    for r in relationships:
        rel_map[r.source_entity_id].add(r.target_entity_id)
        rel_map[r.target_entity_id].add(r.source_entity_id)

    # Assign non-concepts to their best concept
    clusters: dict[str, list[Entity]] = {cid: [] for cid in concepts}
    unclustered: list[Entity] = []

    for e in non_concepts:
        assigned = False

        # 1. Check relationships to a concept
        for related_id in rel_map.get(e.id, set()):
            if related_id in concepts:
                clusters[related_id].append(e)
                assigned = True
                break

        # 2. Check metadata 'related' names
        if not assigned and e.metadata:
            for name in e.metadata.get("related", []):
                key = name.lower().strip()
                if key in concept_by_name:
                    clusters[concept_by_name[key]].append(e)
                    assigned = True
                    break

        if not assigned:
            unclustered.append(e)

    # 3. Group unclustered by document_id
    unclustered_by_doc: dict[str, list[Entity]] = defaultdict(list)
    for e in unclustered:
        unclustered_by_doc[e.document_id].append(e)

    # Build final result: concept_name → entity list (including the concept itself)
    result: dict[str, list[Entity]] = {}
    for cid, concept_entity in concepts.items():
        members = [concept_entity] + clusters.get(cid, [])
        result[concept_entity.name] = members

    # Unclustered entities: group by type to form synthetic concept pages
    if unclustered:
        by_type: dict[str, list[Entity]] = defaultdict(list)
        for e in unclustered:
            by_type[e.entity_type].append(e)
        for etype, ents in by_type.items():
            page_name = f"{etype.replace('_', ' ').title()}s"
            result[page_name] = ents

    return result


_PAGE_SYSTEM = (
    "You are an expert technical writer creating a comprehensive wiki page. "
    "Write detailed, well-structured Markdown content. "
    "Use ## for major sections and ### for subsections. "
    "Explain concepts thoroughly — each entity should get at least a full paragraph. "
    "Include examples, trade-offs, time/space complexity for algorithms, "
    "formal definitions for theorems, and key operations for data structures. "
    "Cross-reference related concepts using [[wikilink]] syntax."
)

_PAGE_TEMPLATE = '''Write a comprehensive wiki page about "{concept_name}".

The page should cover these entities in depth (don't just list them — explain each one with 1-3 paragraphs):

{entity_list}

Requirements:
- Start with a ## Overview section explaining the concept broadly
- Group related entities under ## sections by type (Algorithms, Data Structures, Theorems, etc.)
- Each entity gets a ### subsection with detailed explanation (not one-liners)
- For algorithms: explain how they work, time/space complexity, when to use them
- For data structures: explain key operations, properties, use cases
- For theorems/definitions: state the theorem formally, explain its significance
- For techniques: explain the approach, when to apply it, trade-offs
- End with a ## Related Topics section linking to related concepts using [[concept name]]
- Write in Markdown format
- Be thorough — aim for a reference-quality wiki page

Wiki page:'''

_PAGE_TEMPLATE_WITH_SOURCE = '''Write a comprehensive wiki page about "{concept_name}".

Here are the key entities to cover:
{entity_list}

Here is the actual source text from the original documents about this topic:

{source_text}

Requirements:
- Start with a ## Overview section explaining the concept broadly using the source material
- Group entities under ## sections by type (Algorithms, Data Structures, Theorems, etc.)
- Each entity gets a ### subsection — use the SOURCE TEXT to write detailed, accurate explanations (not just summaries)
- For algorithms: explain how they work step by step, include pseudocode if in the source, time/space complexity
- For data structures: explain key operations, properties, use cases from the source
- For theorems/definitions: state them formally as given in the source, explain significance
- Include concrete examples from the source text where available
- End with a ## Related Topics section using [[concept name]] wikilinks
- Write in Markdown format
- Preserve the technical depth and accuracy of the original source material

Wiki page:'''


class ConceptPageGenerator:
    """Generates a comprehensive wiki page for a concept with all related entities."""

    def __init__(self, registry: Any | None = None) -> None:
        self._registry = registry

    def _build_entity_list(self, members: list[Entity]) -> str:
        """Build a structured entity list for the AI prompt."""
        by_type: dict[str, list[Entity]] = defaultdict(list)
        for e in members:
            by_type[e.entity_type].append(e)

        lines: list[str] = []
        for etype in sorted(by_type.keys()):
            ents = sorted(by_type[etype], key=lambda x: x.name)
            type_title = etype.replace("_", " ").title()
            lines.append(f"\n{type_title}:")
            for e in ents:
                desc = e.description or "No description"
                details = ""
                if e.metadata:
                    d = e.metadata.get("details", "")
                    if d:
                        details = f" | Details: {d}"
                    related = e.metadata.get("related", [])
                    if related:
                        details += f" | Related: {', '.join(related[:5])}"
                lines.append(f"  - {e.name}: {desc}{details}")
        return "\n".join(lines)

    def _generate_with_ai(
        self, concept_name: str, members: list[Entity],
        source_chunks: list[Any] | None = None, *, model: str = "",
    ) -> str:
        """Use AI to write a full concept wiki page from entities + source text."""
        if self._registry is None:
            return ""

        entity_list = self._build_entity_list(members)

        # Include actual source text from chunks (the real knowledge)
        source_text = ""
        if source_chunks:
            chunk_texts = []
            for c in source_chunks[:10]:  # cap to avoid token overflow
                title = getattr(c, "section_title", "") or ""
                text = getattr(c, "content", "") or ""
                if text.strip():
                    header = f"[{title}] " if title else ""
                    chunk_texts.append(f"{header}{text[:3000]}")
            if chunk_texts:
                source_text = "\n\n---\n\n".join(chunk_texts)

        if source_text:
            prompt = _PAGE_TEMPLATE_WITH_SOURCE.format(
                concept_name=concept_name,
                entity_list=entity_list,
                source_text=source_text[:15000],  # cap total prompt size
            )
        else:
            prompt = _PAGE_TEMPLATE.format(
                concept_name=concept_name,
                entity_list=entity_list,
            )

        messages = [
            {"role": "system", "content": _PAGE_SYSTEM},
            {"role": "user", "content": prompt},
        ]
        try:
            resp = self._registry.chat(messages, model=model, max_tokens=4000)
            return resp.text.strip()
        except Exception as exc:
            logger.warning("AI page generation failed for '%s': %s", concept_name, exc)
            return ""

    def _generate_static(
        self, concept_name: str, members: list[Entity],
        relationships: list[Relationship] | None = None,
        all_entities: dict[str, Entity] | None = None,
        source_chunks: list[Any] | None = None,
    ) -> str:
        """Generate page content without AI, using entity data + source chunks."""
        sections: list[str] = []

        # Build chunk lookup: chunk_id → content
        chunk_by_id: dict[str, str] = {}
        if source_chunks:
            for c in source_chunks:
                cid = getattr(c, "id", "")
                content = getattr(c, "content", "")
                if cid and content:
                    chunk_by_id[cid] = content

        # Find concept entity for overview
        concept_entity = None
        sub_entities: list[Entity] = []
        for e in members:
            if e.entity_type in CONCEPT_TYPES and e.name == concept_name:
                concept_entity = e
            else:
                sub_entities.append(e)

        if concept_entity:
            overview_parts: list[str] = []
            if concept_entity.description:
                overview_parts.append(concept_entity.description)
            details = concept_entity.metadata.get("details", "") if concept_entity.metadata else ""
            if details:
                overview_parts.append(details)
            # Include source text from the chunk this concept was extracted from
            if concept_entity.source_chunk_id and concept_entity.source_chunk_id in chunk_by_id:
                overview_parts.append(chunk_by_id[concept_entity.source_chunk_id][:2000])
            if overview_parts:
                sections.append("## Overview\n\n" + "\n\n".join(overview_parts))

        # Group by type with full content from chunks
        by_type: dict[str, list[Entity]] = defaultdict(list)
        for e in sub_entities:
            by_type[e.entity_type].append(e)

        for etype in sorted(by_type.keys()):
            ents = sorted(by_type[etype], key=lambda x: x.name)
            type_title = etype.replace("_", " ").title() + "s"
            type_parts: list[str] = []

            for e in ents:
                parts: list[str] = [f"### {e.name}\n"]
                if e.description:
                    parts.append(e.description)
                details = e.metadata.get("details", "") if e.metadata else ""
                if details:
                    parts.append(f"\n{details}")

                # Include actual source text from the chunk
                if e.source_chunk_id and e.source_chunk_id in chunk_by_id:
                    chunk_text = chunk_by_id[e.source_chunk_id][:2000]
                    parts.append(f"\n{chunk_text}")

                meta_related = e.metadata.get("related", []) if e.metadata else []
                if meta_related:
                    links = ", ".join(title_to_wikilink(n) for n in meta_related[:5])
                    parts.append(f"\n**Related:** {links}")
                type_parts.append("\n".join(parts))

            sections.append(f"## {type_title}\n\n" + "\n\n".join(type_parts))

        # Cross-concept relationships
        if relationships and all_entities:
            member_ids = {e.id for e in members}
            rel_lines: list[str] = []
            for r in relationships:
                if r.source_entity_id in member_ids:
                    target = all_entities.get(r.target_entity_id)
                    if target and target.id not in member_ids:
                        rel_lines.append(f"- {title_to_wikilink(target.name)}")
                elif r.target_entity_id in member_ids:
                    source = all_entities.get(r.source_entity_id)
                    if source and source.id not in member_ids:
                        rel_lines.append(f"- {title_to_wikilink(source.name)}")
            if rel_lines:
                rel_lines = sorted(set(rel_lines))[:20]
                sections.append("## Related Topics\n\n" + "\n".join(rel_lines))

        return "\n\n".join(sections)

    def generate(
        self,
        concept_name: str,
        members: list[Entity],
        relationships: list[Relationship] | None = None,
        all_entities: dict[str, Entity] | None = None,
        source_chunks: list[Any] | None = None,
        *,
        enrich: bool = False,
        model: str = "",
    ) -> WikiPage:
        slug = make_entity_slug(concept_name, "concept")

        # If enrich is on, ask AI to write the entire page using chunk content
        if enrich and self._registry is not None:
            content = self._generate_with_ai(
                concept_name, members, source_chunks=source_chunks, model=model,
            )
            if not content:
                content = self._generate_static(
                    concept_name, members, relationships, all_entities,
                    source_chunks=source_chunks,
                )
        else:
            content = self._generate_static(
                concept_name, members, relationships, all_entities,
                source_chunks=source_chunks,
            )

        all_types = sorted(set(e.entity_type for e in members if e.entity_type))
        all_doc_ids = sorted(set(e.document_id for e in members if e.document_id))

        return WikiPage(
            slug=slug,
            title=concept_name,
            page_type=PageType.TOPIC,
            content=content,
            entity_type="concept",
            tags=all_types,
            source_doc_ids=all_doc_ids,
            source_count=len(all_doc_ids),
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
        doc_summaries = []
        section_summaries = []
        if summaries:
            for s in summaries:
                if s.summary_type == "section":
                    section_summaries.append(s)
                else:
                    doc_summaries.append(s)

        if doc_summaries:
            sections.append("## Summary\n")
            for s in doc_summaries:
                sections.append(s.content)

        # Section-level summaries
        if section_summaries:
            sections.append("## Section Summaries\n")
            for s in sorted(section_summaries, key=lambda x: x.metadata.get("section_index", 0)):
                title = s.metadata.get("section_title", "Untitled section")
                sections.append(f"### {title}\n")
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
