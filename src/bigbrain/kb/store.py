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

_SCHEMA_VERSION = 5

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

CREATE TABLE IF NOT EXISTS chunks (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    content TEXT NOT NULL DEFAULT '',
    content_hash TEXT NOT NULL DEFAULT '',
    start_offset INTEGER NOT NULL DEFAULT 0,
    end_offset INTEGER NOT NULL DEFAULT 0,
    section_title TEXT NOT NULL DEFAULT '',
    chunk_index INTEGER NOT NULL DEFAULT 0,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    UNIQUE(document_id, chunk_index)
);

CREATE TABLE IF NOT EXISTS summaries (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_id TEXT NOT NULL DEFAULT '',
    content TEXT NOT NULL DEFAULT '',
    summary_type TEXT NOT NULL DEFAULT 'document',
    generated_by_provider TEXT NOT NULL DEFAULT '',
    generated_by_model TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT '',
    metadata_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS entities (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    entity_type TEXT NOT NULL DEFAULT 'other',
    description TEXT NOT NULL DEFAULT '',
    source_chunk_id TEXT NOT NULL DEFAULT '',
    generated_by_provider TEXT NOT NULL DEFAULT '',
    generated_by_model TEXT NOT NULL DEFAULT '',
    metadata_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS relationships (
    id TEXT PRIMARY KEY,
    source_entity_id TEXT NOT NULL,
    target_entity_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL DEFAULT 'related_to',
    description TEXT NOT NULL DEFAULT '',
    document_id TEXT NOT NULL DEFAULT '',
    generated_by_provider TEXT NOT NULL DEFAULT '',
    generated_by_model TEXT NOT NULL DEFAULT '',
    confidence REAL NOT NULL DEFAULT 1.0,
    metadata_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS notion_sync (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    notion_page_id TEXT NOT NULL,
    sync_direction TEXT NOT NULL DEFAULT 'bidirectional',
    last_synced_at TEXT,
    notion_last_edited TEXT,
    local_last_edited TEXT,
    status TEXT NOT NULL DEFAULT 'synced',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    UNIQUE(document_id, notion_page_id)
);

CREATE TABLE IF NOT EXISTS file_hashes (
    file_path TEXT PRIMARY KEY,
    mtime REAL NOT NULL DEFAULT 0,
    content_hash TEXT NOT NULL DEFAULT '',
    last_ingested_at TEXT NOT NULL DEFAULT '',
    document_id TEXT NOT NULL DEFAULT ''
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
        """Create tables/triggers if not present and run migrations."""
        with self._lock:
            self._conn.executescript(_SCHEMA_SQL)
            # executescript issues an implicit COMMIT and can reset PRAGMAs;
            # re-enable foreign keys to be safe.
            self._conn.execute("PRAGMA foreign_keys = ON")
            version = self._conn.execute("PRAGMA user_version").fetchone()[0]
            if version < _SCHEMA_VERSION:
                self._run_migrations(version)
                self._conn.execute(f"PRAGMA user_version = {_SCHEMA_VERSION}")
                self._conn.execute(
                    "INSERT INTO documents_fts(documents_fts) VALUES ('rebuild')"
                )
                self._conn.commit()

    def _run_migrations(self, from_version: int) -> None:
        """Apply incremental schema migrations."""
        if from_version < 3:
            # v3: add content_hash column to chunks table
            try:
                self._conn.execute(
                    "ALTER TABLE chunks ADD COLUMN content_hash TEXT NOT NULL DEFAULT ''"
                )
                logger.info("Schema migration: added content_hash to chunks table")
            except Exception:
                pass  # Column already exists (fresh DB created with v3 schema)

        if from_version < 4:
            try:
                self._conn.executescript("""
                    CREATE TABLE IF NOT EXISTS notion_sync (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
                        notion_page_id TEXT NOT NULL,
                        sync_direction TEXT NOT NULL DEFAULT 'bidirectional',
                        last_synced_at TEXT,
                        notion_last_edited TEXT,
                        local_last_edited TEXT,
                        status TEXT NOT NULL DEFAULT 'synced',
                        metadata_json TEXT NOT NULL DEFAULT '{}',
                        UNIQUE(document_id, notion_page_id)
                    );
                """)
                logger.info("Schema migration: added notion_sync table")
            except Exception:
                pass

        if from_version < 5:
            try:
                self._conn.execute("""
                    CREATE TABLE IF NOT EXISTS file_hashes (
                        file_path TEXT PRIMARY KEY,
                        mtime REAL NOT NULL DEFAULT 0,
                        content_hash TEXT NOT NULL DEFAULT '',
                        last_ingested_at TEXT NOT NULL DEFAULT '',
                        document_id TEXT NOT NULL DEFAULT ''
                    )
                """)
                logger.info("Schema migration: added file_hashes table")
            except Exception:
                pass

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

    def resolve_doc_id(self, prefix: str) -> str | None:
        """Resolve a doc ID prefix to a full ID.

        Returns the full ID if exactly one document matches the prefix,
        or ``None`` if zero or multiple documents match.
        """
        with self._lock:
            rows = self._conn.execute(
                "SELECT id FROM documents WHERE id LIKE ? || '%'", (prefix,)
            ).fetchall()
        if len(rows) == 1:
            return rows[0][0]
        return None

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

            total_chunks = self._conn.execute(
                "SELECT COUNT(*) FROM chunks"
            ).fetchone()[0]

            total_summaries = self._conn.execute(
                "SELECT COUNT(*) FROM summaries"
            ).fetchone()[0]

            total_entities = self._conn.execute(
                "SELECT COUNT(*) FROM entities"
            ).fetchone()[0]

            total_relationships = self._conn.execute(
                "SELECT COUNT(*) FROM relationships"
            ).fetchone()[0]

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
            "total_chunks": total_chunks,
            "total_summaries": total_summaries,
            "total_entities": total_entities,
            "total_relationships": total_relationships,
            "by_type": by_type,
            "last_successful_run": _run_dict(last_ok),
            "last_failed_run": _run_dict(last_fail),
        }

    # ------------------------------------------------------------------
    # Chunks
    # ------------------------------------------------------------------

    def save_chunks(self, chunks: list) -> int:
        """Save chunks for a document. Replaces existing chunks. Returns count saved."""
        if not chunks:
            return 0
        doc_id = chunks[0].document_id
        with self._lock:
            with self._conn:
                self._conn.execute("DELETE FROM chunks WHERE document_id = ?", (doc_id,))
                for chunk in chunks:
                    self._conn.execute(
                        "INSERT INTO chunks (id, document_id, content, content_hash, "
                        "start_offset, end_offset, section_title, chunk_index, metadata_json) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            chunk.id, chunk.document_id, chunk.content,
                            chunk.content_hash,
                            chunk.start_offset, chunk.end_offset,
                            chunk.section_title, chunk.chunk_index,
                            json.dumps(chunk.metadata, default=str),
                        ),
                    )
        return len(chunks)

    def get_chunks(self, document_id: str) -> list:
        """Get all chunks for a document."""
        from bigbrain.distill.models import Chunk

        with self._lock:
            rows = self._conn.execute(
                "SELECT id, document_id, content, content_hash, start_offset, "
                "end_offset, section_title, chunk_index, metadata_json "
                "FROM chunks WHERE document_id = ? ORDER BY chunk_index",
                (document_id,),
            ).fetchall()
        return [
            Chunk(
                id=r[0], document_id=r[1], content=r[2],
                content_hash=r[3],
                start_offset=r[4], end_offset=r[5],
                section_title=r[6], chunk_index=r[7],
                metadata=json.loads(r[8]),
            )
            for r in rows
        ]

    def get_chunk_hashes(self, document_id: str) -> dict[int, str]:
        """Get a mapping of chunk_index → content_hash for a document.
        
        Used for incremental distillation — compare new chunk hashes
        against stored ones to skip unchanged chunks.
        """
        with self._lock:
            rows = self._conn.execute(
                "SELECT chunk_index, content_hash FROM chunks WHERE document_id = ?",
                (document_id,),
            ).fetchall()
        return {r[0]: r[1] for r in rows}

    # ------------------------------------------------------------------
    # Summaries
    # ------------------------------------------------------------------

    def save_summaries(self, summaries: list) -> int:
        """Save summaries. Returns count saved."""
        with self._lock:
            with self._conn:
                for s in summaries:
                    self._conn.execute(
                        "INSERT OR REPLACE INTO summaries (id, document_id, chunk_id, "
                        "content, summary_type, generated_by_provider, generated_by_model, "
                        "created_at, metadata_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            s.id, s.document_id, s.chunk_id, s.content,
                            s.summary_type, s.generated_by_provider,
                            s.generated_by_model,
                            s.created_at.isoformat() if hasattr(s.created_at, "isoformat") else str(s.created_at),
                            json.dumps(s.metadata, default=str),
                        ),
                    )
        return len(summaries)

    def get_summaries(self, document_id: str) -> list:
        """Get all summaries for a document."""
        from bigbrain.distill.models import Summary

        with self._lock:
            rows = self._conn.execute(
                "SELECT id, document_id, chunk_id, content, summary_type, "
                "generated_by_provider, generated_by_model, created_at, metadata_json "
                "FROM summaries WHERE document_id = ? ORDER BY summary_type",
                (document_id,),
            ).fetchall()
        return [
            Summary(
                id=r[0], document_id=r[1], chunk_id=r[2], content=r[3],
                summary_type=r[4], generated_by_provider=r[5],
                generated_by_model=r[6], metadata=json.loads(r[8]),
            )
            for r in rows
        ]

    # ------------------------------------------------------------------
    # Entities
    # ------------------------------------------------------------------

    def save_entities(self, entities: list) -> int:
        """Save entities. Returns count saved."""
        with self._lock:
            with self._conn:
                for e in entities:
                    self._conn.execute(
                        "INSERT OR REPLACE INTO entities (id, document_id, name, "
                        "entity_type, description, source_chunk_id, "
                        "generated_by_provider, generated_by_model, metadata_json) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            e.id, e.document_id, e.name, e.entity_type,
                            e.description, e.source_chunk_id,
                            e.generated_by_provider, e.generated_by_model,
                            json.dumps(e.metadata, default=str),
                        ),
                    )
        return len(entities)

    def get_entities(self, document_id: str) -> list:
        """Get all entities for a document."""
        from bigbrain.distill.models import Entity

        with self._lock:
            rows = self._conn.execute(
                "SELECT id, document_id, name, entity_type, description, "
                "source_chunk_id, generated_by_provider, generated_by_model, "
                "metadata_json FROM entities WHERE document_id = ? ORDER BY name",
                (document_id,),
            ).fetchall()
        return [
            Entity(
                id=r[0], document_id=r[1], name=r[2], entity_type=r[3],
                description=r[4], source_chunk_id=r[5],
                generated_by_provider=r[6], generated_by_model=r[7],
                metadata=json.loads(r[8]),
            )
            for r in rows
        ]

    def list_all_entities(
        self,
        *,
        entity_type: str = "",
        search: str = "",
        limit: int = 500,
    ) -> list:
        """List all entities across all documents with optional filters."""
        from bigbrain.distill.models import Entity

        conditions = []
        params: list = []

        if entity_type:
            conditions.append("entity_type = ?")
            params.append(entity_type)
        if search:
            conditions.append("(name LIKE ? OR description LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%"])

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        params.append(limit)

        with self._lock:
            rows = self._conn.execute(
                f"SELECT id, document_id, name, entity_type, description, "
                f"source_chunk_id, generated_by_provider, generated_by_model, "
                f"metadata_json FROM entities {where} ORDER BY entity_type, name LIMIT ?",
                params,
            ).fetchall()
        return [
            Entity(
                id=r[0], document_id=r[1], name=r[2], entity_type=r[3],
                description=r[4], source_chunk_id=r[5],
                generated_by_provider=r[6], generated_by_model=r[7],
                metadata=json.loads(r[8]),
            )
            for r in rows
        ]

    def get_entity_types(self) -> list[tuple[str, int]]:
        """Return all entity types with counts, sorted by count descending."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT entity_type, COUNT(*) FROM entities GROUP BY entity_type ORDER BY COUNT(*) DESC"
            ).fetchall()
        return [(r[0], r[1]) for r in rows]

    def dedup_entities(self) -> int:
        """Remove duplicate entities (same name+type, keep longest description).
        
        Returns count of removed duplicates.
        """
        with self._lock:
            # Find duplicates: group by lowercase name + entity_type
            rows = self._conn.execute(
                "SELECT id, LOWER(TRIM(name)), entity_type, LENGTH(description) "
                "FROM entities ORDER BY LOWER(TRIM(name)), entity_type, LENGTH(description) DESC"
            ).fetchall()

        # Group by (normalized_name, type), keep the one with longest description
        seen: dict[tuple[str, str], str] = {}  # (name, type) → best id
        to_delete: list[str] = []

        for row_id, name, etype, desc_len in rows:
            key = (name, etype)
            if key not in seen:
                seen[key] = row_id
            else:
                to_delete.append(row_id)

        if to_delete:
            with self._lock:
                with self._conn:
                    for eid in to_delete:
                        self._conn.execute("DELETE FROM entities WHERE id = ?", (eid,))
            logger.info("Deduplicated entities: removed %d duplicates", len(to_delete))

        return len(to_delete)

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    def save_relationships(self, relationships: list) -> int:
        """Save relationships. Returns count saved."""
        with self._lock:
            with self._conn:
                for r in relationships:
                    self._conn.execute(
                        "INSERT OR REPLACE INTO relationships (id, source_entity_id, "
                        "target_entity_id, relationship_type, description, document_id, "
                        "generated_by_provider, generated_by_model, confidence, "
                        "metadata_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            r.id, r.source_entity_id, r.target_entity_id,
                            r.relationship_type, r.description, r.document_id,
                            r.generated_by_provider, r.generated_by_model,
                            r.confidence, json.dumps(r.metadata, default=str),
                        ),
                    )
        return len(relationships)

    def get_relationships(self, document_id: str) -> list:
        """Get all relationships for a document."""
        from bigbrain.distill.models import Relationship

        with self._lock:
            rows = self._conn.execute(
                "SELECT id, source_entity_id, target_entity_id, relationship_type, "
                "description, document_id, generated_by_provider, generated_by_model, "
                "confidence, metadata_json "
                "FROM relationships WHERE document_id = ? ORDER BY relationship_type",
                (document_id,),
            ).fetchall()
        return [
            Relationship(
                id=r[0], source_entity_id=r[1], target_entity_id=r[2],
                relationship_type=r[3], description=r[4], document_id=r[5],
                generated_by_provider=r[6], generated_by_model=r[7],
                confidence=r[8], metadata=json.loads(r[9]),
            )
            for r in rows
        ]

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

    # ------------------------------------------------------------------
    # Notion Sync
    # ------------------------------------------------------------------

    def save_sync_mapping(self, document_id: str, notion_page_id: str, **kwargs) -> None:
        """Save or update a document↔Notion page sync mapping."""
        now = _utcnow()
        with self._lock:
            with self._conn:
                self._conn.execute(
                    "INSERT INTO notion_sync (document_id, notion_page_id, sync_direction, "
                    "last_synced_at, notion_last_edited, local_last_edited, status, metadata_json) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?) "
                    "ON CONFLICT(document_id, notion_page_id) DO UPDATE SET "
                    "last_synced_at = excluded.last_synced_at, "
                    "notion_last_edited = excluded.notion_last_edited, "
                    "local_last_edited = excluded.local_last_edited, "
                    "status = excluded.status, "
                    "metadata_json = excluded.metadata_json",
                    (
                        document_id, notion_page_id,
                        kwargs.get("sync_direction", "bidirectional"),
                        now,
                        kwargs.get("notion_last_edited", ""),
                        kwargs.get("local_last_edited", ""),
                        kwargs.get("status", "synced"),
                        json.dumps(kwargs.get("metadata", {}), default=str),
                    ),
                )

    def get_sync_mapping(self, document_id: str) -> dict | None:
        """Get the Notion sync mapping for a document."""
        with self._lock:
            row = self._conn.execute(
                "SELECT document_id, notion_page_id, sync_direction, last_synced_at, "
                "notion_last_edited, local_last_edited, status, metadata_json "
                "FROM notion_sync WHERE document_id = ?",
                (document_id,),
            ).fetchone()
        if row is None:
            return None
        return {
            "document_id": row[0], "notion_page_id": row[1],
            "sync_direction": row[2], "last_synced_at": row[3],
            "notion_last_edited": row[4], "local_last_edited": row[5],
            "status": row[6], "metadata": json.loads(row[7]),
        }

    def get_sync_by_notion_id(self, notion_page_id: str) -> dict | None:
        """Get sync mapping by Notion page ID."""
        with self._lock:
            row = self._conn.execute(
                "SELECT document_id, notion_page_id, sync_direction, last_synced_at, "
                "notion_last_edited, local_last_edited, status, metadata_json "
                "FROM notion_sync WHERE notion_page_id = ?",
                (notion_page_id,),
            ).fetchone()
        if row is None:
            return None
        return {
            "document_id": row[0], "notion_page_id": row[1],
            "sync_direction": row[2], "last_synced_at": row[3],
            "notion_last_edited": row[4], "local_last_edited": row[5],
            "status": row[6], "metadata": json.loads(row[7]),
        }

    def list_sync_mappings(self) -> list[dict]:
        """List all Notion sync mappings."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT document_id, notion_page_id, sync_direction, last_synced_at, "
                "notion_last_edited, local_last_edited, status, metadata_json "
                "FROM notion_sync ORDER BY last_synced_at DESC"
            ).fetchall()
        return [
            {
                "document_id": r[0], "notion_page_id": r[1],
                "sync_direction": r[2], "last_synced_at": r[3],
                "notion_last_edited": r[4], "local_last_edited": r[5],
                "status": r[6], "metadata": json.loads(r[7]),
            }
            for r in rows
        ]

    def delete_sync_mapping(self, document_id: str) -> bool:
        """Remove a sync mapping."""
        with self._lock:
            with self._conn:
                cur = self._conn.execute(
                    "DELETE FROM notion_sync WHERE document_id = ?", (document_id,)
                )
            return cur.rowcount > 0

    # ------------------------------------------------------------------
    # File hash tracking (incremental ingestion)
    # ------------------------------------------------------------------

    def save_file_hash(self, file_path: str, mtime: float, content_hash: str, document_id: str = "") -> None:
        """Save or update a file hash record for change tracking."""
        now = _utcnow()
        with self._lock:
            with self._conn:
                self._conn.execute(
                    "INSERT INTO file_hashes (file_path, mtime, content_hash, last_ingested_at, document_id) "
                    "VALUES (?, ?, ?, ?, ?) "
                    "ON CONFLICT(file_path) DO UPDATE SET "
                    "mtime = excluded.mtime, content_hash = excluded.content_hash, "
                    "last_ingested_at = excluded.last_ingested_at, document_id = excluded.document_id",
                    (file_path, mtime, content_hash, now, document_id),
                )

    def get_file_hashes(self) -> dict[str, dict]:
        """Get all file hash records. Returns {file_path: {mtime, content_hash, document_id}}."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT file_path, mtime, content_hash, last_ingested_at, document_id FROM file_hashes"
            ).fetchall()
        return {
            r[0]: {"mtime": r[1], "content_hash": r[2], "last_ingested_at": r[3], "document_id": r[4]}
            for r in rows
        }

    def get_file_hash(self, file_path: str) -> dict | None:
        """Get a single file hash record."""
        with self._lock:
            row = self._conn.execute(
                "SELECT file_path, mtime, content_hash, last_ingested_at, document_id "
                "FROM file_hashes WHERE file_path = ?",
                (file_path,),
            ).fetchone()
        if row is None:
            return None
        return {"file_path": row[0], "mtime": row[1], "content_hash": row[2], "last_ingested_at": row[3], "document_id": row[4]}

    def delete_file_hash(self, file_path: str) -> bool:
        """Remove a file hash record."""
        with self._lock:
            with self._conn:
                cur = self._conn.execute("DELETE FROM file_hashes WHERE file_path = ?", (file_path,))
            return cur.rowcount > 0
