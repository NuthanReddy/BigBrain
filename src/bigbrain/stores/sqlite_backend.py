"""SQLite backend — wraps existing KBStore as an EntityStoreBackend."""

from __future__ import annotations

from bigbrain.distill.models import Entity, Relationship
from bigbrain.kb.store import KBStore
from bigbrain.stores.base import EntityStoreBackend


class SqliteBackend(EntityStoreBackend):
    """Default SQLite backend using the existing KBStore."""

    def __init__(self, store: KBStore) -> None:
        self._store = store

    @property
    def name(self) -> str:
        return "sqlite"

    def is_available(self) -> bool:
        return True  # SQLite is always available

    def save_entities(self, entities: list[Entity]) -> int:
        return self._store.save_entities(entities)

    def get_entities(self, document_id: str) -> list[Entity]:
        return self._store.get_entities(document_id)

    def list_all_entities(
        self, *, entity_type: str = "", search: str = "", limit: int = 500
    ) -> list[Entity]:
        return self._store.list_all_entities(
            entity_type=entity_type, search=search, limit=limit
        )

    def delete_entities(self, document_id: str) -> int:
        entities = self._store.get_entities(document_id)
        if entities:
            with self._store._lock:
                with self._store._conn:
                    cur = self._store._conn.execute(
                        "DELETE FROM entities WHERE document_id = ?", (document_id,)
                    )
                return cur.rowcount
        return 0

    def save_relationships(self, relationships: list[Relationship]) -> int:
        return self._store.save_relationships(relationships)

    def get_relationships(self, document_id: str) -> list[Relationship]:
        return self._store.get_relationships(document_id)

    def delete_relationships(self, document_id: str) -> int:
        with self._store._lock:
            with self._store._conn:
                cur = self._store._conn.execute(
                    "DELETE FROM relationships WHERE document_id = ?", (document_id,)
                )
            return cur.rowcount

    def close(self) -> None:
        pass  # Don't close the KBStore — it's managed externally
