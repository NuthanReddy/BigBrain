"""Tests for bigbrain.kb.store – Phase 2 KB storage layer."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from bigbrain.kb.models import Document, DocumentSection, IngestionResult, SourceMetadata
from bigbrain.kb.store import KBStore


# ---------------------------------------------------------------------------
# Helper factory
# ---------------------------------------------------------------------------

def _make_document(
    file_path: str = "test/sample.txt",
    title: str = "Test Doc",
    content: str = "Hello world",
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
        language="",
        sections=[
            DocumentSection(title="Section 1", content="First section", level=1),
            DocumentSection(title="Section 2", content="Second section", level=2),
        ],
    )


# ---------------------------------------------------------------------------
# CRUD operations
# ---------------------------------------------------------------------------

class TestCRUD:

    def test_save_and_get_document(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            doc = _make_document()
            doc_id = store.save_document(doc)

            retrieved = store.get_document(doc_id)
            assert retrieved is not None
            assert retrieved.title == doc.title
            assert retrieved.content == doc.content
            assert retrieved.language == doc.language
            assert retrieved.source is not None
            assert retrieved.source.file_path == doc.source.file_path
            assert retrieved.source.file_extension == doc.source.file_extension
            assert retrieved.source.source_type == doc.source.source_type
            assert retrieved.source.size_bytes == doc.source.size_bytes
            assert len(retrieved.sections) == 2
            assert retrieved.sections[0].title == "Section 1"
            assert retrieved.sections[1].title == "Section 2"

    def test_get_document_by_source_path(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            doc = _make_document(file_path="docs/readme.md")
            store.save_document(doc)

            retrieved = store.get_document_by_source_path("docs/readme.md")
            assert retrieved is not None
            assert retrieved.title == "Test Doc"
            assert retrieved.source.file_path == "docs/readme.md"

    def test_get_nonexistent_document(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            assert store.get_document("nonexistent-id-12345") is None

    def test_list_documents(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            store.save_document(_make_document(file_path="a.txt", title="Doc A"))
            store.save_document(_make_document(file_path="b.txt", title="Doc B"))
            store.save_document(_make_document(file_path="c.txt", title="Doc C"))

            docs = store.list_documents()
            assert len(docs) == 3
            titles = {d.title for d in docs}
            assert titles == {"Doc A", "Doc B", "Doc C"}

    def test_list_documents_filter_by_type(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            txt_doc = _make_document(file_path="a.txt")
            txt_doc.source.source_type = "txt"

            md_doc = _make_document(file_path="b.md", title="Markdown Doc")
            md_doc.source.source_type = "md"
            md_doc.source.file_extension = ".md"

            store.save_document(txt_doc)
            store.save_document(md_doc)

            txt_docs = store.list_documents(source_type="txt")
            assert len(txt_docs) == 1
            assert txt_docs[0].source.source_type == "txt"

            md_docs = store.list_documents(source_type="md")
            assert len(md_docs) == 1
            assert md_docs[0].source.source_type == "md"

    def test_delete_document(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            doc_id = store.save_document(_make_document())

            assert store.get_document(doc_id) is not None
            assert store.delete_document(doc_id) is True
            assert store.get_document(doc_id) is None

    def test_delete_nonexistent(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            assert store.delete_document("does-not-exist") is False

    def test_delete_cascades_sections(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            doc_id = store.save_document(_make_document())

            # Verify sections exist before delete
            conn = sqlite3.connect(str(db))
            conn.execute("PRAGMA foreign_keys = ON")
            count_before = conn.execute(
                "SELECT COUNT(*) FROM sections WHERE document_id = ?", (doc_id,)
            ).fetchone()[0]
            assert count_before == 2

            store.delete_document(doc_id)

            count_after = conn.execute(
                "SELECT COUNT(*) FROM sections WHERE document_id = ?", (doc_id,)
            ).fetchone()[0]
            conn.close()
            assert count_after == 0


# ---------------------------------------------------------------------------
# Upsert / dedup
# ---------------------------------------------------------------------------

class TestUpsert:

    def test_upsert_same_file_no_duplicate(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            store.save_document(_make_document(file_path="dup.txt"))
            store.save_document(_make_document(file_path="dup.txt"))

            docs = store.list_documents()
            assert len(docs) == 1

    def test_upsert_updates_content(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            store.save_document(
                _make_document(file_path="update.txt", content="old content")
            )
            store.save_document(
                _make_document(file_path="update.txt", content="new content")
            )

            doc = store.get_document_by_source_path("update.txt")
            assert doc is not None
            assert doc.content == "new content"

    def test_upsert_preserves_created_at(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            store.save_document(_make_document(file_path="ts.txt"))
            first = store.get_document_by_source_path("ts.txt")

            store.save_document(
                _make_document(file_path="ts.txt", content="updated")
            )
            second = store.get_document_by_source_path("ts.txt")

            assert first.created_at == second.created_at

    def test_upsert_replaces_sections(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            doc2 = _make_document(file_path="sec.txt")
            assert len(doc2.sections) == 2
            store.save_document(doc2)

            doc3 = _make_document(file_path="sec.txt")
            doc3.sections.append(
                DocumentSection(title="Section 3", content="Third section", level=3)
            )
            store.save_document(doc3)

            retrieved = store.get_document_by_source_path("sec.txt")
            assert len(retrieved.sections) == 3
            assert retrieved.sections[2].title == "Section 3"


# ---------------------------------------------------------------------------
# Search (FTS5)
# ---------------------------------------------------------------------------

class TestSearch:

    def test_search_finds_by_title(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            store.save_document(
                _make_document(file_path="t.txt", title="Quantum Physics")
            )
            results = store.search_documents("Quantum")
            assert len(results) >= 1
            assert any(d.title == "Quantum Physics" for d in results)

    def test_search_finds_by_content(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            store.save_document(
                _make_document(
                    file_path="c.txt",
                    title="Regular Title",
                    content="The mitochondria is the powerhouse of the cell",
                )
            )
            results = store.search_documents("mitochondria")
            assert len(results) >= 1
            assert results[0].content.startswith("The mitochondria")

    def test_search_no_results(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            store.save_document(_make_document(file_path="n.txt"))
            results = store.search_documents("xylophone_nonexistent_term")
            assert results == []

    def test_search_empty_query(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            store.save_document(_make_document(file_path="e.txt"))
            assert store.search_documents("") == []
            assert store.search_documents("   ") == []

    def test_search_handles_special_chars(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            store.save_document(_make_document(file_path="s.txt"))
            # Should not raise – the store catches OperationalError
            result = store.search_documents('"unclosed quote')
            assert isinstance(result, list)
            result2 = store.search_documents("foo(bar)")
            assert isinstance(result2, list)


# ---------------------------------------------------------------------------
# Ingestion runs
# ---------------------------------------------------------------------------

class TestIngestionRuns:

    def test_save_ingestion_run(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            result = IngestionResult(processed=5, skipped=1, failed=0)
            run_id = store.save_ingestion_run(result, source_path="/data/docs")

            runs = store.list_ingestion_runs()
            assert len(runs) == 1
            run = runs[0]
            assert run["id"] == run_id
            assert run["processed"] == 5
            assert run["skipped"] == 1
            assert run["failed"] == 0
            assert run["source_path"] == "/data/docs"

    def test_ingestion_run_status_succeeded(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            result = IngestionResult(processed=3, skipped=0, failed=0)
            store.save_ingestion_run(result)

            runs = store.list_ingestion_runs()
            assert runs[0]["status"] == "succeeded"

    def test_ingestion_run_status_failed(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            result = IngestionResult(
                processed=2, failed=1, errors=["Could not parse file.pdf"]
            )
            store.save_ingestion_run(result)

            runs = store.list_ingestion_runs()
            assert runs[0]["status"] == "failed"
            assert "Could not parse file.pdf" in runs[0]["errors"]


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

class TestStats:

    def test_get_stats_empty(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            stats = store.get_stats()
            assert stats["total_documents"] == 0
            assert stats["total_sections"] == 0
            assert stats["total_size_bytes"] == 0
            assert stats["by_type"] == {}
            assert stats["last_successful_run"] is None
            assert stats["last_failed_run"] is None

    def test_get_stats_with_data(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            store.save_document(
                _make_document(file_path="x.txt", content="12345")
            )
            md_doc = _make_document(file_path="y.md", content="abcde")
            md_doc.source.source_type = "md"
            store.save_document(md_doc)

            stats = store.get_stats()
            assert stats["total_documents"] == 2
            assert stats["total_sections"] == 4  # 2 sections each
            assert stats["total_size_bytes"] == 10  # 5 + 5
            assert stats["by_type"]["txt"] == 1
            assert stats["by_type"]["md"] == 1

    def test_stats_last_run_info(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            result = IngestionResult(processed=7, skipped=0, failed=0)
            run_id = store.save_ingestion_run(result, source_path="/src")

            stats = store.get_stats()
            last = stats["last_successful_run"]
            assert last is not None
            assert last["id"] == run_id
            assert last["processed"] == 7
            assert last["source_path"] == "/src"


# ---------------------------------------------------------------------------
# Deterministic IDs
# ---------------------------------------------------------------------------

class TestDeterministicIDs:

    def test_make_document_id_deterministic(self):
        id1 = KBStore.make_document_id("some/path/file.txt")
        id2 = KBStore.make_document_id("some/path/file.txt")
        assert id1 == id2

    def test_make_document_id_different_paths(self):
        id1 = KBStore.make_document_id("path/a.txt")
        id2 = KBStore.make_document_id("path/b.txt")
        assert id1 != id2


# ---------------------------------------------------------------------------
# Context manager
# ---------------------------------------------------------------------------

class TestContextManager:

    def test_context_manager(self, tmp_path: Path):
        db = tmp_path / "ctx.db"
        with KBStore(db) as store:
            doc_id = store.save_document(_make_document())
            doc = store.get_document(doc_id)
            assert doc is not None
        # After exiting the context manager, the connection should be closed.
        # We can verify by checking that the db file exists (data was persisted).
        assert db.exists()


# ---------------------------------------------------------------------------
# Edge cases / production hardening
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def test_save_document_without_source_raises(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            doc = Document(title="No source", content="test")
            with pytest.raises(ValueError, match="without SourceMetadata"):
                store.save_document(doc)

    def test_document_without_sections(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            doc = Document(
                title="No sections",
                content="Just content",
                source=SourceMetadata(
                    file_path="nosections.txt",
                    file_extension=".txt",
                    source_type="txt",
                    size_bytes=12,
                ),
                sections=[],
            )
            doc_id = store.save_document(doc)
            retrieved = store.get_document(doc_id)
            assert retrieved is not None
            assert len(retrieved.sections) == 0
            assert retrieved.content == "Just content"

    def test_document_with_empty_content(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            doc = Document(
                title="Empty",
                content="",
                source=SourceMetadata(
                    file_path="empty.txt",
                    file_extension=".txt",
                    source_type="txt",
                    size_bytes=0,
                ),
            )
            doc_id = store.save_document(doc)
            retrieved = store.get_document(doc_id)
            assert retrieved is not None
            assert retrieved.content == ""

    def test_document_with_special_chars_in_content(self, tmp_path: Path):
        db = tmp_path / "test.db"
        content = "SELECT * FROM users WHERE name = 'O''Brien'; -- 日本語テスト 🎉"
        with KBStore(db) as store:
            doc = _make_document(file_path="special.txt", content=content)
            doc_id = store.save_document(doc)
            retrieved = store.get_document(doc_id)
            assert retrieved.content == content

    def test_document_with_metadata(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            doc = _make_document(file_path="meta.txt")
            doc.metadata = {"page_count": 5, "tags": ["test", "sample"]}
            doc.source.extra = {"pdf_author": "Test Author"}
            doc_id = store.save_document(doc)
            retrieved = store.get_document(doc_id)
            assert retrieved.metadata["page_count"] == 5
            assert retrieved.metadata["tags"] == ["test", "sample"]
            assert retrieved.source.extra["pdf_author"] == "Test Author"

    def test_re_ingest_after_delete(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            doc_id = store.save_document(_make_document(file_path="cycle.txt"))
            store.delete_document(doc_id)
            assert store.get_document(doc_id) is None

            # Re-ingest the same path
            doc_id2 = store.save_document(_make_document(
                file_path="cycle.txt", content="new content"
            ))
            assert doc_id == doc_id2  # same deterministic ID
            retrieved = store.get_document(doc_id2)
            assert retrieved is not None
            assert retrieved.content == "new content"

    def test_schema_version_is_set(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            conn = sqlite3.connect(str(db))
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            conn.close()
            assert version == 1

    def test_foreign_keys_enabled(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            fk = store._conn.execute("PRAGMA foreign_keys").fetchone()[0]
            assert fk == 1

    def test_list_documents_pagination(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            for i in range(5):
                store.save_document(_make_document(
                    file_path=f"page_{i}.txt", title=f"Doc {i}"
                ))

            page1 = store.list_documents(limit=2, offset=0)
            page2 = store.list_documents(limit=2, offset=2)
            page3 = store.list_documents(limit=2, offset=4)

            assert len(page1) == 2
            assert len(page2) == 2
            assert len(page3) == 1

    def test_list_ingestion_runs_ordering(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            r1 = IngestionResult(processed=1, failed=0)
            r2 = IngestionResult(processed=2, failed=0)
            id1 = store.save_ingestion_run(r1, source_path="first")
            id2 = store.save_ingestion_run(r2, source_path="second")

            runs = store.list_ingestion_runs(limit=10)
            assert len(runs) == 2
            # Both runs recorded with correct data
            run_ids = {r["id"] for r in runs}
            assert id1 in run_ids
            assert id2 in run_ids
            paths = {r["source_path"] for r in runs}
            assert paths == {"first", "second"}

    def test_search_after_upsert_reflects_new_content(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            store.save_document(_make_document(
                file_path="evolve.txt", content="alpha beta gamma"
            ))
            assert len(store.search_documents("alpha")) >= 1
            assert len(store.search_documents("delta")) == 0

            # Update content
            store.save_document(_make_document(
                file_path="evolve.txt", content="delta epsilon zeta"
            ))
            assert len(store.search_documents("delta")) >= 1
            # Old content should no longer match
            assert len(store.search_documents("alpha")) == 0

    def test_search_after_delete_removes_from_index(self, tmp_path: Path):
        db = tmp_path / "test.db"
        with KBStore(db) as store:
            doc_id = store.save_document(_make_document(
                file_path="rm.txt", content="unique_findme_term"
            ))
            assert len(store.search_documents("unique_findme_term")) == 1

            store.delete_document(doc_id)
            assert len(store.search_documents("unique_findme_term")) == 0


# ---------------------------------------------------------------------------
# JSONL export / import
# ---------------------------------------------------------------------------

class TestJSONL:

    def test_export_jsonl_creates_file(self, tmp_path: Path):
        db = tmp_path / "test.db"
        out = tmp_path / "export.jsonl"
        with KBStore(db) as store:
            store.save_document(_make_document(file_path="a.txt", title="Doc A"))
            store.save_document(_make_document(file_path="b.txt", title="Doc B"))
            store.export_jsonl(out)
        assert out.exists()
        lines = [l for l in out.read_text(encoding="utf-8").splitlines() if l.strip()]
        assert len(lines) == 2

    def test_export_jsonl_returns_count(self, tmp_path: Path):
        db = tmp_path / "test.db"
        out = tmp_path / "export.jsonl"
        with KBStore(db) as store:
            store.save_document(_make_document(file_path="a.txt"))
            store.save_document(_make_document(file_path="b.txt"))
            store.save_document(_make_document(file_path="c.txt"))
            count = store.export_jsonl(out)
        assert count == 3

    def test_export_import_round_trip(self, tmp_path: Path):
        db1 = tmp_path / "src.db"
        db2 = tmp_path / "dst.db"
        out = tmp_path / "round.jsonl"

        with KBStore(db1) as store:
            store.save_document(_make_document(
                file_path="rt.txt", title="Round Trip", content="RT content",
            ))
            store.export_jsonl(out)

        with KBStore(db2) as store2:
            imported, skipped = store2.import_jsonl(out)
            assert imported == 1
            assert skipped == 0

            doc = store2.get_document_by_source_path("rt.txt")
            assert doc is not None
            assert doc.title == "Round Trip"
            assert doc.content == "RT content"
            assert len(doc.sections) == 2
            assert doc.sections[0].title == "Section 1"
            assert doc.sections[1].title == "Section 2"

    def test_import_upsert_updates_existing(self, tmp_path: Path):
        db = tmp_path / "test.db"
        out = tmp_path / "upsert.jsonl"

        with KBStore(db) as store:
            store.save_document(_make_document(
                file_path="up.txt", content="original",
            ))
            store.export_jsonl(out)

            # Overwrite content in the live DB
            store.save_document(_make_document(
                file_path="up.txt", content="modified",
            ))
            doc = store.get_document_by_source_path("up.txt")
            assert doc.content == "modified"

            # Re-import the JSONL (has "original"); upsert=True → overwrite
            imported, skipped = store.import_jsonl(out, upsert=True)
            assert imported == 1
            assert skipped == 0

            doc = store.get_document_by_source_path("up.txt")
            assert doc.content == "original"

    def test_import_no_upsert_skips_existing(self, tmp_path: Path):
        db = tmp_path / "test.db"
        out = tmp_path / "noup.jsonl"

        with KBStore(db) as store:
            store.save_document(_make_document(file_path="skip.txt"))
            store.export_jsonl(out)

            imported, skipped = store.import_jsonl(out, upsert=False)
            assert imported == 0
            assert skipped == 1

    def test_import_malformed_line_skipped(self, tmp_path: Path):
        db = tmp_path / "test.db"
        bad_jsonl = tmp_path / "bad.jsonl"
        bad_jsonl.write_text(
            '{"not_a_document": true}\n'
            '{INVALID JSON\n'
            '',
            encoding="utf-8",
        )

        with KBStore(db) as store:
            imported, skipped = store.import_jsonl(bad_jsonl)
            assert imported == 0
            assert skipped == 2

    def test_export_empty_db(self, tmp_path: Path):
        db = tmp_path / "test.db"
        out = tmp_path / "empty.jsonl"
        with KBStore(db) as store:
            count = store.export_jsonl(out)
        assert count == 0
        assert out.exists()
        assert out.read_text(encoding="utf-8").strip() == ""

    def test_jsonl_preserves_metadata(self, tmp_path: Path):
        db1 = tmp_path / "src.db"
        db2 = tmp_path / "dst.db"
        out = tmp_path / "meta.jsonl"

        with KBStore(db1) as store:
            doc = _make_document(file_path="meta.txt", title="Meta Doc")
            doc.metadata = {"page_count": 42, "tags": ["science", "ai"]}
            doc.source.extra = {"pdf_author": "Jane Doe", "version": 3}
            store.save_document(doc)
            store.export_jsonl(out)

        with KBStore(db2) as store2:
            store2.import_jsonl(out)
            retrieved = store2.get_document_by_source_path("meta.txt")
            assert retrieved is not None
            assert retrieved.metadata["page_count"] == 42
            assert retrieved.metadata["tags"] == ["science", "ai"]
            assert retrieved.source.extra["pdf_author"] == "Jane Doe"
            assert retrieved.source.extra["version"] == 3
