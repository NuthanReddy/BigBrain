"""Q&A generator — creates question-answer pairs for study/review."""

from __future__ import annotations

import json

from bigbrain.compile.models import CompileOutput, OutputFormat, QAPair
from bigbrain.distill.models import Entity, Summary
from bigbrain.kb.models import Document
from bigbrain.logging_config import get_logger
from bigbrain.providers.registry import ProviderRegistry

logger = get_logger(__name__)

QA_SYSTEM = "You are an expert educator. Create study questions that test understanding. Return ONLY valid JSON."

QA_TEMPLATE = """Generate {count} study questions with answers from the following content.

Summary: {summary}

Key Concepts:
{concepts}

Return a JSON array where each item has:
- "question": clear, specific question
- "answer": complete but concise answer
- "difficulty": "easy", "medium", or "hard"
- "topic": the main topic being tested

JSON array only:"""


class QAGenerator:
    """Generates Q&A pairs using AI or templates."""

    def __init__(self, registry: ProviderRegistry | None = None) -> None:
        self._registry = registry

    def compile(
        self,
        doc: Document,
        summaries: list[Summary],
        entities: list[Entity],
        *,
        max_pairs: int = 15,
        model: str = "",
    ) -> CompileOutput:
        """Generate Q&A pairs."""
        pairs: list[QAPair] = []
        provider = ""
        model_used = ""

        if self._registry and self._registry.has_providers():
            try:
                pairs, provider, model_used = self._generate_ai_qa(
                    summaries, entities, max_pairs=max_pairs, model=model
                )
            except Exception as exc:
                logger.warning("AI Q&A generation failed, using template: %s", exc)

        if not pairs:
            pairs = self._generate_template_qa(entities, max_pairs=max_pairs)

        # Render as markdown
        lines = [f"# Study Questions: {doc.title}\n"]
        for i, qa in enumerate(pairs, 1):
            diff_badge = f" [{qa.difficulty}]" if qa.difficulty else ""
            lines.append(f"## Q{i}{diff_badge}\n")
            lines.append(f"**{qa.question}**\n")
            lines.append(f"> {qa.answer}\n")
            if qa.topic:
                lines.append(f"*Topic: {qa.topic}*\n")

        return CompileOutput(
            format=OutputFormat.QA,
            title=f"{doc.title} — Study Questions",
            content="\n".join(lines),
            source_doc_id=doc.id,
            source_doc_title=doc.title,
            qa_pairs=pairs,
            generated_by_provider=provider,
            generated_by_model=model_used,
        )

    def _generate_ai_qa(
        self,
        summaries: list[Summary],
        entities: list[Entity],
        *,
        max_pairs: int,
        model: str,
    ) -> tuple[list[QAPair], str, str]:
        """Generate Q&A pairs via the AI provider."""
        assert self._registry is not None

        summary_text = summaries[0].content if summaries else ""
        concepts = "\n".join(f"- {e.name}: {e.description}" for e in entities[:25])

        prompt = QA_TEMPLATE.format(
            count=max_pairs, summary=summary_text[:2000], concepts=concepts
        )
        messages = [
            {"role": "system", "content": QA_SYSTEM},
            {"role": "user", "content": prompt},
        ]
        resp = self._registry.chat(messages, model=model)

        pairs: list[QAPair] = []
        text = resp.text.strip()

        # Strip markdown fences if present
        if text.startswith("```"):
            text_lines = text.split("\n")
            text_lines = [l for l in text_lines if not l.strip().startswith("```")]
            text = "\n".join(text_lines).strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            start, end = text.find("["), text.rfind("]")
            if start != -1 and end > start:
                data = json.loads(text[start : end + 1])
            else:
                data = []

        for item in data[:max_pairs]:
            if isinstance(item, dict) and "question" in item:
                pairs.append(
                    QAPair(
                        question=item["question"],
                        answer=item.get("answer", ""),
                        difficulty=item.get("difficulty", "medium"),
                        topic=item.get("topic", ""),
                    )
                )

        return pairs, resp.provider, resp.model

    def _generate_template_qa(
        self, entities: list[Entity], *, max_pairs: int
    ) -> list[QAPair]:
        """Fallback: generate Q&A pairs from entity descriptions."""
        pairs: list[QAPair] = []
        for e in entities[:max_pairs]:
            if not e.description:
                continue
            pairs.append(
                QAPair(
                    question=f"Explain {e.name}.",
                    answer=e.description,
                    difficulty="medium",
                    topic=e.entity_type,
                )
            )
        return pairs
