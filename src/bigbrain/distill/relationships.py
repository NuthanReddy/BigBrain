"""AI-powered relationship extraction between entities."""

from __future__ import annotations

import json

from bigbrain.distill.models import Entity, Relationship
from bigbrain.logging_config import get_logger
from bigbrain.providers.registry import ProviderRegistry

logger = get_logger(__name__)

RELATIONSHIP_SYSTEM = "You are a knowledge graph builder. Identify relationships between concepts. Return ONLY valid JSON."

RELATIONSHIP_TEMPLATE = '''Given these entities extracted from a document, identify relationships between them.

Entities:
{entities_text}

Return a JSON array where each item has:
- "source": name of the source entity (must match one of the entities above)
- "target": name of the target entity (must match one of the entities above)
- "type": one of "is_a", "part_of", "uses", "implements", "related_to", "prerequisite_of", "example_of", "variant_of"
- "description": brief description of the relationship

Only include clear, meaningful relationships. Do not invent entities not in the list.

Relationships (JSON array only):'''


class RelationshipBuilder:
    """Builds relationships between extracted entities using AI."""

    def __init__(self, registry: ProviderRegistry) -> None:
        self._registry = registry

    def build_relationships(
        self,
        entities: list[Entity],
        *,
        document_id: str = "",
        model: str = "",
    ) -> list[Relationship]:
        """Identify relationships between entities."""
        if len(entities) < 2:
            return []

        # Build entity name → id mapping
        entity_map = {e.name.lower().strip(): e for e in entities}

        # Format entities for prompt
        entities_text = "\n".join(
            f"- {e.name} ({e.entity_type}): {e.description}" for e in entities
        )

        messages = [
            {"role": "system", "content": RELATIONSHIP_SYSTEM},
            {
                "role": "user",
                "content": RELATIONSHIP_TEMPLATE.format(entities_text=entities_text),
            },
        ]

        try:
            resp = self._registry.chat(messages, model=model)
            rels_data = self._parse_json_response(resp.text)
        except Exception as exc:
            logger.warning("Relationship extraction failed: %s", exc)
            return []

        relationships = []
        for item in rels_data:
            if not isinstance(item, dict):
                continue
            source_name = item.get("source", "").lower().strip()
            target_name = item.get("target", "").lower().strip()

            source_entity = entity_map.get(source_name)
            target_entity = entity_map.get(target_name)

            if not source_entity or not target_entity:
                continue
            if source_entity.id == target_entity.id:
                continue

            relationships.append(
                Relationship(
                    source_entity_id=source_entity.id,
                    target_entity_id=target_entity.id,
                    relationship_type=item.get("type", "related_to"),
                    description=item.get("description", ""),
                    document_id=document_id or source_entity.document_id,
                    generated_by_provider=resp.provider,
                    generated_by_model=resp.model,
                )
            )

        return relationships

    @staticmethod
    def _parse_json_response(text: str) -> list[dict]:
        """Parse JSON array from LLM response."""
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
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

        logger.warning("Could not parse relationship JSON from response")
        return []
