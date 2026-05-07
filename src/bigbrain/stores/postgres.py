"""PostgreSQL + pgvector backend for entity storage and vector search."""

from __future__ import annotations

import json
from typing import Any

from bigbrain.distill.models import Entity, Relationship
from bigbrain.logging_config import get_logger
from bigbrain.stores.base import EntityStoreBackend

logger = get_logger(__name__)


class PostgresBackend(EntityStoreBackend):
    """PostgreSQL backend with optional pgvector support for similarity search."""

    def __init__(self, connection_url: str) -> None:
        self._url = connection_url
        self._conn = None
        self._has_vector = False

    def _get_conn(self):
        if self._conn is None or self._conn.closed:
            import psycopg

            self._conn = psycopg.connect(self._url, autocommit=False)
            self._ensure_schema()
            if self._has_vector:
                try:
                    from pgvector.psycopg import register_vector

                    register_vector(self._conn)
                except Exception as exc:
                    logger.warning(
                        "pgvector Python registration unavailable; falling back to text search: %s",
                        exc,
                    )
                    self._has_vector = False
        return self._conn

    def _ensure_schema(self) -> None:
        conn = self._conn
        try:
            with conn.cursor() as cur:
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            conn.commit()
            vector_available = True
        except Exception as exc:
            conn.rollback()
            logger.warning(
                "pgvector extension unavailable; falling back to text search: %s",
                exc,
            )
            vector_available = False

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS bb_entities (
                    id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    entity_type TEXT NOT NULL DEFAULT '',
                    description TEXT NOT NULL DEFAULT '',
                    source_chunk_id TEXT NOT NULL DEFAULT '',
                    generated_by_provider TEXT NOT NULL DEFAULT '',
                    generated_by_model TEXT NOT NULL DEFAULT '',
                    metadata_json TEXT NOT NULL DEFAULT '{}'
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS bb_relationships (
                    id TEXT PRIMARY KEY,
                    source_entity_id TEXT NOT NULL,
                    target_entity_id TEXT NOT NULL,
                    relationship_type TEXT NOT NULL DEFAULT '',
                    description TEXT NOT NULL DEFAULT '',
                    document_id TEXT NOT NULL DEFAULT '',
                    generated_by_provider TEXT NOT NULL DEFAULT '',
                    generated_by_model TEXT NOT NULL DEFAULT '',
                    confidence REAL NOT NULL DEFAULT 1.0,
                    metadata_json TEXT NOT NULL DEFAULT '{}'
                )
            """)
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_bb_entities_doc ON bb_entities(document_id)"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_bb_entities_type ON bb_entities(entity_type)"
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_bb_rels_doc ON bb_relationships(document_id)"
            )
        conn.commit()

        if not vector_available:
            self._has_vector = False
            return

        try:
            with conn.cursor() as cur:
                cur.execute(
                    "ALTER TABLE bb_entities ADD COLUMN IF NOT EXISTS embedding vector(384)"
                )
            conn.commit()
            self._has_vector = True
        except Exception as exc:
            conn.rollback()
            logger.warning(
                "Failed to add pgvector embedding column; falling back to text search: %s",
                exc,
            )
            self._has_vector = False
            return

        try:
            with conn.cursor() as cur:
                cur.execute(
                    "CREATE INDEX IF NOT EXISTS idx_bb_entities_embedding "
                    "ON bb_entities USING hnsw (embedding vector_cosine_ops)"
                )
            conn.commit()
        except Exception as exc:
            conn.rollback()
            logger.warning("Failed to create pgvector HNSW index: %s", exc)

    @property
    def name(self) -> str:
        return "postgres"

    def is_available(self) -> bool:
        try:
            conn = self._get_conn()
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
            return True
        except Exception:
            return False

    def save_entities(self, entities: list[Entity]) -> int:
        conn = self._get_conn()
        with conn.cursor() as cur:
            for e in entities:
                metadata_json = json.dumps(e.metadata, default=str)
                if self._has_vector:
                    embedding = self._text_to_vector(f"{e.name} {e.description}")
                    cur.execute(
                        "INSERT INTO bb_entities (id, document_id, name, entity_type, description, "
                        "source_chunk_id, generated_by_provider, generated_by_model, embedding, metadata_json) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                        "ON CONFLICT(id) DO UPDATE SET name=EXCLUDED.name, entity_type=EXCLUDED.entity_type, "
                        "description=EXCLUDED.description, embedding=EXCLUDED.embedding, "
                        "metadata_json=EXCLUDED.metadata_json",
                        (
                            e.id,
                            e.document_id,
                            e.name,
                            e.entity_type,
                            e.description,
                            e.source_chunk_id,
                            e.generated_by_provider,
                            e.generated_by_model,
                            embedding,
                            metadata_json,
                        ),
                    )
                else:
                    cur.execute(
                        "INSERT INTO bb_entities (id, document_id, name, entity_type, description, "
                        "source_chunk_id, generated_by_provider, generated_by_model, metadata_json) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) "
                        "ON CONFLICT(id) DO UPDATE SET name=EXCLUDED.name, entity_type=EXCLUDED.entity_type, "
                        "description=EXCLUDED.description, metadata_json=EXCLUDED.metadata_json",
                        (
                            e.id,
                            e.document_id,
                            e.name,
                            e.entity_type,
                            e.description,
                            e.source_chunk_id,
                            e.generated_by_provider,
                            e.generated_by_model,
                            metadata_json,
                        ),
                    )
        conn.commit()
        return len(entities)

    def get_entities(self, document_id: str) -> list[Entity]:
        conn = self._get_conn()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id,document_id,name,entity_type,description,source_chunk_id,"
                "generated_by_provider,generated_by_model,metadata_json "
                "FROM bb_entities WHERE document_id=%s ORDER BY name",
                (document_id,),
            )
            return [self._row_to_entity(r) for r in cur.fetchall()]

    def list_all_entities(
        self, *, entity_type: str = "", search: str = "", limit: int = 500
    ) -> list[Entity]:
        conn = self._get_conn()
        conditions: list[str] = []
        params: list[Any] = []
        if entity_type:
            conditions.append("entity_type=%s")
            params.append(entity_type)
        if search:
            conditions.append("(name ILIKE %s OR description ILIKE %s)")
            params.extend([f"%{search}%", f"%{search}%"])
        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        params.append(limit)
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT id,document_id,name,entity_type,description,source_chunk_id,"
                f"generated_by_provider,generated_by_model,metadata_json "
                f"FROM bb_entities {where} ORDER BY entity_type,name LIMIT %s",
                params,
            )
            return [self._row_to_entity(r) for r in cur.fetchall()]

    def search_similar(
        self, query: str, *, limit: int = 10, entity_type: str = ""
    ) -> list[Entity]:
        conn = self._get_conn()
        if not self._has_vector:
            return super().search_similar(
                query, limit=limit, entity_type=entity_type
            )

        conditions = ["embedding IS NOT NULL"]
        params: list[Any] = []
        if entity_type:
            conditions.append("entity_type=%s")
            params.append(entity_type)
        params.extend([self._text_to_vector(query), limit])
        where = f"WHERE {' AND '.join(conditions)}"
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT id,document_id,name,entity_type,description,source_chunk_id,"
                f"generated_by_provider,generated_by_model,metadata_json "
                f"FROM bb_entities {where} "
                f"ORDER BY embedding <=> %s::vector LIMIT %s",
                params,
            )
            return [self._row_to_entity(r) for r in cur.fetchall()]

    def delete_entities(self, document_id: str) -> int:
        conn = self._get_conn()
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM bb_entities WHERE document_id=%s", (document_id,)
            )
            count = cur.rowcount
        conn.commit()
        return count

    def save_relationships(self, relationships: list[Relationship]) -> int:
        conn = self._get_conn()
        with conn.cursor() as cur:
            for r in relationships:
                cur.execute(
                    "INSERT INTO bb_relationships (id,source_entity_id,target_entity_id,"
                    "relationship_type,description,document_id,generated_by_provider,"
                    "generated_by_model,confidence,metadata_json) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT(id) DO UPDATE SET "
                    "relationship_type=EXCLUDED.relationship_type,description=EXCLUDED.description",
                    (
                        r.id,
                        r.source_entity_id,
                        r.target_entity_id,
                        r.relationship_type,
                        r.description,
                        r.document_id,
                        r.generated_by_provider,
                        r.generated_by_model,
                        r.confidence,
                        json.dumps(r.metadata, default=str),
                    ),
                )
        conn.commit()
        return len(relationships)

    def get_relationships(self, document_id: str) -> list[Relationship]:
        conn = self._get_conn()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id,source_entity_id,target_entity_id,relationship_type,description,"
                "document_id,generated_by_provider,generated_by_model,confidence,metadata_json "
                "FROM bb_relationships WHERE document_id=%s",
                (document_id,),
            )
            return [
                Relationship(
                    id=r[0],
                    source_entity_id=r[1],
                    target_entity_id=r[2],
                    relationship_type=r[3],
                    description=r[4],
                    document_id=r[5],
                    generated_by_provider=r[6],
                    generated_by_model=r[7],
                    confidence=r[8],
                    metadata=json.loads(r[9]),
                )
                for r in cur.fetchall()
            ]

    def delete_relationships(self, document_id: str) -> int:
        conn = self._get_conn()
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM bb_relationships WHERE document_id=%s", (document_id,)
            )
            count = cur.rowcount
        conn.commit()
        return count

    def close(self) -> None:
        if self._conn and not self._conn.closed:
            self._conn.close()

    @staticmethod
    def _text_to_vector(text: str, dim: int = 384) -> list[float]:
        """Simple hash-based vector (placeholder — real impl uses sentence-transformers)."""
        import hashlib

        h = hashlib.sha512(text.encode()).digest()
        raw = [float(b) / 255.0 for b in h]
        while len(raw) < dim:
            raw = raw + raw
        return raw[:dim]

    @staticmethod
    def _row_to_entity(row: tuple[Any, ...]) -> Entity:
        return Entity(
            id=row[0],
            document_id=row[1],
            name=row[2],
            entity_type=row[3],
            description=row[4],
            source_chunk_id=row[5],
            generated_by_provider=row[6],
            generated_by_model=row[7],
            metadata=json.loads(row[8]),
        )
