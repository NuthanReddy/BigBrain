"""Flashcard compiler — generates Q&A flashcards from distilled content."""

from __future__ import annotations

import json

from bigbrain.compile.models import CompileOutput, Flashcard, OutputFormat
from bigbrain.distill.models import Entity, Summary
from bigbrain.kb.models import Document
from bigbrain.logging_config import get_logger
from bigbrain.providers.registry import ProviderRegistry

logger = get_logger(__name__)

FLASHCARD_SYSTEM = "You are a study aid creator. Generate concise flashcards. Return ONLY valid JSON."

FLASHCARD_TEMPLATE = """Create {count} flashcards from the following entities and summary. Each flashcard should test understanding of a key concept.

Summary: {summary}

Entities:
{entities_text}

Return a JSON array where each item has:
- "front": the question (concise, specific)
- "back": the answer (clear, complete but brief)
- "tags": array of topic tags

JSON array only:"""


class FlashcardCompiler:
    """Compiles distilled content into flashcards."""

    def __init__(self, registry: ProviderRegistry | None = None) -> None:
        self._registry = registry

    def compile(
        self,
        doc: Document,
        summaries: list[Summary],
        entities: list[Entity],
        *,
        max_cards: int = 20,
        model: str = "",
    ) -> CompileOutput:
        """Generate flashcards from distilled content."""
        cards: list[Flashcard] = []
        provider = ""
        model_used = ""

        # Try AI generation first
        if self._registry and self._registry.has_providers():
            try:
                cards, provider, model_used = self._generate_ai_cards(
                    summaries, entities, max_cards=max_cards, model=model
                )
            except Exception as exc:
                logger.warning("AI flashcard generation failed, using template: %s", exc)

        # Fallback: template-based cards from entities
        if not cards:
            cards = self._generate_template_cards(entities, max_cards=max_cards)

        # Render as markdown
        lines = [f"# Flashcards: {doc.title}\n"]
        for i, card in enumerate(cards, 1):
            lines.append(f"## Card {i}\n")
            lines.append(f"**Q:** {card.front}\n")
            lines.append(f"**A:** {card.back}\n")
            if card.tags:
                lines.append(f"*Tags: {', '.join(card.tags)}*\n")

        return CompileOutput(
            format=OutputFormat.FLASHCARD,
            title=f"{doc.title} — Flashcards",
            content="\n".join(lines),
            source_doc_id=doc.id,
            source_doc_title=doc.title,
            flashcards=cards,
            generated_by_provider=provider,
            generated_by_model=model_used,
        )

    def _generate_ai_cards(
        self,
        summaries: list[Summary],
        entities: list[Entity],
        *,
        max_cards: int,
        model: str,
    ) -> tuple[list[Flashcard], str, str]:
        summary_text = summaries[0].content if summaries else "No summary available"
        entities_text = "\n".join(
            f"- {e.name} ({e.entity_type}): {e.description}" for e in entities[:30]
        )

        prompt = FLASHCARD_TEMPLATE.format(
            count=min(max_cards, len(entities) + 5),
            summary=summary_text[:2000],
            entities_text=entities_text,
        )
        messages = [
            {"role": "system", "content": FLASHCARD_SYSTEM},
            {"role": "user", "content": prompt},
        ]
        resp = self._registry.chat(messages, model=model)  # type: ignore[union-attr]

        cards: list[Flashcard] = []
        try:
            data = json.loads(resp.text.strip().strip("```json").strip("```").strip())
            if not isinstance(data, list):
                data = []
        except json.JSONDecodeError:
            # Try extracting a JSON array from the response
            start, end = resp.text.find("["), resp.text.rfind("]")
            if start != -1 and end > start:
                try:
                    data = json.loads(resp.text[start : end + 1])
                except json.JSONDecodeError:
                    data = []
            else:
                data = []

        for item in data[:max_cards]:
            if isinstance(item, dict) and "front" in item and "back" in item:
                cards.append(
                    Flashcard(
                        front=item["front"],
                        back=item["back"],
                        tags=item.get("tags", []),
                    )
                )

        return cards, resp.provider, resp.model

    def _generate_template_cards(
        self, entities: list[Entity], *, max_cards: int
    ) -> list[Flashcard]:
        cards: list[Flashcard] = []
        for e in entities[:max_cards]:
            if not e.description:
                continue
            cards.append(
                Flashcard(
                    front=f"What is {e.name}?",
                    back=e.description,
                    tags=[e.entity_type],
                    source_entity_id=e.id,
                )
            )
        return cards
