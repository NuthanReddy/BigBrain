"""Stable slug generation for wiki pages."""

from __future__ import annotations

import re
import hashlib


def make_slug(title: str) -> str:
    """Generate a deterministic, URL-safe slug from a title.

    Rules:
    - Lowercase
    - Replace spaces/underscores with hyphens
    - Strip non-alphanumeric (except hyphens)
    - Collapse multiple hyphens
    - Trim leading/trailing hyphens
    - Max 80 chars

    Same input always produces same output.
    """
    slug = title.lower().strip()
    # Replace common separators
    slug = slug.replace("_", "-").replace(" ", "-")
    # Strip non-alphanumeric except hyphens
    slug = re.sub(r"[^a-z0-9\-]", "", slug)
    # Collapse multiple hyphens
    slug = re.sub(r"-{2,}", "-", slug)
    # Trim
    slug = slug.strip("-")
    # Truncate
    if len(slug) > 80:
        slug = slug[:80].rstrip("-")
    # Ensure non-empty
    if not slug:
        slug = "page-" + hashlib.sha256(title.encode()).hexdigest()[:8]
    return slug


def make_entity_slug(name: str, entity_type: str = "") -> str:
    """Slug for an entity page, optionally prefixed by type."""
    return make_slug(name)


def make_source_slug(title: str) -> str:
    """Slug for a source document summary page."""
    return "source-" + make_slug(title)


def slug_to_wikilink(slug: str, display: str = "") -> str:
    """Convert a slug to a [[wikilink]] format."""
    if display and display.lower().replace(" ", "-") != slug:
        return f"[[{slug}|{display}]]"
    return f"[[{slug}]]"


def title_to_wikilink(title: str) -> str:
    """Convert a title directly to a [[wikilink]]."""
    slug = make_slug(title)
    return f"[[{slug}|{title}]]"
