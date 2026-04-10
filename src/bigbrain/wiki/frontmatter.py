"""YAML frontmatter generation and parsing for wiki pages."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bigbrain.wiki.models import WikiPage


def build_frontmatter(page: WikiPage) -> str:
    """Generate YAML frontmatter string for a WikiPage.

    Output is deterministic: keys are sorted, lists are sorted.
    """
    lines = ["---"]

    lines.append(f"title: {_yaml_str(page.title)}")
    lines.append(f"slug: {page.slug}")
    lines.append(f"type: {page.page_type.value}")
    lines.append(f"managed_by: {page.managed_by}")

    if page.entity_type:
        lines.append(f"entity_type: {page.entity_type}")

    if page.aliases:
        lines.append(f"aliases: [{', '.join(sorted(page.aliases))}]")

    if page.tags:
        lines.append(f"tags: [{', '.join(sorted(page.tags))}]")

    if page.source_count:
        lines.append(f"source_count: {page.source_count}")

    if page.source_doc_ids:
        lines.append(f"sources: [{', '.join(sorted(page.source_doc_ids))}]")

    if page.related_pages:
        lines.append(f"related: [{', '.join(sorted(page.related_pages))}]")

    lines.append(f"last_updated: {page.last_updated.strftime('%Y-%m-%dT%H:%M:%SZ')}")

    lines.append("---")
    return "\n".join(lines)


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from markdown text.

    Returns (frontmatter_dict, body_without_frontmatter).
    If no frontmatter found, returns ({}, original_text).
    """
    if not text.startswith("---"):
        return {}, text

    lines = text.split("\n")
    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx == -1:
        return {}, text

    # Parse frontmatter lines as simple key: value
    fm: dict[str, Any] = {}
    for line in lines[1:end_idx]:
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()

        # Parse lists: [item1, item2]
        if value.startswith("[") and value.endswith("]"):
            items = [v.strip() for v in value[1:-1].split(",") if v.strip()]
            fm[key] = items
        # Parse numbers
        elif value.isdigit():
            fm[key] = int(value)
        else:
            fm[key] = value

    body = "\n".join(lines[end_idx + 1:]).lstrip("\n")
    return fm, body


def render_page(page: WikiPage) -> str:
    """Render a complete wiki page: frontmatter + content."""
    fm = build_frontmatter(page)
    return f"{fm}\n\n{page.content}\n"


def _yaml_str(s: str) -> str:
    """Quote a string for YAML if it contains special chars."""
    if any(c in s for c in ":#{}[]|>&*!%@"):
        return f'"{s}"'
    return s
