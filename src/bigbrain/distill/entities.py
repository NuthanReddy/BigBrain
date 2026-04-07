"""AI-powered entity extraction for the distillation pipeline."""

from __future__ import annotations

import json

from bigbrain.distill.models import Chunk, Entity
from bigbrain.logging_config import get_logger
from bigbrain.providers.registry import ProviderRegistry

logger = get_logger(__name__)

EXTRACT_SYSTEM = (
    "You are a precise knowledge extraction assistant. "
    "Extract key entities, concepts, and terms from text. "
    "Return ONLY valid JSON."
)

EXTRACT_TEMPLATE = '''Extract the key entities and concepts from the following text.
Return a JSON array where each item has:
- "name": the entity/concept name
- "type": one of "algorithm", "data_structure", "concept", "theorem", "person", "definition", "technique", "property", "other"
- "description": a brief one-sentence description

Text:
{text}

Entities (JSON array only, no other text):'''


class EntityExtractor:
    """Extracts named entities and key concepts using AI."""

    def __init__(self, registry: ProviderRegistry) -> None:
        self._registry = registry

    def extract_from_chunk(self, chunk: Chunk, *, model: str = "") -> list[Entity]:
        """Extract entities from a single chunk."""
        messages = [
            {"role": "system", "content": EXTRACT_SYSTEM},
            {"role": "user", "content": EXTRACT_TEMPLATE.format(text=chunk.content)},
        ]

        try:
            resp = self._registry.chat(messages, model=model)
            entities_data = _parse_json_response(resp.text)
        except Exception as exc:
            logger.warning("Entity extraction failed for chunk %s: %s", chunk.id, exc)
            return []

        entities: list[Entity] = []
        for item in entities_data:
            if not isinstance(item, dict) or "name" not in item:
                continue
            entities.append(
                Entity(
                    document_id=chunk.document_id,
                    name=item.get("name", ""),
                    entity_type=item.get("type", "other"),
                    description=item.get("description", ""),
                    source_chunk_id=chunk.id,
                    generated_by_provider=resp.provider,
                    generated_by_model=resp.model,
                )
            )

        return entities

    def extract_from_chunks(
        self, chunks: list[Chunk], *, model: str = "", existing_names: set[str] | None = None,
    ) -> list[Entity]:
        """Extract entities from multiple chunks, deduplicating by normalized name.
        
        Args:
            chunks: Chunks to extract from
            model: Override AI model
            existing_names: Set of already-known entity names (lowercase) to skip
        """
        all_entities: list[Entity] = []
        seen: set[str] = set(existing_names or set())

        for chunk in chunks:
            try:
                entities = self.extract_from_chunk(chunk, model=model)
                for e in entities:
                    key = _normalize_name(e.name)
                    if key and key not in seen:
                        seen.add(key)
                        all_entities.append(e)
            except Exception as exc:
                logger.warning(
                    "Entity extraction failed for chunk %s: %s", chunk.id, exc
                )

        return all_entities


def _normalize_name(name: str) -> str:
    """Normalize entity name for deduplication: lowercase, strip, collapse whitespace."""
    return " ".join(name.lower().strip().split())


def _parse_json_response(text: str) -> list[dict]:
    """Parse JSON array from LLM response, handling markdown code blocks."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [line for line in lines if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()

    try:
        result = json.loads(text)
        if isinstance(result, list):
            return result
    except json.JSONDecodeError:
        pass

    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass

    logger.warning("Could not parse entity JSON from response")
    return []
