"""Wiki file writer — writes WikiPage objects to markdown files."""

from __future__ import annotations

import hashlib
from pathlib import Path

from bigbrain.wiki.frontmatter import render_page
from bigbrain.wiki.models import WikiPage
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


class WikiWriter:
    """Writes wiki pages to a directory as markdown files."""

    def __init__(self, wiki_dir: str | Path) -> None:
        self._dir = Path(wiki_dir)

    def write_page(self, page: WikiPage) -> bool:
        """Write a single page to disk. Returns True if file was written (changed).

        Skips writing if the content hash matches the existing file.
        """
        self._dir.mkdir(parents=True, exist_ok=True)

        rendered = render_page(page)
        new_hash = hashlib.sha256(rendered.encode("utf-8")).hexdigest()[:16]
        page.content_hash = new_hash

        file_path = self._dir / f"{page.slug}.md"

        # Skip if unchanged
        if file_path.exists():
            existing = file_path.read_text(encoding="utf-8")
            existing_hash = hashlib.sha256(existing.encode("utf-8")).hexdigest()[:16]
            if existing_hash == new_hash:
                logger.debug("Unchanged: %s", page.slug)
                return False

        file_path.write_text(rendered, encoding="utf-8")
        logger.debug("Wrote: %s", file_path)
        return True

    def write_all(self, pages: list[WikiPage], *, clean: bool = False) -> tuple[int, int]:
        """Write all pages to disk. Returns (written, skipped).

        If clean=True, removes markdown files not in the pages list.
        """
        self._dir.mkdir(parents=True, exist_ok=True)

        written = 0
        skipped = 0
        page_slugs = set()

        for page in pages:
            page_slugs.add(page.slug)
            if self.write_page(page):
                written += 1
            else:
                skipped += 1

        # Clean orphan files
        removed = 0
        if clean:
            for md_file in self._dir.glob("*.md"):
                slug = md_file.stem
                if slug not in page_slugs:
                    md_file.unlink()
                    removed += 1
                    logger.debug("Removed orphan: %s", md_file)

        if removed:
            logger.info("Removed %d orphan wiki files", removed)

        return written, skipped

    def list_existing_pages(self) -> list[str]:
        """Return slugs of all existing wiki pages."""
        if not self._dir.is_dir():
            return []
        return sorted(f.stem for f in self._dir.glob("*.md"))

    @property
    def wiki_dir(self) -> Path:
        return self._dir
