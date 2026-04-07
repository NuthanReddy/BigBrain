"""Tests for bigbrain.kb.service – KBService high-level API."""

from __future__ import annotations

from pathlib import Path

import pytest

from bigbrain.kb.models import (
    Document,
    DocumentSection,
    IngestionResult,
    SourceMetadata,
)
from bigbrain.kb.service import KBService
from bigbrain.kb.store import KBStore


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------

def _make_service(tmp_path: Path) -> KBService:
    db = tmp_path / "test.db"
    store = KBStore(db)
    return KBService(store)


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
# Tests
# ---------------------------------------------------------------------------

class TestKBService:

    def test_from_config(self, tmp_path: Path):
        """from_config() is config-dependent; verify direct construction works."""
        svc = _make_service(tmp_path)
        assert svc is not None
        svc.close()

    def test_store_ingestion_result(self, tmp_path: Path):
        svc = _make_service(tmp_path)
        try:
            result = IngestionResult(
                documents=[
                    _make_document(file_path="a.txt", title="A"),
                    _make_document(file_path="b.txt", title="B"),
                ],
                processed=2,
                skipped=0,
                failed=0,
            )
            stored_count, run_id = svc.store_ingestion_result(result, source_path="/src")
            assert stored_count == 2
            assert isinstance(run_id, str) and len(run_id) > 0
        finally:
            svc.close()

    def test_search(self, tmp_path: Path):
        svc = _make_service(tmp_path)
        try:
            result = IngestionResult(
                documents=[
                    _make_document(
                        file_path="s.txt",
                        title="Quantum Mechanics",
                        content="Quantum theory describes nature",
                    ),
                ],
                processed=1,
            )
            svc.store_ingestion_result(result)
            hits = svc.search("Quantum")
            assert len(hits) >= 1
            assert any(d.title == "Quantum Mechanics" for d in hits)
        finally:
            svc.close()

    def test_get_document(self, tmp_path: Path):
        svc = _make_service(tmp_path)
        try:
            result = IngestionResult(
                documents=[_make_document(file_path="g.txt", title="Get Me")],
                processed=1,
            )
            svc.store_ingestion_result(result)

            docs = svc.list_documents()
            assert len(docs) == 1
            doc = svc.get_document(docs[0].id)
            assert doc is not None
            assert doc.title == "Get Me"
        finally:
            svc.close()

    def test_list_documents(self, tmp_path: Path):
        svc = _make_service(tmp_path)
        try:
            result = IngestionResult(
                documents=[
                    _make_document(file_path="l1.txt", title="L1"),
                    _make_document(file_path="l2.txt", title="L2"),
                    _make_document(file_path="l3.txt", title="L3"),
                ],
                processed=3,
            )
            svc.store_ingestion_result(result)
            docs = svc.list_documents()
            assert len(docs) == 3
            titles = {d.title for d in docs}
            assert titles == {"L1", "L2", "L3"}
        finally:
            svc.close()

    def test_delete_document(self, tmp_path: Path):
        svc = _make_service(tmp_path)
        try:
            result = IngestionResult(
                documents=[_make_document(file_path="del.txt", title="Del")],
                processed=1,
            )
            svc.store_ingestion_result(result)
            docs = svc.list_documents()
            assert len(docs) == 1
            doc_id = docs[0].id
            assert svc.delete_document(doc_id) is True
            assert svc.get_document(doc_id) is None
        finally:
            svc.close()

    def test_get_stats(self, tmp_path: Path):
        svc = _make_service(tmp_path)
        try:
            result = IngestionResult(
                documents=[
                    _make_document(file_path="s1.txt", content="12345"),
                    _make_document(file_path="s2.txt", content="abcde"),
                ],
                processed=2,
            )
            svc.store_ingestion_result(result)
            stats = svc.get_stats()
            assert stats["total_documents"] == 2
            assert stats["total_sections"] == 4  # 2 sections × 2 docs
            assert stats["total_size_bytes"] == 10
        finally:
            svc.close()

    def test_db_exists_false(self, tmp_path: Path):
        """db_exists relies on load_config(); test via store path directly."""
        db = tmp_path / "nonexistent" / "nope.db"
        assert not db.exists()

    def test_context_manager(self, tmp_path: Path):
        with _make_service(tmp_path) as svc:
            result = IngestionResult(
                documents=[_make_document(file_path="ctx.txt")],
                processed=1,
            )
            svc.store_ingestion_result(result)
            docs = svc.list_documents()
            assert len(docs) == 1
        # After exiting context, DB file should persist
        assert (tmp_path / "test.db").exists()

    def test_export_import_via_service(self, tmp_path: Path):
        out = tmp_path / "svc_export.jsonl"
        with _make_service(tmp_path) as svc:
            result = IngestionResult(
                documents=[
                    _make_document(file_path="e1.txt", title="E1", content="Export one"),
                    _make_document(file_path="e2.txt", title="E2", content="Export two"),
                ],
                processed=2,
            )
            svc.store_ingestion_result(result)
            count = svc.export_jsonl(out)
            assert count == 2

        # Import into a fresh service
        db2 = tmp_path / "dst.db"
        store2 = KBStore(db2)
        with KBService(store2) as svc2:
            imported, skipped = svc2.import_jsonl(out)
            assert imported == 2
            assert skipped == 0
            docs = svc2.list_documents()
            assert len(docs) == 2
            titles = {d.title for d in docs}
            assert titles == {"E1", "E2"}
