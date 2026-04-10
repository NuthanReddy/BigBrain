"""Wikilink cross-reference engine — links entity mentions across wiki pages."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from bigbrain.wiki.models import WikiPage
from bigbrain.wiki.slugger import make_slug
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class LinkGraph:
    """Tracks page-to-page link edges."""
    edges: dict[str, set[str]] = field(default_factory=dict)  # source_slug → {target_slugs}

    def add_edge(self, from_slug: str, to_slug: str) -> None:
        self.edges.setdefault(from_slug, set()).add(to_slug)

    def get_outgoing(self, slug: str) -> set[str]:
        return self.edges.get(slug, set())

    def get_incoming(self, slug: str) -> set[str]:
        """Find all pages that link TO this slug."""
        incoming = set()
        for src, targets in self.edges.items():
            if slug in targets:
                incoming.add(src)
        return incoming

    def get_orphans(self, all_slugs: set[str]) -> set[str]:
        """Find pages with no incoming links (except overview)."""
        linked_to = set()
        for targets in self.edges.values():
            linked_to.update(targets)
        return all_slugs - linked_to - {"overview", "index"}

    @property
    def total_edges(self) -> int:
        return sum(len(targets) for targets in self.edges.values())


_MAX_AUTO_LINKS_PER_PAGE = 20


def _is_inside_wikilink(content: str, pos: int) -> bool:
    """Check if position is inside a [[...]] wikilink."""
    open_pos = content.rfind("[[", 0, pos)
    if open_pos == -1:
        return False
    close_pos = content.find("]]", open_pos)
    if close_pos == -1:
        return False
    return open_pos < pos < close_pos + 2


class WikiLinker:
    """Scans wiki pages and inserts cross-reference wikilinks."""

    def __init__(self, pages: list[WikiPage]) -> None:
        # Build lookup: slug → page, name → slug (for entity name matching)
        self._pages = {p.slug: p for p in pages}
        self._name_to_slug: dict[str, str] = {}
        for p in pages:
            # Map title to slug
            self._name_to_slug[p.title.lower()] = p.slug
            # Map aliases too
            for alias in p.aliases:
                self._name_to_slug[alias.lower()] = p.slug

    def link_pages(self) -> LinkGraph:
        """Scan all pages and insert wikilinks. Returns the link graph."""
        graph = LinkGraph()

        for page in self._pages.values():
            self._link_page(page, graph)

        return graph

    def _link_page(self, page: WikiPage, graph: LinkGraph) -> None:
        """Insert wikilinks in a page's content for known entity names."""
        # Extract existing wikilinks first (don't double-link)
        existing_links = set(re.findall(r'\[\[([^\]|]+)', page.content))
        existing_slugs = {make_slug(link) for link in existing_links}

        # Track what this page links to
        for slug in existing_slugs:
            if slug in self._pages and slug != page.slug:
                graph.add_edge(page.slug, slug)

        # Find unlinked entity names in content and add wikilinks
        # Sort by length descending to match longer names first
        candidates = sorted(self._name_to_slug.items(), key=lambda x: -len(x[0]))

        content = page.content
        auto_links = 0
        for name_lower, target_slug in candidates:
            if auto_links >= _MAX_AUTO_LINKS_PER_PAGE:
                break
            if target_slug == page.slug:
                continue  # Don't self-link
            if target_slug in existing_slugs:
                continue  # Already linked

            # Case-insensitive match for the name in content
            # Only match whole words (not inside other words)
            pattern = re.compile(r'\b' + re.escape(name_lower) + r'\b', re.IGNORECASE)
            match = pattern.search(content)
            if match:
                if _is_inside_wikilink(content, match.start()):
                    continue  # Skip — inside an existing wikilink
                original_text = match.group(0)
                wikilink = f"[[{target_slug}|{original_text}]]"
                # Replace only the FIRST occurrence
                content = content[:match.start()] + wikilink + content[match.end():]
                graph.add_edge(page.slug, target_slug)
                existing_slugs.add(target_slug)
                auto_links += 1

        page.content = content
        page.related_pages = sorted(graph.get_outgoing(page.slug))
