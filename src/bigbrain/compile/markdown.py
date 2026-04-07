"""Markdown compiler — renders distilled content into structured markdown."""

from __future__ import annotations

from bigbrain.compile.models import CompileOutput, OutputFormat
from bigbrain.distill.models import Entity, Relationship, Summary
from bigbrain.kb.models import Document
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


class MarkdownCompiler:
    """Compiles distilled content into a structured markdown document."""

    def compile(
        self,
        doc: Document,
        summaries: list[Summary],
        entities: list[Entity],
        relationships: list[Relationship],
    ) -> CompileOutput:
        """Render markdown from distilled content."""
        parts: list[str] = []

        # Title
        parts.append(f"# {doc.title}\n")

        # Source info
        if doc.source:
            parts.append(
                f"*Source: {doc.source.file_path} ({doc.source.source_type})*\n"
            )

        # Summary section
        if summaries:
            parts.append("## Summary\n")
            for s in summaries:
                parts.append(f"{s.content}\n")

        # Entities grouped by type
        if entities:
            parts.append("## Key Concepts\n")
            by_type: dict[str, list[Entity]] = {}
            for e in entities:
                by_type.setdefault(e.entity_type, []).append(e)

            for etype, ents in sorted(by_type.items()):
                parts.append(f"### {etype.replace('_', ' ').title()}\n")
                for e in sorted(ents, key=lambda x: x.name):
                    desc = f" — {e.description}" if e.description else ""
                    parts.append(f"- **{e.name}**{desc}")
                parts.append("")

        # Relationships
        if relationships:
            entity_map = {e.id: e.name for e in entities}
            parts.append("## Relationships\n")
            for r in relationships:
                src = entity_map.get(r.source_entity_id, "?")
                tgt = entity_map.get(r.target_entity_id, "?")
                parts.append(f"- {src} → *{r.relationship_type}* → {tgt}")
                if r.description:
                    parts.append(f"  - {r.description}")
            parts.append("")

        content = "\n".join(parts)

        return CompileOutput(
            format=OutputFormat.MARKDOWN,
            title=f"{doc.title} — Summary",
            content=content,
            source_doc_id=doc.id,
            source_doc_title=doc.title,
        )
