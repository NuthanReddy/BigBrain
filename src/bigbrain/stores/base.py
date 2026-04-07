"""Entity store backend ABC — interface for all storage backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from bigbrain.distill.models import Entity, Relationship


class EntityStoreBackend(ABC):
    """Abstract base for entity/relationship storage backends.

    All backends must implement these methods. The system routes
    operations to the configured backend at runtime.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Backend name (e.g., 'sqlite', 'postgres', 'neo4j')."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the backend is reachable and ready."""
        ...

    @abstractmethod
    def save_entities(self, entities: list[Entity]) -> int:
        """Save entities. Returns count saved."""
        ...

    @abstractmethod
    def get_entities(self, document_id: str) -> list[Entity]:
        """Get all entities for a document."""
        ...

    @abstractmethod
    def list_all_entities(
        self,
        *,
        entity_type: str = "",
        search: str = "",
        limit: int = 500,
    ) -> list[Entity]:
        """List entities with optional filters."""
        ...

    @abstractmethod
    def delete_entities(self, document_id: str) -> int:
        """Delete all entities for a document. Returns count deleted."""
        ...

    @abstractmethod
    def save_relationships(self, relationships: list[Relationship]) -> int:
        """Save relationships. Returns count saved."""
        ...

    @abstractmethod
    def get_relationships(self, document_id: str) -> list[Relationship]:
        """Get all relationships for a document."""
        ...

    @abstractmethod
    def delete_relationships(self, document_id: str) -> int:
        """Delete all relationships for a document. Returns count deleted."""
        ...

    def search_similar(
        self, query: str, *, limit: int = 10, entity_type: str = ""
    ) -> list[Entity]:
        """Vector similarity search (optional, not all backends support this).

        Default implementation falls back to text search.
        Backends with vector support (pgvector, Qdrant, etc.) override this.
        """
        return self.list_all_entities(
            search=query, entity_type=entity_type, limit=limit
        )

    def close(self) -> None:
        """Close backend connection."""
        pass

    def __enter__(self) -> EntityStoreBackend:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
