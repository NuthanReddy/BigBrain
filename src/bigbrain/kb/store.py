"""SQLite-backed knowledge base storage.

Provides :class:`KBStore` for persisting :class:`Document` objects and
:class:`IngestionResult` records into a local SQLite database with FTS5
full-text search support.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from bigbrain.kb.models import Document, DocumentSection, IngestionResult, SourceMetadata
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)

_SCHEMA_VERSION = 1

_SCHEMA_SQL = """\
CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL DEFAULT '',
    language TEXT NOT NULL DEFAULT '',
    file_path TEXT NOT NULL UNIQUE,
    source_type TEXT NOT NULL DEFAULT '',
    file_extension TEXT NOT NULL DEFAULT '',
    size_bytes INTEGER NOT NULL DEFAULT 0,
    modified_at TEXT,
    source_extra_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    title TEXT NOT NULL DEFAULT '',
    content TEXT NOT NULL DEFAULT '',
    level INTEGER NOT NULL DEFAULT 0,
    position INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    UNIQUE(document_id, position)
);

CREATE TABLE IF NOT EXISTS ingestion_runs (
    id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    status TEXT NOT NULL DEFAULT 'in_progress',
    source_path TEXT NOT NULL DEFAULT '',
    processed INTEGER NOT NULL DEFAULT 0,
    skipped INTEGER NOT NULL DEFAULT 0,
    failed INTEGER NOT NULL DEFAULT 0,
    errors_json TEXT NOT NULL DEFAULT '[]',
    warnings_json TEXT NOT NULL DEFAULT '[]'
);

CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
    title, content, content=documents, content_rowid=rowid
);

CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
    INSERT INTO documents_fts(rowid, title, content)
        VALUES (new.rowid, new.title, new.content);
END;

CREATE TRIGGER IF NOT EXISTS documents_ad AFTER DELETE ON documents BEGIN
    INSERT INTO documents_fts(documents_fts, rowid, title, content)
        VALUES ('delete', old.rowid, old.title, old.content);
END;

CREATE TRIGGER IF NOT EXISTS documents_au AFTER UPDATE ON documents BEGIN
    INSERT INTO documents_fts(documents_fts, rowid, title, content)
        VALUES ('delete', old.rowid, old.title, old.content);
    INSERT INTO documents_fts(rowid, title, content)
        VALUES (new.rowid, new.title, new.content);
END;
"""

_UPSERT_DOCUMENT_SQL = """\
INSERT INTO documents (
    id, title, content, language,
    file_path, source_type, file_extension, size_bytes,
    modified_at, source_extra_json, metadata_json,
    created_at, updated_at
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(id) DO UPDATE SET
    title = excluded.title,
    content = excluded.content,
    language = excluded.language,
    file_path = excluded.file_path,
    source_type = excluded.source_type,
    file_extension = excluded.file_extension,
    size_bytes = excluded.size_bytes,
    modified_at = excluded.modified_at,
    source_extra_json = excluded.source_extra_json,
    metadata_json = excluded.metadata_json,
    updated_at = excluded.updated_at
"""

_INSERT_SECTION_SQL = """\
INSERT INTO sections (document_id, title, content, level, position, metadata_json)
VALUES (?, ?, ?, ?, ?, ?)
"""


def _utcnow() -> str:
    """Return current UTC time as ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _dt_to_iso(dt: datetime | None) -> str | None:
    """Convert a datetime to ISO-8601 string, or None."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def _iso_to_dt(iso: str | None) -> datetime | None:
    """Parse an ISO-8601 string back to a datetime, or None."""
    if not iso:
        return None
    return datetime.fromisoformat(iso)


class KBStore:
    """SQLite-backed knowledge base storage."""

    def __init__(self, db_path: str | Path) -> None:
        """Open or create the database at *db_path*.

        Creates parent directories if needed, enables WAL mode and foreign
        keys, and ensures the schema is up to date.
        """
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(
            str(self._db_path),
            check_same_thread=False,
        )
        self._conn.execute("PRAGMA journal_mode = WAL")
        self._conn.execute("PRAGMA busy_timeout = 5000")
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._ensure_schema()
        logger.debug("KBStore opened: %s", self._db_path)

    # ------------------------------------------------------------------
    # Schema management
    # ------------------------------------------------------------------

    def _ensure_schema(self) -> None:
        """Create tables/triggers if not present and set schema version."""
        with self._lock:
            self._conn.executescript(_SCHEMA_SQL)
            # executescript issues an implicit COMMIT and can reset PRAGMAs;
            # re-enable foreign keys to be safe.
            self._conn.execute("PRAGMA foreign_keys = ON")
            version = self._conn.execute("PRAGMA user_version").fetchone()[0]
            if version < _SCHEMA_VERSION:
                self._conn.execute(f"PRAGMA user_version = {_SCHEMA_VERSION}")
                self._conn.execute(
                    "INSERT INTO documents_fts(documents_fts) VALUES ('rebuild')"
                )
                self._conn.commit()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()
        logger.debug("KBStore closed: %s", self._db_path)

    def __enter__(self) -> KBStore:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    # ------------------------------------------------------------------
    # ID helpers
    # ------------------------------------------------------------------

    @staticmethod
    def make_document_id(file_path: str) -> str:
        """Deterministic document ID from a normalised absolute source path.

        Uses SHA-256 of the canonical path (resolved, case-folded on
        Windows) and returns the first 16 hex characters.
        """
        resolved = str(Path(file_path).resolve())
        if sys.platform == "win32":
            resolved = resolved.lower()
        return hashlib.sha256(resolved.encode()).hexdigest()[:16]

    # ------------------------------------------------------------------
    # Document CRUD
    # ------------------------------------------------------------------

    def save_document(self, doc: Document) -> str:
        """Upsert a document and its sections.  Returns the document ID.

        Raises :class:`ValueError` if ``doc.source`` is *None* (every
        persisted document must have provenance metadata).
        """
        if doc.source is None:
            raise ValueError("Cannot save a Document without SourceMetadata")

        doc_id = self.make_document_id(doc.source.file_path)
        now = _utcnow()

        doc_params = (
            doc_id,
            doc.title,
            doc.content,
            doc.language,
            doc.source.file_path,
            doc.source.source_type,
            doc.source.file_extension,
            doc.source.size_bytes,
            _dt_to_iso(doc.source.modified_at),
            json.dumps(doc.source.extra, default=str),
            json.dumps(doc.metadata, default=str),
            _dt_to_iso(doc.created_at) or now,
            now,
        )

        section_rows = [
            (
                doc_id,
                sec.title,
                sec.content,
                sec.level,
                idx,
                json.dumps(sec.metadata, default=str),
            )
            for idx, sec in enumerate(doc.sections)
        ]

        with self._lock:
            with self._conn:
                self._conn.execute(_UPSERT_DOCUMENT_SQL, doc_params)
                self._conn.execute(
                    "DELETE FROM sections WHERE document_id = ?", (doc_id,)
                )
                if section_rows:
                    self._conn.executemany(_INSERT_SECTION_SQL, section_rows)

        logger.debug("Saved document %s (%s)", doc_id, doc.source.file_path)
        return doc_id

    def get_document(self, doc_id: str) -> Document | None:
        """Retrieve a document by ID, including sections and source metadata."""
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM documents WHERE id = ?", (doc_id,)
            ).fetchone()
            if row is None:
                return None
            return self._row_to_document(row)

    def get_document_by_source_path(self, file_path: str) -> Document | None:
        """Retrieve a document by its original source file path."""
        doc_id = self.make_document_id(file_path)
        return self.get_document(doc_id)

    def list_documents(
        self,
        source_type: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Document]:
        """List documents, optionally filtered by *source_type*."""
        if source_type:
            sql = (
                "SELECT * FROM documents WHERE source_type = ? "
                "ORDER BY updated_at DESC LIMIT ? OFFSET ?"
            )
            params: tuple[Any, ...] = (source_type, limit, offset)
        else:
            sql = (
                "SELECT * FROM documents "
                "ORDER BY updated_at DESC LIMIT ? OFFSET ?"
            )
            params = (limit, offset)

        with self._lock:
            rows = self._conn.execute(sql, params).fetchall()
            return [self._row_to_document(r) for r in rows]

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document (sections cascade).  Returns *True* if found."""
        with self._lock:
            with self._conn:
                cur = self._conn.execute(
                    "DELETE FROM documents WHERE id = ?", (doc_id,)
                )
            return cur.rowcount > 0

    def search_documents(self, query: str, limit: int = 20) -> list[Document]:
        """Full-text search via FTS5.  Returns documents ranked by relevance."""
        if not query or not query.strip():
            return []

        sql = (
            "SELECT d.* FROM documents_fts f "
            "JOIN documents d ON d.rowid = f.rowid "
            "WHERE documents_fts MATCH ? "
            "ORDER BY rank LIMIT ?"
        )
        try:
            with self._lock:
                rows = self._conn.execute(sql, (query, limit)).fetchall()
                return [self._row_to_document(r) for r in rows]
        except sqlite3.OperationalError:
            logger.warning("FTS5 query failed for: %r", query)
            return []

    # ------------------------------------------------------------------
    # Ingestion runs
    # ------------------------------------------------------------------

    def save_ingestion_run(
        self, result: IngestionResult, source_path: str = ""
    ) -> str:
        """Persist an ingestion run record.  Returns the run ID."""
        run_id = str(uuid.uuid4())
        now = _utcnow()
        status = "failed" if result.failed > 0 else "succeeded"

        with self._lock:
            with self._conn:
                self._conn.execute(
                    "INSERT INTO ingestion_runs "
                    "(id, started_at, finished_at, status, source_path, "
                    " processed, skipped, failed, errors_json, warnings_json) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        run_id,
                        now,
                        now,
                        status,
                        source_path,
                        result.processed,
                        result.skipped,
                        result.failed,
                        json.dumps(result.errors),
                        json.dumps(result.warnings),
                    ),
                )

        logger.debug("Saved ingestion run %s (status=%s)", run_id, status)
        return run_id

    def list_ingestion_runs(self, limit: int = 10) -> list[dict]:
        """List recent ingestion runs, most recent first."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT * FROM ingestion_runs ORDER BY started_at DESC LIMIT ?",
                (limit,),
            ).fetchall()

        cols = [
            "id", "started_at", "finished_at", "status", "source_path",
            "processed", "skipped", "failed", "errors_json", "warnings_json",
        ]
        results: list[dict] = []
        for row in rows:
            d = dict(zip(cols, row))
            d["errors"] = json.loads(d.pop("errors_json"))
            d["warnings"] = json.loads(d.pop("warnings_json"))
            results.append(d)
        return results

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def get_stats(self) -> dict:
        """Return aggregate knowledge base statistics."""
        with self._lock:
            total_docs = self._conn.execute(
                "SELECT COUNT(*) FROM documents"
            ).fetchone()[0]

            total_sections = self._conn.execute(
                "SELECT COUNT(*) FROM sections"
            ).fetchone()[0]

            total_size = self._conn.execute(
                "SELECT COALESCE(SUM(size_bytes), 0) FROM documents"
            ).fetchone()[0]

            type_rows = self._conn.execute(
                "SELECT source_type, COUNT(*) FROM documents GROUP BY source_type"
            ).fetchall()
            by_type = {row[0]: row[1] for row in type_rows}

            last_ok = self._conn.execute(
                "SELECT * FROM ingestion_runs WHERE status = 'succeeded' "
                "ORDER BY started_at DESC LIMIT 1"
            ).fetchone()

            last_fail = self._conn.execute(
                "SELECT * FROM ingestion_runs WHERE status = 'failed' "
                "ORDER BY started_at DESC LIMIT 1"
            ).fetchone()

        run_cols = [
            "id", "started_at", "finished_at", "status", "source_path",
            "processed", "skipped", "failed", "errors_json", "warnings_json",
        ]

        def _run_dict(row: tuple | None) -> dict | None:
            if row is None:
                return None
            d = dict(zip(run_cols, row))
            d["errors"] = json.loads(d.pop("errors_json"))
            d["warnings"] = json.loads(d.pop("warnings_json"))
            return d

        return {
            "total_documents": total_docs,
            "total_sections": total_sections,
            "total_size_bytes": total_size,
            "by_type": by_type,
            "last_successful_run": _run_dict(last_ok),
            "last_failed_run": _run_dict(last_fail),
        }

    # ------------------------------------------------------------------
    # JSONL export / import
    # ------------------------------------------------------------------

    def export_jsonl(self, output_path: str | Path) -> int:
        """Export all documents to a JSONL file (one JSON object per line).

        Returns the number of documents exported.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        count = 0
        with open(output_path, "w", encoding="utf-8") as fh:
            offset = 0
            batch_size = 500
            while True:
                docs = self.list_documents(limit=batch_size, offset=offset)
                if not docs:
                    break
                for doc in docs:
                    line = json.dumps(
                        self._document_to_dict(doc), ensure_ascii=False
                    )
                    fh.write(line + "\n")
                    count += 1
                if len(docs) < batch_size:
                    break
                offset += batch_size

        logger.info("Exported %d document(s) to %s", count, output_path)
        return count

    def import_jsonl(
        self, input_path: str | Path, *, upsert: bool = True
    ) -> tuple[int, int]:
        """Import documents from a JSONL file.

        Parameters:
            input_path: path to the JSONL file
            upsert: if True, update existing docs; if False, skip existing

        Returns:
            tuple of (imported_count, skipped_count)
        """
        input_path = Path(input_path)
        imported = 0
        skipped = 0

        with open(input_path, "r", encoding="utf-8") as fh:
            for lineno, raw_line in enumerate(fh, start=1):
                raw_line = raw_line.strip()
                if not raw_line:
                    continue
                try:
                    obj = json.loads(raw_line)
                except json.JSONDecodeError as exc:
                    logger.warning(
                        "Skipping line %d: JSON parse error: %s", lineno, exc
                    )
                    skipped += 1
                    continue

                try:
                    doc = self._dict_to_document(obj)
                except (KeyError, TypeError, ValueError) as exc:
                    logger.warning(
                        "Skipping line %d: invalid document data: %s",
                        lineno,
                        exc,
                    )
                    skipped += 1
                    continue

                if not upsert:
                    existing_id = self.make_document_id(doc.source.file_path)
                    if self.get_document(existing_id) is not None:
                        skipped += 1
                        continue

                try:
                    self.save_document(doc)
                    imported += 1
                except Exception as exc:
                    logger.warning(
                        "Skipping line %d: save failed: %s", lineno, exc
                    )
                    skipped += 1

        logger.info(
            "Imported %d document(s), skipped %d from %s",
            imported,
            skipped,
            input_path,
        )
        return imported, skipped

    # ------------------------------------------------------------------
    # Serialisation helpers for JSONL
    # ------------------------------------------------------------------

    @staticmethod
    def _document_to_dict(doc: Document) -> dict[str, Any]:
        """Serialise a Document into a plain dict for JSON export."""
        source_dict: dict[str, Any] = {}
        if doc.source is not None:
            source_dict = {
                "file_path": doc.source.file_path,
                "file_extension": doc.source.file_extension,
                "source_type": doc.source.source_type,
                "modified_at": _dt_to_iso(doc.source.modified_at),
                "size_bytes": doc.source.size_bytes,
                "extra": doc.source.extra,
            }

        return {
            "id": doc.id,
            "title": doc.title,
            "content": doc.content,
            "language": doc.language,
            "source": source_dict,
            "sections": [
                {
                    "title": sec.title,
                    "content": sec.content,
                    "level": sec.level,
                    "metadata": sec.metadata,
                }
                for sec in doc.sections
            ],
            "metadata": doc.metadata,
            "created_at": _dt_to_iso(doc.created_at),
        }

    @staticmethod
    def _dict_to_document(obj: dict[str, Any]) -> Document:
        """Reconstruct a Document from a dict (inverse of _document_to_dict)."""
        src = obj.get("source", {})
        source = SourceMetadata(
            file_path=src["file_path"],
            file_extension=src.get("file_extension", ""),
            source_type=src.get("source_type", ""),
            modified_at=_iso_to_dt(src.get("modified_at")),
            size_bytes=src.get("size_bytes", 0),
            extra=src.get("extra", {}),
        )

        sections = [
            DocumentSection(
                title=s.get("title", ""),
                content=s.get("content", ""),
                level=s.get("level", 0),
                metadata=s.get("metadata", {}),
            )
            for s in obj.get("sections", [])
        ]

        return Document(
            title=obj.get("title", ""),
            content=obj.get("content", ""),
            source=source,
            language=obj.get("language", ""),
            sections=sections,
            metadata=obj.get("metadata", {}),
            created_at=_iso_to_dt(obj.get("created_at")) or datetime.now(timezone.utc),
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _row_to_document(self, row: tuple) -> Document:
        """Convert a raw ``documents`` row into a :class:`Document`.

        Also fetches the associated sections (must be called while
        ``self._lock`` is held).
        """
        (
            doc_id, title, content, language,
            file_path, source_type, file_extension, size_bytes,
            modified_at, source_extra_json, metadata_json,
            created_at, updated_at,
        ) = row

        section_rows = self._conn.execute(
            "SELECT title, content, level, position, metadata_json "
            "FROM sections WHERE document_id = ? ORDER BY position",
            (doc_id,),
        ).fetchall()

        sections = [
            DocumentSection(
                title=sr[0],
                content=sr[1],
                level=sr[2],
                metadata=json.loads(sr[4]),
            )
            for sr in section_rows
        ]

        source = SourceMetadata(
            file_path=file_path,
            file_extension=file_extension,
            source_type=source_type,
            modified_at=_iso_to_dt(modified_at),
            size_bytes=size_bytes,
            extra=json.loads(source_extra_json),
        )

        return Document(
            id=doc_id,
            title=title,
            content=content,
            source=source,
            language=language,
            sections=sections,
            metadata=json.loads(metadata_json),
            created_at=_iso_to_dt(created_at) or datetime.now(timezone.utc),
        )
