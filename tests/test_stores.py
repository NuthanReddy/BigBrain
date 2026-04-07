"""Tests for bigbrain.stores — Phase 11 polyglot entity store backends."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from bigbrain.distill.models import Entity, Relationship
from bigbrain.kb.models import Document, DocumentSection, SourceMetadata
from bigbrain.stores.base import EntityStoreBackend


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------

def _make_document(file_path: str = "test/sample.txt") -> Document:
    """Create a minimal Document to satisfy FK constraints in KBStore."""
    return Document(
        title="Test Doc",
        content="Sample content for entity tests",
        source=SourceMetadata(
            file_path=file_path,
            file_extension=".txt",
            source_type="txt",
            size_bytes=31,
        ),
        language="",
        sections=[DocumentSection(title="S1", content="Section one", level=1)],
    )


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
        ),
    ]


# ===========================================================================
# ABC tests
# ===========================================================================

class TestEntityStoreBackendABC:
    """Verify the ABC contract for EntityStoreBackend."""

    def test_cannot_instantiate(self):
        with pytest.raises(TypeError):
            EntityStoreBackend()

    def test_interface_methods(self):
        expected = {
            "name",
            "is_available",
            "save_entities",
            "get_entities",
            "list_all_entities",
            "delete_entities",
            "save_relationships",
            "get_relationships",
            "delete_relationships",
        }
        # All abstract methods must be present on the ABC
        abstract_names = set()
        for attr_name in dir(EntityStoreBackend):
            obj = getattr(EntityStoreBackend, attr_name, None)
            if getattr(obj, "__isabstractmethod__", False):
                abstract_names.add(attr_name)
        assert expected == abstract_names

    def test_search_similar_has_default_implementation(self):
        """search_similar should not be abstract — it has a default fallback."""
        obj = getattr(EntityStoreBackend, "search_similar", None)
        assert obj is not None
        assert not getattr(obj, "__isabstractmethod__", False)

    def test_context_manager_protocol(self):
        """EntityStoreBackend supports ``with`` blocks."""
        assert hasattr(EntityStoreBackend, "__enter__")
        assert hasattr(EntityStoreBackend, "__exit__")


# ===========================================================================
# SQLite backend — real integration tests
# ===========================================================================

class TestSqliteBackend:
    """Integration tests using a real SQLite database via KBStore."""

    @pytest.fixture(autouse=True)
    def setup_backend(self, tmp_path):
        from bigbrain.kb.store import KBStore
        from bigbrain.stores.sqlite_backend import SqliteBackend

        db_path = tmp_path / "test.db"
        self.store = KBStore(str(db_path))
        self.backend = SqliteBackend(self.store)

        # Save a document to satisfy FK constraints on entities table
        doc1 = _make_document("test/sample1.txt")
        self.doc1_id = self.store.save_document(doc1)

        doc2 = _make_document("test/sample2.txt")
        self.doc2_id = self.store.save_document(doc2)

        yield
        self.store.close()

    def test_name_is_sqlite(self):
        assert self.backend.name == "sqlite"

    def test_is_available(self):
        assert self.backend.is_available() is True

    def test_save_and_get_entities(self):
        entities = _make_entities(self.doc1_id)
        saved = self.backend.save_entities(entities)
        assert saved == 2

        loaded = self.backend.get_entities(self.doc1_id)
        assert len(loaded) == 2
        names = {e.name for e in loaded}
        assert names == {"BST", "Quicksort"}

    def test_save_entities_upsert(self):
        """Saving the same entity twice should upsert, not duplicate."""
        entities = _make_entities(self.doc1_id)
        self.backend.save_entities(entities)
        entities[0].description = "Updated BST"
        self.backend.save_entities(entities)

        loaded = self.backend.get_entities(self.doc1_id)
        assert len(loaded) == 2

    def test_get_entities_empty(self):
        result = self.backend.get_entities("nonexistent")
        assert result == []

    def test_list_all_entities(self):
        self.backend.save_entities(_make_entities(self.doc1_id))
        self.backend.save_entities(
            [Entity(id="e3", document_id=self.doc2_id, name="Heap", entity_type="data_structure")]
        )
        all_entities = self.backend.list_all_entities()
        assert len(all_entities) == 3

    def test_list_entities_filter_by_type(self):
        self.backend.save_entities(_make_entities(self.doc1_id))
        ds = self.backend.list_all_entities(entity_type="data_structure")
        assert len(ds) == 1
        assert ds[0].name == "BST"

        algos = self.backend.list_all_entities(entity_type="algorithm")
        assert len(algos) == 1
        assert algos[0].name == "Quicksort"

    def test_list_entities_search(self):
        self.backend.save_entities(_make_entities(self.doc1_id))
        results = self.backend.list_all_entities(search="Binary")
        assert len(results) >= 1
        assert any(e.name == "BST" for e in results)

    def test_list_entities_limit(self):
        self.backend.save_entities(_make_entities(self.doc1_id))
        results = self.backend.list_all_entities(limit=1)
        assert len(results) == 1

    def test_delete_entities(self):
        self.backend.save_entities(_make_entities(self.doc1_id))
        deleted = self.backend.delete_entities(self.doc1_id)
        assert deleted == 2

        remaining = self.backend.get_entities(self.doc1_id)
        assert remaining == []

    def test_delete_entities_nonexistent(self):
        deleted = self.backend.delete_entities("nope")
        assert deleted == 0

    def test_save_and_get_relationships(self):
        self.backend.save_entities(_make_entities(self.doc1_id))
        rels = _make_relationships(self.doc1_id)
        saved = self.backend.save_relationships(rels)
        assert saved == 1

        loaded = self.backend.get_relationships(self.doc1_id)
        assert len(loaded) == 1
        assert loaded[0].relationship_type == "related_to"

    def test_get_relationships_empty(self):
        result = self.backend.get_relationships("nonexistent")
        assert result == []

    def test_delete_relationships(self):
        self.backend.save_entities(_make_entities(self.doc1_id))
        self.backend.save_relationships(_make_relationships(self.doc1_id))
        deleted = self.backend.delete_relationships(self.doc1_id)
        assert deleted == 1

        remaining = self.backend.get_relationships(self.doc1_id)
        assert remaining == []

    def test_delete_relationships_nonexistent(self):
        deleted = self.backend.delete_relationships("nope")
        assert deleted == 0

    def test_search_similar_falls_back_to_text(self):
        """SqliteBackend inherits default search_similar which calls list_all_entities."""
        self.backend.save_entities(_make_entities(self.doc1_id))
        results = self.backend.search_similar("Binary")
        assert len(results) >= 1
        assert any(e.name == "BST" for e in results)

    def test_context_manager(self):
        """Backend can be used as a context manager."""
        from bigbrain.stores.sqlite_backend import SqliteBackend
        from bigbrain.kb.store import KBStore

        store = KBStore(":memory:")
        with SqliteBackend(store) as backend:
            assert backend.name == "sqlite"
        store.close()


# ===========================================================================
# Postgres backend — mocked
# ===========================================================================

class TestPostgresBackend:
    """Verify PostgresBackend SQL calls via mocked psycopg."""

    def test_name(self):
        from bigbrain.stores.postgres import PostgresBackend

        backend = PostgresBackend("postgresql://localhost/test")
        assert backend.name == "postgres"

    def test_schema_creation_called(self):
        from bigbrain.stores.postgres import PostgresBackend

        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        backend = PostgresBackend("postgresql://localhost/test")
        backend._conn = mock_conn
        backend._ensure_schema()

        sql_calls = [str(c) for c in mock_cursor.execute.call_args_list]
        create_calls = [s for s in sql_calls if "CREATE TABLE" in s]
        assert len(create_calls) >= 2, "Should create bb_entities and bb_relationships tables"

    def test_save_entities_executes_upsert(self):
        from bigbrain.stores.postgres import PostgresBackend

        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        backend = PostgresBackend("postgresql://localhost/test")
        backend._conn = mock_conn

        entities = _make_entities("doc-1")
        count = backend.save_entities(entities)
        assert count == 2
        assert mock_cursor.execute.call_count == 2

        first_sql = mock_cursor.execute.call_args_list[0][0][0]
        assert "INSERT INTO bb_entities" in first_sql
        assert "ON CONFLICT" in first_sql

    def test_save_relationships_executes_upsert(self):
        from bigbrain.stores.postgres import PostgresBackend

        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        backend = PostgresBackend("postgresql://localhost/test")
        backend._conn = mock_conn

        rels = _make_relationships("doc-1")
        count = backend.save_relationships(rels)
        assert count == 1

        first_sql = mock_cursor.execute.call_args_list[0][0][0]
        assert "INSERT INTO bb_relationships" in first_sql
        assert "ON CONFLICT" in first_sql

    def test_delete_entities(self):
        from bigbrain.stores.postgres import PostgresBackend

        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 3
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

        backend = PostgresBackend("postgresql://localhost/test")
        backend._conn = mock_conn

        deleted = backend.delete_entities("doc-1")
        assert deleted == 3

        sql = mock_cursor.execute.call_args_list[0][0][0]
        assert "DELETE FROM bb_entities" in sql


# ===========================================================================
# Neo4j backend — mocked
# ===========================================================================

class TestNeo4jBackend:
    """Verify Neo4jBackend Cypher queries via mocked neo4j driver."""

    def test_name(self):
        from bigbrain.stores.neo4j_backend import Neo4jBackend

        backend = Neo4jBackend("bolt://localhost:7687")
        assert backend.name == "neo4j"

    def test_save_entities_runs_merge(self):
        from bigbrain.stores.neo4j_backend import Neo4jBackend

        mock_driver = MagicMock()
        mock_session = MagicMock()
        mock_driver.session.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_driver.session.return_value.__exit__ = MagicMock(return_value=False)

        backend = Neo4jBackend("bolt://localhost:7687")
        backend._driver = mock_driver

        entities = _make_entities("doc-1")
        count = backend.save_entities(entities)
        assert count == 2
        assert mock_session.run.call_count == 2

        first_cypher = mock_session.run.call_args_list[0][0][0]
        assert "MERGE" in first_cypher
        assert "Entity" in first_cypher

    def test_save_relationships_runs_merge(self):
        from bigbrain.stores.neo4j_backend import Neo4jBackend

        mock_driver = MagicMock()
        mock_session = MagicMock()
        mock_driver.session.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_driver.session.return_value.__exit__ = MagicMock(return_value=False)

        backend = Neo4jBackend("bolt://localhost:7687")
        backend._driver = mock_driver

        rels = _make_relationships("doc-1")
        count = backend.save_relationships(rels)
        assert count == 1

        cypher = mock_session.run.call_args_list[0][0][0]
        assert "MERGE" in cypher
        assert "RELATED" in cypher

    def test_delete_entities_runs_detach_delete(self):
        from bigbrain.stores.neo4j_backend import Neo4jBackend

        mock_driver = MagicMock()
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_result.single.return_value = {"cnt": 5}
        mock_session.run.return_value = mock_result
        mock_driver.session.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_driver.session.return_value.__exit__ = MagicMock(return_value=False)

        backend = Neo4jBackend("bolt://localhost:7687")
        backend._driver = mock_driver

        deleted = backend.delete_entities("doc-1")
        assert deleted == 5

        cypher = mock_session.run.call_args_list[0][0][0]
        assert "DETACH DELETE" in cypher


# ===========================================================================
# Qdrant backend — mocked
# ===========================================================================

class TestQdrantBackend:
    """Verify QdrantBackend calls via mocked qdrant_client."""

    def test_name(self):
        from bigbrain.stores.qdrant_backend import QdrantBackend

        backend = QdrantBackend("http://localhost:6333")
        assert backend.name == "qdrant"

    def test_save_entities_calls_upsert(self):
        from bigbrain.stores.qdrant_backend import QdrantBackend

        mock_client = MagicMock()

        backend = QdrantBackend("http://localhost:6333")
        backend._client = mock_client

        entities = _make_entities("doc-1")
        count = backend.save_entities(entities)
        assert count == 2
        mock_client.upsert.assert_called_once()

    def test_search_similar_uses_vector(self):
        from bigbrain.stores.qdrant_backend import QdrantBackend

        mock_client = MagicMock()
        mock_client.search.return_value = []

        backend = QdrantBackend("http://localhost:6333")
        backend._client = mock_client

        results = backend.search_similar("binary tree")
        assert results == []
        mock_client.search.assert_called_once()

        search_kwargs = mock_client.search.call_args.kwargs
        assert "query_vector" in search_kwargs

    def test_text_to_vector_correct_dimension(self):
        from bigbrain.stores.qdrant_backend import QdrantBackend

        vec = QdrantBackend._text_to_vector("hello world")
        assert len(vec) == 384
        assert all(isinstance(v, float) for v in vec)

    def test_relationships_not_supported(self):
        from bigbrain.stores.qdrant_backend import QdrantBackend

        backend = QdrantBackend("http://localhost:6333")
        assert backend.save_relationships(_make_relationships()) == 0
        assert backend.get_relationships("doc-1") == []
        assert backend.delete_relationships("doc-1") == 0


# ===========================================================================
# Weaviate backend — mocked
# ===========================================================================

class TestWeaviateBackend:
    """Verify WeaviateBackend behaviour."""

    def test_name(self):
        from bigbrain.stores.weaviate_backend import WeaviateBackend

        backend = WeaviateBackend("http://localhost:8080")
        assert backend.name == "weaviate"

    def test_relationships_not_supported(self):
        from bigbrain.stores.weaviate_backend import WeaviateBackend

        backend = WeaviateBackend("http://localhost:8080")
        assert backend.save_relationships(_make_relationships()) == 0
        assert backend.get_relationships("doc-1") == []
        assert backend.delete_relationships("doc-1") == 0


# ===========================================================================
# Pinecone backend — mocked
# ===========================================================================

class TestPineconeBackend:
    """Verify PineconeBackend behaviour."""

    def test_name(self):
        from bigbrain.stores.pinecone_backend import PineconeBackend

        backend = PineconeBackend(api_key="test-key")
        assert backend.name == "pinecone"

    def test_relationships_not_supported(self):
        from bigbrain.stores.pinecone_backend import PineconeBackend

        backend = PineconeBackend(api_key="test-key")
        assert backend.save_relationships(_make_relationships()) == 0
        assert backend.get_relationships("doc-1") == []
        assert backend.delete_relationships("doc-1") == 0

    def test_text_to_vector_correct_dimension(self):
        from bigbrain.stores.pinecone_backend import PineconeBackend

        vec = PineconeBackend._text_to_vector("hello world")
        assert len(vec) == 384
        assert all(isinstance(v, float) for v in vec)

    def test_text_to_vector_deterministic(self):
        from bigbrain.stores.pinecone_backend import PineconeBackend

        v1 = PineconeBackend._text_to_vector("same text")
        v2 = PineconeBackend._text_to_vector("same text")
        assert v1 == v2

    def test_text_to_vector_different_inputs(self):
        from bigbrain.stores.pinecone_backend import PineconeBackend

        v1 = PineconeBackend._text_to_vector("hello")
        v2 = PineconeBackend._text_to_vector("world")
        assert v1 != v2


# ===========================================================================
# StoreConfig tests
# ===========================================================================

class TestStoreConfig:
    """Verify StoreConfig defaults and integration with BigBrainConfig."""

    def test_default_values(self):
        from bigbrain.config import StoreConfig

        cfg = StoreConfig()
        assert cfg.backend == "sqlite"
        assert cfg.postgres_url == ""
        assert cfg.neo4j_url == ""
        assert cfg.neo4j_user == "neo4j"
        assert cfg.neo4j_password == ""
        assert cfg.qdrant_url == ""
        assert cfg.qdrant_collection == "bigbrain_entities"
        assert cfg.weaviate_url == ""
        assert cfg.pinecone_api_key == ""
        assert cfg.pinecone_index == "bigbrain-entities"
        assert cfg.pinecone_environment == ""

    def test_config_in_bigbrain_config(self):
        from bigbrain.config import BigBrainConfig, StoreConfig

        config = BigBrainConfig()
        assert isinstance(config.entity_store, StoreConfig)
        assert config.entity_store.backend == "sqlite"

    def test_env_var_override(self, monkeypatch, tmp_path):
        from bigbrain.config import load_config

        monkeypatch.setenv("BIGBRAIN_STORE_BACKEND", "postgres")
        monkeypatch.setenv("BIGBRAIN_STORE_POSTGRES_URL", "postgresql://localhost/bb")

        # Write a minimal config file
        cfg_file = tmp_path / "test.yaml"
        cfg_file.write_text("app:\n  log_level: INFO\n")

        config = load_config(str(cfg_file))
        assert config.entity_store.backend == "postgres"
        assert config.entity_store.postgres_url == "postgresql://localhost/bb"
