"""Weaviate vector backend for entity storage and search."""
from __future__ import annotations

import json

from bigbrain.distill.models import Entity, Relationship
from bigbrain.stores.base import EntityStoreBackend
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


class WeaviateBackend(EntityStoreBackend):
    def __init__(self, url: str) -> None:
        self._url = url
        self._client = None
        self._class_name = "BigBrainEntity"

    def _get_client(self):
        if self._client is None:
            import weaviate

            host = self._url.replace("http://", "").split(":")[0]
            tail = self._url.split("/")[-1]
            port = int(tail.split(":")[-1]) if ":" in tail else 8080
            self._client = weaviate.connect_to_local(host=host, port=port)
            self._ensure_schema()
        return self._client

    def _ensure_schema(self):
        try:
            collections = self._client.collections.list_all()
            names = (
                [c.name for c in collections.values()]
                if hasattr(collections, "values")
                else []
            )
            if self._class_name not in names:
                self._client.collections.create(
                    name=self._class_name,
                    properties=[
                        {"name": "entity_id", "data_type": ["text"]},
                        {"name": "document_id", "data_type": ["text"]},
                        {"name": "name", "data_type": ["text"]},
                        {"name": "entity_type", "data_type": ["text"]},
                        {"name": "description", "data_type": ["text"]},
                    ],
                )
        except Exception as exc:
            logger.debug("Weaviate schema check: %s", exc)

    @property
    def name(self) -> str:
        return "weaviate"

    def is_available(self) -> bool:
        try:
            client = self._get_client()
            return client.is_ready()
        except Exception:
            return False

    def save_entities(self, entities: list[Entity]) -> int:
        client = self._get_client()
        collection = client.collections.get(self._class_name)
        for e in entities:
            collection.data.insert(
                properties={
                    "entity_id": e.id,
                    "document_id": e.document_id,
                    "name": e.name,
                    "entity_type": e.entity_type,
                    "description": e.description,
                }
            )
        return len(entities)

    def get_entities(self, document_id: str) -> list[Entity]:
        client = self._get_client()
        collection = client.collections.get(self._class_name)
        result = collection.query.fetch_objects(
            filters=weaviate_filter("document_id", document_id),
            limit=1000,
        )
        return [self._obj_to_entity(o) for o in result.objects]

    def list_all_entities(
        self, *, entity_type: str = "", search: str = "", limit: int = 500
    ) -> list[Entity]:
        client = self._get_client()
        collection = client.collections.get(self._class_name)
        if search:
            result = collection.query.bm25(query=search, limit=limit)
        else:
            result = collection.query.fetch_objects(limit=limit)
        return [self._obj_to_entity(o) for o in result.objects]

    def delete_entities(self, document_id: str) -> int:
        entities = self.get_entities(document_id)
        client = self._get_client()
        collection = client.collections.get(self._class_name)
        for e_obj in entities:
            try:
                collection.data.delete_by_id(e_obj.id)
            except Exception:
                pass
        return len(entities)

    def save_relationships(self, relationships: list[Relationship]) -> int:
        logger.warning(
            "Weaviate does not natively support typed relationships; "
            "use Neo4j for graph data"
        )
        return 0

    def get_relationships(self, document_id: str) -> list[Relationship]:
        return []

    def delete_relationships(self, document_id: str) -> int:
        return 0

    def close(self) -> None:
        if self._client:
            try:
                self._client.close()
            except Exception:
                pass

    @staticmethod
    def _obj_to_entity(obj) -> Entity:
        p = obj.properties
        return Entity(
            id=p.get("entity_id", ""),
            document_id=p.get("document_id", ""),
            name=p.get("name", ""),
            entity_type=p.get("entity_type", ""),
            description=p.get("description", ""),
        )


def weaviate_filter(key, value):
    """Build a Weaviate filter."""
    try:
        from weaviate.classes.query import Filter

        return Filter.by_property(key).equal(value)
    except ImportError:
        return None
