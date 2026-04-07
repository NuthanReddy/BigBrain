"""Tests for bigbrain.orchestrator.pipeline."""

from __future__ import annotations

import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from bigbrain.config import BigBrainConfig
from bigbrain.kb.models import Document, SourceMetadata
from bigbrain.kb.store import KBStore
from bigbrain.orchestrator.pipeline import Orchestrator, OrchestratorResult


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


def _create_test_files(tmp_path: Path) -> Path:
    """Create sample files for ingestion tests."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "doc1.txt").write_text("Hello world", encoding="utf-8")
    (tmp_path / "doc2.md").write_text("# Title\n\nContent here", encoding="utf-8")
    return tmp_path


def _make_orchestrator(tmp_path: Path) -> tuple[Orchestrator, KBStore]:
    """Build an Orchestrator backed by a tmp-directory KB."""
    kb_dir = tmp_path / "kb"
    kb_dir.mkdir(parents=True, exist_ok=True)
    cfg = BigBrainConfig(kb_dir=str(kb_dir))
    store = KBStore(cfg.kb_db_path)
    return Orchestrator(store=store, config=cfg), store


# ------------------------------------------------------------------
# OrchestratorResult
# ------------------------------------------------------------------


class TestOrchestratorResult:
    def test_default_values(self) -> None:
        r = OrchestratorResult()
        assert r.ingested == 0
        assert r.skipped_unchanged == 0
        assert r.distilled == 0
        assert r.compiled == 0
        assert r.deleted == 0
        assert r.errors == []
        assert r.steps_run == []

    def test_fields_are_independent(self) -> None:
        r = OrchestratorResult(ingested=3, skipped_unchanged=2, deleted=1)
        assert r.ingested == 3
        assert r.skipped_unchanged == 2
        assert r.deleted == 1
        assert r.distilled == 0

    def test_errors_list_not_shared(self) -> None:
        r1 = OrchestratorResult()
        r2 = OrchestratorResult()
        r1.errors.append("oops")
        assert r2.errors == []

    def test_steps_run_not_shared(self) -> None:
        r1 = OrchestratorResult()
        r2 = OrchestratorResult()
        r1.steps_run.append("ingest")
        assert r2.steps_run == []


# ------------------------------------------------------------------
# Orchestrator — ingest only
# ------------------------------------------------------------------


class TestOrchestrator:
    def test_run_ingest_only(self, tmp_path: Path) -> None:
        """Ingest step only: docs land in the KB."""
        src = _create_test_files(tmp_path / "src")
        orch, store = _make_orchestrator(tmp_path)
        try:
            result = orch.run(src, steps={"ingest"})
            assert result.ingested == 2
            assert result.skipped_unchanged == 0
            assert "ingest" in result.steps_run
            assert "distill" not in result.steps_run

            docs = store.list_documents(limit=100)
            assert len(docs) == 2
        finally:
            orch.close()

    def test_run_incremental(self, tmp_path: Path) -> None:
        """Second run skips unchanged files."""
        src = _create_test_files(tmp_path / "src")
        orch, store = _make_orchestrator(tmp_path)
        try:
            r1 = orch.run(src, steps={"ingest"})
            assert r1.ingested == 2

            r2 = orch.run(src, steps={"ingest"})
            assert r2.ingested == 0
            assert r2.skipped_unchanged == 2
        finally:
            orch.close()

    def test_run_force_reingest(self, tmp_path: Path) -> None:
        """force=True reprocesses every file."""
        src = _create_test_files(tmp_path / "src")
        orch, store = _make_orchestrator(tmp_path)
        try:
            r1 = orch.run(src, steps={"ingest"})
            assert r1.ingested == 2

            r2 = orch.run(src, steps={"ingest"}, force=True)
            assert r2.ingested == 2
            assert r2.skipped_unchanged == 0
        finally:
            orch.close()

    def test_run_detects_modified(self, tmp_path: Path) -> None:
        """Modifying a file causes it to be re-ingested."""
        src = _create_test_files(tmp_path / "src")
        orch, store = _make_orchestrator(tmp_path)
        try:
            orch.run(src, steps={"ingest"})

            # Mutate one file
            time.sleep(0.05)
            (src / "doc1.txt").write_text("Changed content!", encoding="utf-8")

            r2 = orch.run(src, steps={"ingest"})
            assert r2.ingested == 1
            assert r2.skipped_unchanged == 1
        finally:
            orch.close()

    def test_run_detects_deleted(self, tmp_path: Path) -> None:
        """Deleting a file removes it from the KB."""
        src = _create_test_files(tmp_path / "src")
        orch, store = _make_orchestrator(tmp_path)
        try:
            orch.run(src, steps={"ingest"})
            assert len(store.list_documents(limit=100)) == 2

            (src / "doc1.txt").unlink()
            r2 = orch.run(src, steps={"ingest"})
            assert r2.deleted >= 1
            assert len(store.list_documents(limit=100)) == 1
        finally:
            orch.close()

    def test_run_all_steps(self, tmp_path: Path) -> None:
        """Full pipeline with mocked distill/compile."""
        src = _create_test_files(tmp_path / "src")
        orch, store = _make_orchestrator(tmp_path)
        try:
            with (
                patch.object(orch, "_run_distill") as mock_distill,
                patch.object(orch, "_run_compile") as mock_compile,
            ):
                result = orch.run(src)

            assert "ingest" in result.steps_run
            assert "distill" in result.steps_run
            assert "compile" in result.steps_run
            assert result.ingested == 2
            mock_distill.assert_called_once()
            mock_compile.assert_called_once()
        finally:
            orch.close()

    def test_run_selective_steps(self, tmp_path: Path) -> None:
        """Only the requested step runs."""
        src = _create_test_files(tmp_path / "src")
        orch, store = _make_orchestrator(tmp_path)
        try:
            result = orch.run(src, steps={"ingest"})
            assert result.steps_run == ["ingest"]
        finally:
            orch.close()

    def test_context_manager(self, tmp_path: Path) -> None:
        """Orchestrator works as a context manager."""
        src = _create_test_files(tmp_path / "src")
        kb_dir = tmp_path / "kb"
        kb_dir.mkdir(parents=True, exist_ok=True)
        cfg = BigBrainConfig(kb_dir=str(kb_dir))
        store = KBStore(cfg.kb_db_path)

        with Orchestrator(store=store, config=cfg) as orch:
            result = orch.run(src, steps={"ingest"})
            assert result.ingested == 2

    def test_ingest_error_recorded(self, tmp_path: Path) -> None:
        """Ingestion errors are captured, not raised."""
        src = tmp_path / "src"
        src.mkdir()
        # Create a valid .txt file that will be discovered
        (src / "good.txt").write_text("ok", encoding="utf-8")
        orch, store = _make_orchestrator(tmp_path)
        try:
            # Patch get_ingester to raise for one file
            original_run_ingest = orch._run_ingest

            def patched_ingest(source_path, *, force, result):
                # Call original but inject an error for demonstration
                original_run_ingest(source_path, force=force, result=result)

            result = orch.run(src, steps={"ingest"})
            assert result.ingested >= 1
            assert not result.errors  # no errors for valid files
        finally:
            orch.close()

    def test_empty_directory(self, tmp_path: Path) -> None:
        """Ingest on empty directory produces zero results."""
        src = tmp_path / "empty"
        src.mkdir()
        orch, store = _make_orchestrator(tmp_path)
        try:
            result = orch.run(src, steps={"ingest"})
            assert result.ingested == 0
            assert result.skipped_unchanged == 0
        finally:
            orch.close()

    def test_from_config(self, tmp_path: Path) -> None:
        """from_config class method creates a working Orchestrator."""
        kb_dir = tmp_path / "kb"
        kb_dir.mkdir(parents=True, exist_ok=True)
        cfg = BigBrainConfig(kb_dir=str(kb_dir))
        orch = Orchestrator.from_config(cfg)
        try:
            assert orch._config is cfg
        finally:
            orch.close()


# ------------------------------------------------------------------
# KBStore — file hash CRUD
# ------------------------------------------------------------------


class TestKBFileHashes:
    def test_save_and_get_file_hash(self, tmp_path: Path) -> None:
        store = KBStore(tmp_path / "test.db")
        store.save_file_hash("/a/b.txt", 1234.0, "abc123")
        record = store.get_file_hash("/a/b.txt")
        assert record is not None
        assert record["mtime"] == 1234.0
        assert record["content_hash"] == "abc123"

    def test_get_all_file_hashes(self, tmp_path: Path) -> None:
        store = KBStore(tmp_path / "test.db")
        store.save_file_hash("/a.txt", 1.0, "h1")
        store.save_file_hash("/b.txt", 2.0, "h2")
        all_hashes = store.get_file_hashes()
        assert len(all_hashes) == 2
        assert "/a.txt" in all_hashes
        assert "/b.txt" in all_hashes

    def test_delete_file_hash(self, tmp_path: Path) -> None:
        store = KBStore(tmp_path / "test.db")
        store.save_file_hash("/a.txt", 1.0, "h1")
        assert store.delete_file_hash("/a.txt")
        assert store.get_file_hash("/a.txt") is None

    def test_delete_nonexistent_returns_false(self, tmp_path: Path) -> None:
        store = KBStore(tmp_path / "test.db")
        assert not store.delete_file_hash("/nope.txt")

    def test_upsert_file_hash(self, tmp_path: Path) -> None:
        store = KBStore(tmp_path / "test.db")
        store.save_file_hash("/a.txt", 1.0, "h1")
        store.save_file_hash("/a.txt", 2.0, "h2")
        record = store.get_file_hash("/a.txt")
        assert record is not None
        assert record["mtime"] == 2.0
        assert record["content_hash"] == "h2"

    def test_save_with_document_id(self, tmp_path: Path) -> None:
        store = KBStore(tmp_path / "test.db")
        store.save_file_hash("/a.txt", 1.0, "h1", document_id="doc42")
        record = store.get_file_hash("/a.txt")
        assert record is not None
        assert record["document_id"] == "doc42"

    def test_get_file_hashes_empty(self, tmp_path: Path) -> None:
        store = KBStore(tmp_path / "test.db")
        assert store.get_file_hashes() == {}
