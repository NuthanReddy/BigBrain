"""Cheatsheet compiler — concise reference sheet from distilled entities."""

from __future__ import annotations

from bigbrain.compile.models import CompileOutput, OutputFormat
from bigbrain.distill.models import Entity, Relationship
from bigbrain.kb.models import Document
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


class CheatsheetCompiler:
    """Compiles entities into a concise cheatsheet."""

    def compile(
        self,
        doc: Document,
        entities: list[Entity],
        relationships: list[Relationship] | None = None,
    ) -> CompileOutput:
        """Render a cheatsheet from entities."""
        lines = [f"# Cheatsheet: {doc.title}\n"]

        if not entities:
            lines.append("*No entities extracted yet. Run `bigbrain distill` first.*")
            return CompileOutput(
                format=OutputFormat.CHEATSHEET,
                title=f"{doc.title} — Cheatsheet",
                content="\n".join(lines),
                source_doc_id=doc.id,
                source_doc_title=doc.title,
            )

        # Group by type
        by_type: dict[str, list[Entity]] = {}
        for e in entities:
            by_type.setdefault(e.entity_type, []).append(e)

        # Render each type
        type_order = [
            "algorithm",
            "data_structure",
            "theorem",
            "technique",
            "concept",
            "definition",
            "property",
            "person",
            "other",
        ]
        rendered_types = set()

        for etype in type_order:
            if etype in by_type:
                self._render_type(lines, etype, by_type[etype])
                rendered_types.add(etype)

        # Any remaining types not in the order
        for etype in sorted(by_type.keys()):
            if etype not in rendered_types:
                self._render_type(lines, etype, by_type[etype])

        # Quick relationship reference
        if relationships:
            entity_map = {e.id: e.name for e in entities}
            lines.append("---\n")
            lines.append("## Quick Reference: Relationships\n")
            for r in relationships[:30]:
                src = entity_map.get(r.source_entity_id, "?")
                tgt = entity_map.get(r.target_entity_id, "?")
                lines.append(
                    f"- **{src}** {r.relationship_type.replace('_', ' ')} **{tgt}**"
                )
            lines.append("")

        return CompileOutput(
            format=OutputFormat.CHEATSHEET,
            title=f"{doc.title} — Cheatsheet",
            content="\n".join(lines),
            source_doc_id=doc.id,
            source_doc_title=doc.title,
        )

    @staticmethod
    def _render_type(lines: list[str], etype: str, entities: list[Entity]) -> None:
        header = etype.replace("_", " ").title()
        lines.append(f"## {header}\n")
        for e in sorted(entities, key=lambda x: x.name):
            if e.description:
                lines.append(f"- **{e.name}**: {e.description}")
            else:
                lines.append(f"- **{e.name}**")
        lines.append("")
