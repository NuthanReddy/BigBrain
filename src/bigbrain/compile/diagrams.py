"""Diagram generation — creates Mermaid charts from distilled content."""

from __future__ import annotations

from bigbrain.distill.models import Entity, Relationship
from bigbrain.logging_config import get_logger
from bigbrain.providers.registry import ProviderRegistry

logger = get_logger(__name__)


def generate_entity_relationship_diagram(
    entities: list[Entity],
    relationships: list[Relationship],
    *,
    max_nodes: int = 30,
) -> str:
    """Generate a Mermaid ER/graph diagram from entities and relationships."""
    lines = ["graph TD"]

    # Add entity nodes (with sanitized IDs)
    seen_ids: set[str] = set()
    for e in entities[:max_nodes]:
        safe_id = _safe_mermaid_id(e.id)
        label = e.name.replace('"', "'")
        lines.append(f'    {safe_id}["{label}"]')
        seen_ids.add(e.id)

    # Add relationship edges
    for r in relationships:
        if r.source_entity_id not in seen_ids or r.target_entity_id not in seen_ids:
            continue
        src = _safe_mermaid_id(r.source_entity_id)
        tgt = _safe_mermaid_id(r.target_entity_id)
        label = r.relationship_type.replace("_", " ")
        lines.append(f'    {src} -->|{label}| {tgt}')

    return "\n".join(lines)


def generate_class_diagram(entities: list[Entity], max_items: int = 25) -> str:
    """Generate a Mermaid class diagram grouping entities by type."""
    by_type: dict[str, list[Entity]] = {}
    for e in entities[: max_items * 3]:
        by_type.setdefault(e.entity_type, []).append(e)

    lines = ["classDiagram"]

    for etype, ents in sorted(by_type.items()):
        class_name = etype.replace("_", " ").title().replace(" ", "")
        lines.append(f"    class {class_name} {{")
        for e in ents[:max_items]:
            lines.append(f"        +{e.name}")
        lines.append("    }")

    return "\n".join(lines)


def generate_flowchart(
    entities: list[Entity],
    relationships: list[Relationship],
    *,
    max_nodes: int = 20,
) -> str:
    """Generate a Mermaid flowchart focusing on process/technique entities."""
    # Prioritize algorithms, techniques, concepts
    priority_types = {"algorithm", "technique", "concept", "data_structure"}
    priority = [e for e in entities if e.entity_type in priority_types][:max_nodes]
    other = [e for e in entities if e.entity_type not in priority_types][
        : max(0, max_nodes - len(priority))
    ]
    selected = priority + other
    selected_ids = {e.id for e in selected}

    lines = ["flowchart LR"]

    # Shape by type
    for e in selected:
        safe_id = _safe_mermaid_id(e.id)
        label = e.name.replace('"', "'")
        if e.entity_type == "algorithm":
            lines.append(f'    {safe_id}(["{label}"])')
        elif e.entity_type == "data_structure":
            lines.append(f'    {safe_id}[["{label}"]]')
        elif e.entity_type == "theorem":
            lines.append(f'    {safe_id}{{"{label}"}}')
        else:
            lines.append(f'    {safe_id}["{label}"]')

    for r in relationships:
        if r.source_entity_id in selected_ids and r.target_entity_id in selected_ids:
            src = _safe_mermaid_id(r.source_entity_id)
            tgt = _safe_mermaid_id(r.target_entity_id)
            label = r.relationship_type.replace("_", " ")
            lines.append(f'    {src} -->|{label}| {tgt}')

    return "\n".join(lines)


def generate_mindmap(entities: list[Entity], root_title: str = "Knowledge") -> str:
    """Generate a Mermaid mindmap from entities grouped by type."""
    by_type: dict[str, list[Entity]] = {}
    for e in entities:
        by_type.setdefault(e.entity_type, []).append(e)

    lines = ["mindmap"]
    lines.append(f"  root(({root_title}))")

    for etype, ents in sorted(by_type.items()):
        type_label = etype.replace("_", " ").title()
        lines.append(f"    {type_label}")
        for e in ents[:10]:
            lines.append(f"      {e.name}")

    return "\n".join(lines)


def generate_ai_diagram(
    entities: list[Entity],
    relationships: list[Relationship],
    registry: ProviderRegistry,
    *,
    diagram_type: str = "flowchart",
    model: str = "",
) -> str:
    """Use AI to generate a Mermaid diagram from entities."""
    e_map = {e.id: e.name for e in entities}
    entities_text = "\n".join(f"- {e.name} ({e.entity_type})" for e in entities[:30])
    rels_text = (
        "\n".join(
            f"- {e_map.get(r.source_entity_id, '?')} {r.relationship_type} {e_map.get(r.target_entity_id, '?')}"
            for r in relationships[:20]
        )
        or "None"
    )

    prompt = (
        f"Generate a Mermaid {diagram_type} diagram from these entities and relationships.\n\n"
        f"Entities:\n{entities_text}\n\n"
        f"Relationships:\n{rels_text}\n\n"
        f"Return ONLY the Mermaid code, starting with '{diagram_type}' or 'graph'. No markdown fences."
    )

    try:
        resp = registry.complete(prompt, model=model)
        code = resp.text.strip()
        # Strip markdown fences if present
        if code.startswith("```"):
            code_lines = code.split("\n")
            code_lines = [ln for ln in code_lines if not ln.strip().startswith("```")]
            code = "\n".join(code_lines).strip()
        return code
    except Exception as exc:
        logger.warning("AI diagram generation failed: %s", exc)
        return generate_flowchart(entities, relationships)


def _safe_mermaid_id(raw_id: str) -> str:
    """Create a safe Mermaid node ID from a UUID."""
    return "n" + raw_id.replace("-", "")[:12]
