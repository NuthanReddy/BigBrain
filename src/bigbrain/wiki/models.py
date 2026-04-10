"""Data models for wiki pages."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class PageType(str, Enum):
    """Types of wiki pages."""
    ENTITY = "entity"
    SOURCE = "source"
    TOPIC = "topic"
    OVERVIEW = "overview"


@dataclass
class WikiPage:
    """A single wiki page with metadata and content."""
    slug: str = ""
    title: str = ""
    page_type: PageType = PageType.ENTITY
    content: str = ""  # Markdown body (without frontmatter)

    # Frontmatter fields
    entity_type: str = ""
    tags: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)
    source_count: int = 0
    source_doc_ids: list[str] = field(default_factory=list)
    related_pages: list[str] = field(default_factory=list)  # slugs of linked pages

    # Metadata
    managed_by: str = "bigbrain"  # "bigbrain" or "user"
    last_updated: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    content_hash: str = ""  # for skip-if-unchanged writes
    metadata: dict[str, Any] = field(default_factory=dict)
