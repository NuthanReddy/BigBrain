"""Study guide compiler — AI-powered comprehensive study guide."""

from __future__ import annotations

from bigbrain.compile.models import CompileOutput, OutputFormat
from bigbrain.distill.models import Entity, Relationship, Summary
from bigbrain.kb.models import Document
from bigbrain.logging_config import get_logger
from bigbrain.providers.registry import ProviderRegistry

logger = get_logger(__name__)

STUDY_GUIDE_SYSTEM = "You are an expert educator creating comprehensive study guides. Be thorough but clear."

STUDY_GUIDE_TEMPLATE = '''Create a comprehensive study guide for the following content.

Title: {title}

Summary:
{summary}

Key Concepts ({entity_count}):
{entities_text}

Relationships:
{relationships_text}

Generate a well-structured study guide with these sections:
1. **Overview** — 2-3 paragraph introduction
2. **Core Concepts** — Explain each major concept clearly
3. **How They Connect** — Describe how concepts relate
4. **Common Pitfalls** — Mistakes to avoid
5. **Review Questions** — 5 questions to test understanding

Study Guide:'''


class StudyGuideCompiler:
    """Compiles a comprehensive study guide using AI."""

    def __init__(self, registry: ProviderRegistry | None = None) -> None:
        self._registry = registry

    def compile(
        self,
        doc: Document,
        summaries: list[Summary],
        entities: list[Entity],
        relationships: list[Relationship],
        *,
        model: str = "",
    ) -> CompileOutput:
        """Generate a study guide."""
        # Build context
        summary_text = summaries[0].content if summaries else f"Document: {doc.title}"
        entities_text = "\n".join(
            f"- {e.name} ({e.entity_type}): {e.description}" for e in entities[:40]
        )

        entity_map = {e.id: e.name for e in entities}
        rels_text = "\n".join(
            f"- {entity_map.get(r.source_entity_id, '?')} "
            f"{r.relationship_type.replace('_', ' ')} "
            f"{entity_map.get(r.target_entity_id, '?')}"
            for r in relationships[:20]
        ) or "No relationships extracted yet."

        # Try AI generation
        if self._registry and self._registry.has_providers():
            try:
                return self._generate_ai_guide(
                    doc,
                    summary_text,
                    entities_text,
                    rels_text,
                    len(entities),
                    model=model,
                )
            except Exception as exc:
                logger.warning(
                    "AI study guide generation failed, using template: %s", exc
                )

        # Fallback: template-based
        return self._generate_template_guide(doc, summaries, entities, relationships)

    def _generate_ai_guide(
        self,
        doc: Document,
        summary: str,
        entities_text: str,
        rels_text: str,
        entity_count: int,
        *,
        model: str,
    ) -> CompileOutput:
        prompt = STUDY_GUIDE_TEMPLATE.format(
            title=doc.title,
            summary=summary[:3000],
            entities_text=entities_text,
            relationships_text=rels_text,
            entity_count=entity_count,
        )
        messages = [
            {"role": "system", "content": STUDY_GUIDE_SYSTEM},
            {"role": "user", "content": prompt},
        ]
        resp = self._registry.chat(messages, model=model)

        content = f"# Study Guide: {doc.title}\n\n{resp.text}"

        return CompileOutput(
            format=OutputFormat.STUDY_GUIDE,
            title=f"{doc.title} — Study Guide",
            content=content,
            source_doc_id=doc.id,
            source_doc_title=doc.title,
            generated_by_provider=resp.provider,
            generated_by_model=resp.model,
        )

    def _generate_template_guide(
        self,
        doc: Document,
        summaries: list[Summary],
        entities: list[Entity],
        relationships: list[Relationship],
    ) -> CompileOutput:
        lines = [f"# Study Guide: {doc.title}\n"]

        lines.append("## Overview\n")
        if summaries:
            lines.append(f"{summaries[0].content}\n")
        else:
            lines.append(f"Study guide for {doc.title}.\n")

        if entities:
            lines.append("## Core Concepts\n")
            for e in entities[:30]:
                lines.append(f"### {e.name}\n")
                if e.description:
                    lines.append(f"{e.description}\n")
                lines.append(f"*Type: {e.entity_type}*\n")

        if relationships:
            entity_map = {e.id: e.name for e in entities}
            lines.append("## How They Connect\n")
            for r in relationships[:20]:
                src = entity_map.get(r.source_entity_id, "?")
                tgt = entity_map.get(r.target_entity_id, "?")
                lines.append(
                    f"- **{src}** {r.relationship_type.replace('_', ' ')} **{tgt}**"
                )
                if r.description:
                    lines.append(f"  - {r.description}")
            lines.append("")

        lines.append("## Review Questions\n")
        for i, e in enumerate(entities[:5], 1):
            lines.append(f"{i}. Explain {e.name} and its significance.\n")

        return CompileOutput(
            format=OutputFormat.STUDY_GUIDE,
            title=f"{doc.title} — Study Guide",
            content="\n".join(lines),
            source_doc_id=doc.id,
            source_doc_title=doc.title,
        )
