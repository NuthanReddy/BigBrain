"""Tests for bigbrain.orchestrator.change_detector."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from bigbrain.kb.store import KBStore
from bigbrain.orchestrator.change_detector import ChangeDetector, ChangeResult


@pytest.fixture()
def store(tmp_path: Path) -> KBStore:
    return KBStore(tmp_path / "test.db")


@pytest.fixture()
def detector(store: KBStore) -> ChangeDetector:
    return ChangeDetector(store)


@pytest.fixture()
def sample_file(tmp_path: Path) -> Path:
    p = tmp_path / "hello.txt"
    p.write_text("hello world")
    return p


# ------------------------------------------------------------------
# ChangeResult
# ------------------------------------------------------------------

class TestChangeResult:
    def test_empty_result(self) -> None:
        r = ChangeResult()
        assert not r.has_changes
        assert r.changed_files == []

    def test_has_changes_new(self) -> None:
        r = ChangeResult(new_files=[Path("a.txt")])
        assert r.has_changes

    def test_has_changes_modified(self) -> None:
        r = ChangeResult(modified_files=[Path("a.txt")])
        assert r.has_changes

    def test_has_changes_deleted(self) -> None:
        r = ChangeResult(deleted_paths=["/gone.txt"])
        assert r.has_changes

    def test_changed_files_combines(self) -> None:
        r = ChangeResult(
            new_files=[Path("a.txt")],
            modified_files=[Path("b.txt")],
        )
        assert len(r.changed_files) == 2


# ------------------------------------------------------------------
# ChangeDetector.file_hash
# ------------------------------------------------------------------

class TestFileHash:
    def test_deterministic(self, sample_file: Path) -> None:
        h1 = ChangeDetector.file_hash(sample_file)
        h2 = ChangeDetector.file_hash(sample_file)
        assert h1 == h2

    def test_full_sha256_length(self, sample_file: Path) -> None:
        h = ChangeDetector.file_hash(sample_file)
        assert len(h) == 64  # full SHA-256 hex digest

    def test_different_content_different_hash(self, tmp_path: Path) -> None:
        a = tmp_path / "a.txt"
        b = tmp_path / "b.txt"
        a.write_text("aaa")
        b.write_text("bbb")
        assert ChangeDetector.file_hash(a) != ChangeDetector.file_hash(b)


# ------------------------------------------------------------------
# scan()
# ------------------------------------------------------------------

class TestScan:
    def test_new_file_detected(self, detector: ChangeDetector, sample_file: Path) -> None:
        result = detector.scan([sample_file])
        assert sample_file in result.new_files
        assert not result.modified_files
        assert not result.deleted_paths

    def test_unchanged_after_save(self, detector: ChangeDetector, sample_file: Path) -> None:
        detector.save_file_record(sample_file)
        result = detector.scan([sample_file])
        assert sample_file in result.unchanged_files
        assert not result.has_changes

    def test_modified_file_detected(self, detector: ChangeDetector, sample_file: Path) -> None:
        detector.save_file_record(sample_file)
        # Mutate the file — change content and bump mtime
        time.sleep(0.05)
        sample_file.write_text("changed content")
        result = detector.scan([sample_file])
        assert sample_file in result.modified_files

    def test_deleted_file_detected(self, detector: ChangeDetector, sample_file: Path) -> None:
        detector.save_file_record(sample_file)
        sample_file.unlink()
        result = detector.scan([])  # empty snapshot
        assert len(result.deleted_paths) >= 1

    def test_unsupported_extension_skipped(self, detector: ChangeDetector, tmp_path: Path) -> None:
        p = tmp_path / "data.csv"
        p.write_text("a,b,c")
        result = detector.scan([p])
        assert not result.new_files

    def test_nonexistent_path_skipped(self, detector: ChangeDetector, tmp_path: Path) -> None:
        result = detector.scan([tmp_path / "ghost.txt"])
        assert not result.has_changes

    def test_custom_extensions(self, detector: ChangeDetector, tmp_path: Path) -> None:
        p = tmp_path / "data.csv"
        p.write_text("a,b,c")
        result = detector.scan([p], supported_extensions=[".csv"])
        assert p in result.new_files

    def test_mtime_same_content_same_is_unchanged(
        self, detector: ChangeDetector, store: KBStore, sample_file: Path,
    ) -> None:
        """If mtime changes but content hash is the same, file is unchanged."""
        key = detector._normalize_path(sample_file)
        content_hash = detector.file_hash(sample_file)
        # Store with a deliberately different mtime
        store.save_file_hash(key, 0.0, content_hash)
        result = detector.scan([sample_file])
        assert sample_file in result.unchanged_files


# ------------------------------------------------------------------
# save_file_record / remove_file_record
# ------------------------------------------------------------------

class TestRecordManagement:
    def test_save_and_retrieve(self, detector: ChangeDetector, store: KBStore, sample_file: Path) -> None:
        detector.save_file_record(sample_file)
        key = detector._normalize_path(sample_file)
        record = store.get_file_hash(key)
        assert record is not None
        assert record["content_hash"] == detector.file_hash(sample_file)

    def test_remove_record(self, detector: ChangeDetector, store: KBStore, sample_file: Path) -> None:
        detector.save_file_record(sample_file)
        key = detector._normalize_path(sample_file)
        assert detector.remove_file_record(key)
        assert store.get_file_hash(key) is None

    def test_remove_nonexistent_returns_false(self, detector: ChangeDetector) -> None:
        assert not detector.remove_file_record("/no/such/file")

    def test_save_with_document_id(self, detector: ChangeDetector, store: KBStore, sample_file: Path) -> None:
        detector.save_file_record(sample_file, document_id="doc123")
        key = detector._normalize_path(sample_file)
        record = store.get_file_hash(key)
        assert record is not None
        assert record["document_id"] == "doc123"
