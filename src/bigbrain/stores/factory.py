"""Entity store backend factory — creates the configured backend."""

from __future__ import annotations

from bigbrain.config import StoreConfig
from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger
from bigbrain.stores.base import EntityStoreBackend

logger = get_logger(__name__)


def create_entity_store(config: StoreConfig, kb_store: KBStore | None = None) -> EntityStoreBackend:
    """Create an entity store backend from config.

    Args:
        config: StoreConfig with backend name and connection details
        kb_store: Required for sqlite backend (wraps existing KBStore)
    """
    backend = config.backend.lower()

    if backend == "sqlite":
        from bigbrain.stores.sqlite_backend import SqliteBackend
        if kb_store is None:
            raise ValueError("SQLite backend requires a KBStore instance")
        return SqliteBackend(kb_store)

    elif backend == "postgres":
        from bigbrain.stores.postgres import PostgresBackend
        if not config.postgres_url:
            raise ValueError("postgres_url must be set for PostgreSQL backend")
        return PostgresBackend(config.postgres_url)

    elif backend == "neo4j":
        from bigbrain.stores.neo4j_backend import Neo4jBackend
        if not config.neo4j_url:
            raise ValueError("neo4j_url must be set for Neo4j backend")
        return Neo4jBackend(config.neo4j_url, config.neo4j_user, config.neo4j_password)

    elif backend == "qdrant":
        from bigbrain.stores.qdrant_backend import QdrantBackend
        if not config.qdrant_url:
            raise ValueError("qdrant_url must be set for Qdrant backend")
        return QdrantBackend(config.qdrant_url, config.qdrant_collection)

    elif backend == "weaviate":
        from bigbrain.stores.weaviate_backend import WeaviateBackend
        if not config.weaviate_url:
            raise ValueError("weaviate_url must be set for Weaviate backend")
        return WeaviateBackend(config.weaviate_url)

    elif backend == "pinecone":
        from bigbrain.stores.pinecone_backend import PineconeBackend
        if not config.pinecone_api_key:
            raise ValueError("pinecone_api_key must be set for Pinecone backend")
        return PineconeBackend(config.pinecone_api_key, config.pinecone_index, config.pinecone_environment)

    else:
        logger.warning("Unknown backend '%s', falling back to sqlite", backend)
        from bigbrain.stores.sqlite_backend import SqliteBackend
        if kb_store is None:
            raise ValueError("SQLite fallback requires a KBStore instance")
        return SqliteBackend(kb_store)
