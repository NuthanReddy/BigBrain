"""Real PostgreSQL integration tests for PostgresBackend with pgvector."""

from __future__ import annotations

import os

import pytest

from bigbrain.distill.models import Entity, Relationship
from bigbrain.stores.postgres import PostgresBackend

psycopg = pytest.importorskip("psycopg")

DEFAULT_POSTGRES_URL = "postgresql://postgres:bigbrain123@localhost:5432/bigbrain"
POSTGRES_URL = os.getenv("BIGBRAIN_POSTGRES_URL", DEFAULT_POSTGRES_URL)


def _postgres_available() -> bool:
    try:
        with psycopg.connect(POSTGRES_URL, connect_timeout=2) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return True
    except Exception:
        return False


def _pgvector_available() -> bool:
    if not _postgres_available():
        return False

    backend = PostgresBackend(POSTGRES_URL)
    try:
        backend._get_conn()
        return backend._has_vector
    except Exception:
        return False
    finally:
        backend.close()


PGVECTOR_AVAILABLE = _pgvector_available()


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not _postgres_available(),
        reason=f"Postgres not available at {POSTGRES_URL}",
    ),
]


def _truncate_tables(backend: PostgresBackend) -> None:
    conn = backend._get_conn()
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE bb_relationships, bb_entities")
    conn.commit()


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------


def _make_entities(doc_id: str = "doc-1") -> list[Entity]:
    return [
        Entity(
            id="e1",
            document_id=doc_id,
            name="BST",
            entity_type="data_structure",
            description="Binary search tree",
        ),
        Entity(
            id="e2",
            document_id=doc_id,
            name="Quicksort",
            entity_type="algorithm",
            description="Divide and conquer sort",
        ),
    ]



def _make_relationships(doc_id: str = "doc-1") -> list[Relationship]:
    return [
        Relationship(
            id="r1",
            source_entity_id="e1",
            target_entity_id="e2",
            relationship_type="related_to",
            description="BST relates to Quicksort",
            document_id=doc_id,
            confidence=0.9,
        )
    ]


class TestPostgresBackendIntegration:
    """Integration tests using a real PostgreSQL database with pgvector."""

    @pytest.fixture(autouse=True)
    def setup_backend(self):
        self.backend = PostgresBackend(POSTGRES_URL)
        self.backend._get_conn()
        _truncate_tables(self.backend)
        yield
        try:
            if self.backend._conn and not self.backend._conn.closed:
                _truncate_tables(self.backend)
        finally:
            self.backend.close()

    def test_is_available(self):
        assert self.backend.is_available() is True

    def test_save_and_get_entities(self):
        entities = _make_entities()
        saved = self.backend.save_entities(entities)

        assert saved == 2

        loaded = self.backend.get_entities("doc-1")
        assert len(loaded) == 2
        assert {entity.name for entity in loaded} == {"BST", "Quicksort"}

    def test_save_entities_upsert(self):
        entities = _make_entities()
        self.backend.save_entities(entities)

        entities[0].description = "Updated BST description"
        self.backend.save_entities(entities)

        loaded = self.backend.get_entities("doc-1")
        assert len(loaded) == 2
        assert next(entity for entity in loaded if entity.id == "e1").description == "Updated BST description"

    def test_get_entities_empty(self):
        assert self.backend.get_entities("nonexistent") == []

    def test_list_all_entities(self):
        self.backend.save_entities(_make_entities("doc-1"))
        self.backend.save_entities(
            [
                Entity(
                    id="e3",
                    document_id="doc-2",
                    name="Heap",
                    entity_type="data_structure",
                    description="Binary heap",
                )
            ]
        )

        all_entities = self.backend.list_all_entities()
        assert len(all_entities) == 3

    def test_list_entities_filter_by_type(self):
        self.backend.save_entities(_make_entities())

        data_structures = self.backend.list_all_entities(entity_type="data_structure")
        assert len(data_structures) == 1
        assert data_structures[0].name == "BST"

        algorithms = self.backend.list_all_entities(entity_type="algorithm")
        assert len(algorithms) == 1
        assert algorithms[0].name == "Quicksort"

    def test_list_entities_search(self):
        self.backend.save_entities(_make_entities())

        results = self.backend.list_all_entities(search="Binary")
        assert len(results) >= 1
        assert any(entity.name == "BST" for entity in results)

    def test_list_entities_limit(self):
        self.backend.save_entities(_make_entities())

        results = self.backend.list_all_entities(limit=1)
        assert len(results) == 1

    def test_delete_entities(self):
        self.backend.save_entities(_make_entities())

        deleted = self.backend.delete_entities("doc-1")
        assert deleted == 2
        assert self.backend.get_entities("doc-1") == []

    def test_save_and_get_relationships(self):
        self.backend.save_entities(_make_entities())

        saved = self.backend.save_relationships(_make_relationships())
        assert saved == 1

        loaded = self.backend.get_relationships("doc-1")
        assert len(loaded) == 1
        assert loaded[0].relationship_type == "related_to"

    def test_delete_relationships(self):
        self.backend.save_entities(_make_entities())
        self.backend.save_relationships(_make_relationships())

        deleted = self.backend.delete_relationships("doc-1")
        assert deleted == 1
        assert self.backend.get_relationships("doc-1") == []

    @pytest.mark.skipif(not PGVECTOR_AVAILABLE, reason="pgvector extension not installed")
    def test_search_similar_vector(self, monkeypatch: pytest.MonkeyPatch):
        assert self.backend._has_vector is True

        vector_map = {
            "BST Binary search tree": [1.0, 0.0, 0.0],
            "AVL Tree Self-balancing binary search tree": [0.96, 0.04, 0.0],
            "Quicksort Divide and conquer sort": [0.0, 1.0, 0.0],
            "Binary search tree": [1.0, 0.0, 0.0],
        }

        def fake_vector(text: str, dim: int = 384) -> list[float]:
            base = vector_map[text]
            return base + [0.0] * (dim - len(base))

        monkeypatch.setattr(self.backend, "_text_to_vector", fake_vector)
        self.backend.save_entities(
            [
                Entity(
                    id="e1",
                    document_id="doc-1",
                    name="BST",
                    entity_type="data_structure",
                    description="Binary search tree",
                ),
                Entity(
                    id="e2",
                    document_id="doc-1",
                    name="AVL Tree",
                    entity_type="data_structure",
                    description="Self-balancing binary search tree",
                ),
                Entity(
                    id="e3",
                    document_id="doc-1",
                    name="Quicksort",
                    entity_type="algorithm",
                    description="Divide and conquer sort",
                ),
            ]
        )

        results = self.backend.search_similar("Binary search tree", limit=3)

        assert [entity.name for entity in results] == ["BST", "AVL Tree", "Quicksort"]

    @pytest.mark.skipif(not PGVECTOR_AVAILABLE, reason="pgvector extension not installed")
    def test_search_similar_with_type_filter(self, monkeypatch: pytest.MonkeyPatch):
        assert self.backend._has_vector is True

        vector_map = {
            "BST Binary search tree": [1.0, 0.0, 0.0],
            "AVL Tree Self-balancing binary search tree": [0.96, 0.04, 0.0],
            "Merge sort Divide and conquer sort": [0.99, 0.01, 0.0],
            "Binary search tree": [1.0, 0.0, 0.0],
        }

        def fake_vector(text: str, dim: int = 384) -> list[float]:
            base = vector_map[text]
            return base + [0.0] * (dim - len(base))

        monkeypatch.setattr(self.backend, "_text_to_vector", fake_vector)
        self.backend.save_entities(
            [
                Entity(
                    id="e1",
                    document_id="doc-1",
                    name="BST",
                    entity_type="data_structure",
                    description="Binary search tree",
                ),
                Entity(
                    id="e2",
                    document_id="doc-1",
                    name="AVL Tree",
                    entity_type="data_structure",
                    description="Self-balancing binary search tree",
                ),
                Entity(
                    id="e3",
                    document_id="doc-1",
                    name="Merge sort",
                    entity_type="algorithm",
                    description="Divide and conquer sort",
                ),
            ]
        )

        results = self.backend.search_similar(
            "Binary search tree",
            limit=5,
            entity_type="data_structure",
        )

        assert [entity.name for entity in results] == ["BST", "AVL Tree"]

    def test_context_manager(self):
        with PostgresBackend(POSTGRES_URL) as backend:
            assert backend.name == "postgres"
            assert backend.is_available() is True
            conn = backend._conn

        assert conn is not None
        assert conn.closed

    @pytest.mark.skipif(not PGVECTOR_AVAILABLE, reason="pgvector extension not installed")
    def test_pgvector_extension_available(self):
        assert self.backend._has_vector is True
