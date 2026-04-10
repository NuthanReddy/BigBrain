"""Tests for bigbrain.wiki — Phase 12A Wiki Build MVP."""

from __future__ import annotations

from pathlib import Path

import pytest

from bigbrain.kb.models import Document, SourceMetadata
from bigbrain.kb.store import KBStore
from bigbrain.distill.models import Entity, Relationship, Summary
from bigbrain.wiki.models import WikiPage, PageType
from bigbrain.wiki.slugger import (
    make_slug,
    make_entity_slug,
    make_source_slug,
    slug_to_wikilink,
    title_to_wikilink,
)
from bigbrain.wiki.frontmatter import build_frontmatter, parse_frontmatter, render_page
from bigbrain.wiki.generators import (
    ConceptPageGenerator,
    SourcePageGenerator,
    OverviewPageGenerator,
)
from bigbrain.wiki.linker import WikiLinker, LinkGraph
from bigbrain.wiki.writer import WikiWriter
from bigbrain.wiki.builder import WikiBuilder, WikiBuildResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _setup_wiki_kb(tmp_path: Path) -> tuple[KBStore, str]:
    """Create a KB with test data for wiki builder tests."""
    store = KBStore(tmp_path / "test.db")
    doc = Document(
        title="Test Doc",
        content="Test content about Binary Search and Array data structures",
        source=SourceMetadata(
            file_path="test.txt",
            file_extension=".txt",
            source_type="txt",
            size_bytes=100,
        ),
    )
    doc_id = store.save_document(doc)

    entities = [
        Entity(
            id="e1",
            document_id=doc_id,
            name="Binary Search",
            entity_type="algorithm",
            description="Efficient search on sorted array",
        ),
        Entity(
            id="e2",
            document_id=doc_id,
            name="Array",
            entity_type="data_structure",
            description="Contiguous memory block",
        ),
    ]
    store.save_entities(entities)
    store.save_summaries(
        [Summary(document_id=doc_id, content="Test summary about algorithms.")]
    )
    store.save_relationships(
        [
            Relationship(
                id="r1",
                source_entity_id="e1",
                target_entity_id="e2",
                relationship_type="uses",
                document_id=doc_id,
            )
        ]
    )

    return store, doc_id


def _make_entity(
    name: str = "Binary Search",
    entity_type: str = "algorithm",
    description: str = "A search algorithm",
    doc_id: str = "doc-1",
    eid: str = "e1",
) -> Entity:
    return Entity(
        id=eid,
        document_id=doc_id,
        name=name,
        entity_type=entity_type,
        description=description,
    )


def _make_doc(
    title: str = "Test Doc",
    content: str = "Test content",
    file_path: str = "test.txt",
) -> Document:
    return Document(
        title=title,
        content=content,
        source=SourceMetadata(
            file_path=file_path,
            file_extension=".txt",
            source_type="txt",
            size_bytes=len(content),
        ),
    )


# ---------------------------------------------------------------------------
# TestSlugger
# ---------------------------------------------------------------------------


class TestSlugger:
    def test_make_slug_basic(self):
        assert make_slug("Binary Search Tree") == "binary-search-tree"

    def test_make_slug_special_chars(self):
        slug = make_slug("Hello, World! #2024")
        assert "," not in slug
        assert "!" not in slug
        assert "#" not in slug

    def test_make_slug_deterministic(self):
        assert make_slug("Same Input") == make_slug("Same Input")

    def test_make_slug_truncates(self):
        long_title = "a " * 100  # 200 chars
        slug = make_slug(long_title)
        assert len(slug) <= 80

    def test_make_slug_empty(self):
        slug = make_slug("")
        assert slug.startswith("page-")
        assert len(slug) > 5  # has hash suffix

    def test_make_slug_underscores(self):
        assert make_slug("hello_world_test") == "hello-world-test"

    def test_make_slug_collapses_hyphens(self):
        assert make_slug("a---b") == "a-b"

    def test_make_entity_slug(self):
        slug = make_entity_slug("Binary Search", "algorithm")
        assert slug == "binary-search"

    def test_make_source_slug(self):
        slug = make_source_slug("My Notes")
        assert slug == "source-my-notes"
        assert slug.startswith("source-")

    def test_title_to_wikilink(self):
        link = title_to_wikilink("Red-Black Tree")
        assert link == "[[red-black-tree|Red-Black Tree]]"

    def test_slug_to_wikilink_simple(self):
        link = slug_to_wikilink("binary-search")
        assert link == "[[binary-search]]"

    def test_slug_to_wikilink_with_display(self):
        # Display text that differs from slug gets included
        link = slug_to_wikilink("binary-search", "Binary Search Algorithm")
        assert link == "[[binary-search|Binary Search Algorithm]]"

    def test_slug_to_wikilink_display_matches_slug(self):
        # When display matches slug, no display text needed
        link = slug_to_wikilink("binary-search", "binary search")
        assert link == "[[binary-search]]"


# ---------------------------------------------------------------------------
# TestFrontmatter
# ---------------------------------------------------------------------------


class TestFrontmatter:
    def test_build_frontmatter(self):
        page = WikiPage(
            slug="binary-search",
            title="Binary Search",
            page_type=PageType.ENTITY,
            managed_by="bigbrain",
        )
        fm = build_frontmatter(page)
        assert "title: Binary Search" in fm
        assert "slug: binary-search" in fm
        assert "type: entity" in fm
        assert "managed_by: bigbrain" in fm
        assert fm.startswith("---")
        assert fm.endswith("---")

    def test_build_frontmatter_sorted(self):
        page = WikiPage(
            slug="test",
            title="Test",
            tags=["zebra", "alpha", "middle"],
            aliases=["z-alias", "a-alias"],
        )
        fm = build_frontmatter(page)
        # Tags should be sorted
        assert "tags: [alpha, middle, zebra]" in fm
        # Aliases should be sorted
        assert "aliases: [a-alias, z-alias]" in fm

    def test_parse_frontmatter_roundtrip(self):
        page = WikiPage(
            slug="test-page",
            title="Test Page",
            page_type=PageType.ENTITY,
            entity_type="algorithm",
            tags=["algo", "search"],
            source_count=3,
        )
        fm_str = build_frontmatter(page)
        full_text = f"{fm_str}\n\nSome body content."
        parsed, body = parse_frontmatter(full_text)
        assert parsed["title"] == "Test Page"
        assert parsed["slug"] == "test-page"
        assert parsed["type"] == "entity"
        assert parsed["entity_type"] == "algorithm"
        assert parsed["source_count"] == 3
        assert "algo" in parsed["tags"]
        assert "search" in parsed["tags"]
        assert body.strip() == "Some body content."

    def test_parse_frontmatter_no_fm(self):
        text = "Just plain markdown\nNo frontmatter here."
        parsed, body = parse_frontmatter(text)
        assert parsed == {}
        assert body == text

    def test_render_page(self):
        page = WikiPage(
            slug="test",
            title="Test",
            page_type=PageType.ENTITY,
            content="# Hello\n\nWorld",
        )
        rendered = render_page(page)
        assert rendered.startswith("---")
        assert "# Hello" in rendered
        assert "World" in rendered
        # frontmatter + blank line + content + trailing newline
        assert "\n\n# Hello" in rendered


# ---------------------------------------------------------------------------
# TestConceptPageGenerator
# ---------------------------------------------------------------------------


class TestConceptPageGenerator:
    def test_generate_basic(self):
        entity = _make_entity(description="Efficient search on sorted array", entity_type="concept")
        gen = ConceptPageGenerator()
        page = gen.generate("Binary Search", [entity])
        assert "binary-search" in page.slug
        assert page.title == "Binary Search"
        assert "Efficient search on sorted array" in page.content

    def test_generate_groups_by_type(self):
        e1 = _make_entity(eid="e1", name="Sorting", entity_type="concept", description="Ordering elements")
        e2 = _make_entity(eid="e2", name="Merge Sort", entity_type="algorithm", description="Divide and conquer sort")
        e3 = _make_entity(eid="e3", name="Array", entity_type="data_structure", description="Contiguous memory")
        gen = ConceptPageGenerator()
        page = gen.generate("Sorting", [e1, e2, e3])
        assert "## Algorithms" in page.content
        assert "### Merge Sort" in page.content
        assert "## Data Structures" in page.content
        assert "### Array" in page.content

    def test_page_type_is_topic(self):
        entity = _make_entity(entity_type="concept")
        gen = ConceptPageGenerator()
        page = gen.generate("Binary Search", [entity])
        assert page.page_type == PageType.TOPIC

    def test_tags_include_all_member_types(self):
        e1 = _make_entity(eid="e1", entity_type="concept")
        e2 = _make_entity(eid="e2", entity_type="algorithm")
        gen = ConceptPageGenerator()
        page = gen.generate("Test", [e1, e2])
        assert "concept" in page.tags
        assert "algorithm" in page.tags


# ---------------------------------------------------------------------------
# TestSourcePageGenerator
# ---------------------------------------------------------------------------


class TestSourcePageGenerator:
    def test_generate_basic(self):
        doc = _make_doc(title="My Notes", file_path="notes.txt")
        gen = SourcePageGenerator()
        page = gen.generate(doc)
        assert page.slug == "source-my-notes"
        assert page.page_type == PageType.SOURCE
        assert "`notes.txt`" in page.content
        assert "txt" in page.content

    def test_generate_with_summaries(self):
        doc = _make_doc()
        summaries = [Summary(document_id="d1", content="This is a great summary.")]
        gen = SourcePageGenerator()
        page = gen.generate(doc, summaries=summaries)
        assert "## Summary" in page.content
        assert "This is a great summary." in page.content

    def test_generate_with_entities(self):
        doc = _make_doc()
        entities = [
            _make_entity(eid="e1", name="Binary Search", entity_type="algorithm"),
        ]
        gen = SourcePageGenerator()
        page = gen.generate(doc, entities=entities)
        assert "## Key Concepts" in page.content
        assert "[[binary-search|Binary Search]]" in page.content


# ---------------------------------------------------------------------------
# TestOverviewPageGenerator
# ---------------------------------------------------------------------------


class TestOverviewPageGenerator:
    def test_generate(self):
        docs = [_make_doc(title="Doc A", file_path="a.txt")]
        entities = [
            _make_entity(eid="e1", name="X", entity_type="algorithm"),
            _make_entity(eid="e2", name="Y", entity_type="algorithm"),
            _make_entity(eid="e3", name="Z", entity_type="data_structure"),
        ]
        gen = OverviewPageGenerator()
        page = gen.generate(docs, entities)
        assert "## Sources" in page.content
        assert "Doc A" in page.content
        assert "## Knowledge Map" in page.content
        assert "Algorithm" in page.content
        assert "Data Structure" in page.content

    def test_slug_is_overview(self):
        gen = OverviewPageGenerator()
        page = gen.generate([], [])
        assert page.slug == "overview"
        assert page.page_type == PageType.OVERVIEW


# ---------------------------------------------------------------------------
# TestLinker
# ---------------------------------------------------------------------------


class TestLinker:
    def test_link_inserts_wikilinks(self):
        entity_page = WikiPage(
            slug="binary-search",
            title="Binary Search",
            page_type=PageType.ENTITY,
            content="Binary Search uses Array for storage.",
        )
        target_page = WikiPage(
            slug="array",
            title="Array",
            page_type=PageType.ENTITY,
            content="A contiguous block of memory.",
        )
        linker = WikiLinker([entity_page, target_page])
        graph = linker.link_pages()
        # "Array" in entity_page content should become a wikilink
        assert "[[array|Array]]" in entity_page.content

    def test_no_self_link(self):
        page = WikiPage(
            slug="binary-search",
            title="Binary Search",
            page_type=PageType.ENTITY,
            content="Binary Search is a well-known algorithm.",
        )
        linker = WikiLinker([page])
        linker.link_pages()
        # Should NOT self-link
        assert "[[binary-search" not in page.content

    def test_no_double_link(self):
        page = WikiPage(
            slug="page-a",
            title="Page A",
            page_type=PageType.ENTITY,
            content="Uses [[array|Array]] and also mentions Array again.",
        )
        target = WikiPage(
            slug="array",
            title="Array",
            page_type=PageType.ENTITY,
            content="A data structure.",
        )
        linker = WikiLinker([page, target])
        linker.link_pages()
        # Should not double-link the second "Array"
        count = page.content.count("[[array|Array]]")
        assert count >= 1
        # Ensure no nested/broken wikilinks
        assert "[[[[" not in page.content

    def test_link_graph_edges(self):
        p1 = WikiPage(
            slug="a", title="A", page_type=PageType.ENTITY,
            content="Mentions B in text.",
        )
        p2 = WikiPage(
            slug="b", title="B", page_type=PageType.ENTITY,
            content="Standalone page.",
        )
        linker = WikiLinker([p1, p2])
        graph = linker.link_pages()
        assert "b" in graph.get_outgoing("a")
        assert graph.total_edges >= 1

    def test_link_graph_orphans(self):
        graph = LinkGraph()
        graph.add_edge("a", "b")
        graph.add_edge("a", "c")
        orphans = graph.get_orphans({"a", "b", "c", "d"})
        # "a" has no incoming links, "d" has no incoming links
        assert "a" in orphans
        assert "d" in orphans
        # "b" and "c" have incoming links from "a"
        assert "b" not in orphans
        assert "c" not in orphans


# ---------------------------------------------------------------------------
# TestWriter
# ---------------------------------------------------------------------------


class TestWriter:
    def test_write_page(self, tmp_path: Path):
        wiki_dir = tmp_path / "wiki"
        writer = WikiWriter(wiki_dir)
        page = WikiPage(
            slug="test-page",
            title="Test Page",
            page_type=PageType.ENTITY,
            content="Hello world",
        )
        written = writer.write_page(page)
        assert written is True
        assert (wiki_dir / "test-page.md").exists()
        content = (wiki_dir / "test-page.md").read_text(encoding="utf-8")
        assert "Hello world" in content
        assert "title: Test Page" in content

    def test_skip_unchanged(self, tmp_path: Path):
        wiki_dir = tmp_path / "wiki"
        writer = WikiWriter(wiki_dir)
        page = WikiPage(
            slug="test-page",
            title="Test Page",
            page_type=PageType.ENTITY,
            content="Same content",
        )
        assert writer.write_page(page) is True
        assert writer.write_page(page) is False  # unchanged

    def test_write_all(self, tmp_path: Path):
        wiki_dir = tmp_path / "wiki"
        writer = WikiWriter(wiki_dir)
        pages = [
            WikiPage(slug="page-a", title="A", content="Content A"),
            WikiPage(slug="page-b", title="B", content="Content B"),
        ]
        written, skipped = writer.write_all(pages)
        assert written == 2
        assert skipped == 0
        assert (wiki_dir / "page-a.md").exists()
        assert (wiki_dir / "page-b.md").exists()

    def test_clean_removes_orphans(self, tmp_path: Path):
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir(parents=True)
        # Pre-create an orphan file
        (wiki_dir / "orphan.md").write_text("old content", encoding="utf-8")

        writer = WikiWriter(wiki_dir)
        pages = [WikiPage(slug="keep-me", title="Keep", content="Keep this")]
        writer.write_all(pages, clean=True)
        assert (wiki_dir / "keep-me.md").exists()
        assert not (wiki_dir / "orphan.md").exists()

    def test_list_existing_pages(self, tmp_path: Path):
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir(parents=True)
        (wiki_dir / "alpha.md").write_text("a", encoding="utf-8")
        (wiki_dir / "beta.md").write_text("b", encoding="utf-8")
        (wiki_dir / "not-md.txt").write_text("c", encoding="utf-8")

        writer = WikiWriter(wiki_dir)
        slugs = writer.list_existing_pages()
        assert slugs == ["alpha", "beta"]

    def test_list_existing_pages_empty_dir(self, tmp_path: Path):
        writer = WikiWriter(tmp_path / "nonexistent")
        assert writer.list_existing_pages() == []


# ---------------------------------------------------------------------------
# TestWikiBuilder
# ---------------------------------------------------------------------------


class TestWikiBuilder:
    def test_build_empty_kb(self, tmp_path: Path):
        store = KBStore(tmp_path / "empty.db")
        wiki_dir = tmp_path / "wiki"
        builder = WikiBuilder(store=store, wiki_dir=wiki_dir)
        result = builder.build()
        assert result.total_pages == 0
        assert result.written == 0
        store.close()

    def test_build_with_data(self, tmp_path: Path):
        store, doc_id = _setup_wiki_kb(tmp_path)
        wiki_dir = tmp_path / "wiki"
        builder = WikiBuilder(store=store, wiki_dir=wiki_dir)
        result = builder.build()

        # Concept grouping: 2 entities without type "concept" → grouped by type
        assert result.entity_pages >= 1  # at least 1 concept page
        assert result.source_pages == 1  # Test Doc
        assert result.total_pages >= 3  # concept(s) + 1 source + 1 overview
        assert result.written >= 3
        assert (wiki_dir / "overview.md").exists()
        # At least some entity-derived pages exist
        md_files = list(wiki_dir.glob("*.md"))
        assert len(md_files) >= 3
        store.close()

    def test_build_dry_run(self, tmp_path: Path):
        store, doc_id = _setup_wiki_kb(tmp_path)
        wiki_dir = tmp_path / "wiki"
        builder = WikiBuilder(store=store, wiki_dir=wiki_dir)
        result = builder.build(dry_run=True)

        assert result.total_pages >= 3
        assert result.written == 0
        # No files should be created
        assert not wiki_dir.exists() or not list(wiki_dir.glob("*.md"))
        store.close()

    def test_build_clean(self, tmp_path: Path):
        store, doc_id = _setup_wiki_kb(tmp_path)
        wiki_dir = tmp_path / "wiki"
        wiki_dir.mkdir(parents=True)
        # Pre-create an orphan
        (wiki_dir / "old-orphan.md").write_text("stale", encoding="utf-8")

        builder = WikiBuilder(store=store, wiki_dir=wiki_dir)
        builder.build(clean=True)
        assert not (wiki_dir / "old-orphan.md").exists()
        store.close()

    def test_build_deterministic(self, tmp_path: Path):
        store, doc_id = _setup_wiki_kb(tmp_path)
        wiki_dir = tmp_path / "wiki"
        builder = WikiBuilder(store=store, wiki_dir=wiki_dir)

        result1 = builder.build()
        assert result1.written >= 3

        result2 = builder.build()
        # Second build should write 0 (all unchanged)
        assert result2.written == 0
        assert result2.skipped_unchanged == result1.total_pages
        store.close()

    def test_result_counts(self, tmp_path: Path):
        store, doc_id = _setup_wiki_kb(tmp_path)
        wiki_dir = tmp_path / "wiki"
        builder = WikiBuilder(store=store, wiki_dir=wiki_dir)
        result = builder.build()

        assert result.entity_pages >= 1
        assert result.source_pages == 1
        assert result.total_links >= 1  # at least the relationship link
        assert not result.errors
        store.close()

    def test_context_manager(self, tmp_path: Path):
        store, _ = _setup_wiki_kb(tmp_path)
        wiki_dir = tmp_path / "wiki"
        with WikiBuilder(store=store, wiki_dir=wiki_dir) as builder:
            result = builder.build()
            assert result.total_pages >= 3


# ---------------------------------------------------------------------------
# TestWikiBuildResult
# ---------------------------------------------------------------------------


class TestWikiBuildResult:
    def test_default_values(self):
        result = WikiBuildResult()
        assert result.total_pages == 0
        assert result.written == 0
        assert result.skipped_unchanged == 0
        assert result.entity_pages == 0
        assert result.source_pages == 0
        assert result.total_links == 0
        assert result.orphan_pages == 0
        assert result.errors == []
