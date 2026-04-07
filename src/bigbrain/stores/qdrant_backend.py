"""Qdrant vector backend for entity similarity search."""

from __future__ import annotations

import hashlib
import json

from bigbrain.distill.models import Entity, Relationship
from bigbrain.logging_config import get_logger
from bigbrain.stores.base import EntityStoreBackend

logger = get_logger(__name__)


class QdrantBackend(EntityStoreBackend):
    """Vector similarity search for entities via Qdrant."""

    def __init__(
        self, url: str, collection: str = "bigbrain_entities"
    ) -> None:
        self._url = url
        self._collection = collection
        self._client = None

    def _get_client(self):
        if self._client is None:
            from qdrant_client import QdrantClient

            self._client = QdrantClient(url=self._url)
            self._ensure_collection()
        return self._client

    def _ensure_collection(self):
        from qdrant_client.models import Distance, VectorParams

        try:
            self._client.get_collection(self._collection)
        except Exception:
            self._client.create_collection(
                collection_name=self._collection,
                vectors_config=VectorParams(
                    size=384, distance=Distance.COSINE
                ),
            )

    @property
    def name(self) -> str:
        return "qdrant"

    def is_available(self) -> bool:
        try:
            client = self._get_client()
            client.get_collections()
            return True
        except Exception:
            return False

    def save_entities(self, entities: list[Entity]) -> int:
        from qdrant_client.models import PointStruct

        client = self._get_client()
        points = []
        for e in entities:
            # Placeholder vector — real implementation would use embeddings
            vector = self._text_to_vector(f"{e.name} {e.description}")
            points.append(
                PointStruct(
                    id=e.id,
                    vector=vector,
                    payload={
                        "document_id": e.document_id,
                        "name": e.name,
                        "entity_type": e.entity_type,
                        "description": e.description,
                        "source_chunk_id": e.source_chunk_id,
                        "generated_by_provider": e.generated_by_provider,
                        "generated_by_model": e.generated_by_model,
                        "metadata": json.dumps(e.metadata, default=str),
                    },
                )
            )
        if points:
            client.upsert(collection_name=self._collection, points=points)
        return len(points)

    def get_entities(self, document_id: str) -> list[Entity]:
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        client = self._get_client()
        results = client.scroll(
            collection_name=self._collection,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            ),
            limit=1000,
        )[0]
        return [self._point_to_entity(p) for p in results]

    def list_all_entities(
        self,
        *,
        entity_type: str = "",
        search: str = "",
        limit: int = 500,
    ) -> list[Entity]:
        client = self._get_client()
        if search:
            return self.search_similar(
                search, limit=limit, entity_type=entity_type
            )
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        conditions = []
        if entity_type:
            conditions.append(
                FieldCondition(
                    key="entity_type",
                    match=MatchValue(value=entity_type),
                )
            )
        filt = Filter(must=conditions) if conditions else None
        results = client.scroll(
            collection_name=self._collection,
            scroll_filter=filt,
            limit=limit,
        )[0]
        return [self._point_to_entity(p) for p in results]

    def delete_entities(self, document_id: str) -> int:
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        client = self._get_client()
        entities = self.get_entities(document_id)
        if entities:
            client.delete(
                collection_name=self._collection,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="document_id",
                            match=MatchValue(value=document_id),
                        )
                    ]
                ),
            )
        return len(entities)

    def search_similar(
        self, query: str, *, limit: int = 10, entity_type: str = ""
    ) -> list[Entity]:
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        client = self._get_client()
        vector = self._text_to_vector(query)
        conditions = []
        if entity_type:
            conditions.append(
                FieldCondition(
                    key="entity_type",
                    match=MatchValue(value=entity_type),
                )
            )
        filt = Filter(must=conditions) if conditions else None
        results = client.search(
            collection_name=self._collection,
            query_vector=vector,
            limit=limit,
            query_filter=filt,
        )
        return [self._hit_to_entity(h) for h in results]

    def save_relationships(self, relationships: list[Relationship]) -> int:
        logger.warning(
            "Qdrant does not natively support relationships; "
            "use Neo4j or SQLite for graph data"
        )
        return 0

    def get_relationships(self, document_id: str) -> list[Relationship]:
        return []

    def delete_relationships(self, document_id: str) -> int:
        return 0

    def close(self) -> None:
        if self._client:
            self._client.close()

    @staticmethod
    def _text_to_vector(text: str, dim: int = 384) -> list[float]:
        """Simple hash-based vector (placeholder — real impl uses sentence-transformers)."""
        h = hashlib.sha512(text.encode()).digest()
        raw = [b / 255.0 for b in h]
        while len(raw) < dim:
            raw.extend(raw)
        return raw[:dim]

    @staticmethod
    def _point_to_entity(point) -> Entity:
        p = point.payload
        return Entity(
            id=point.id,
            document_id=p.get("document_id", ""),
            name=p.get("name", ""),
            entity_type=p.get("entity_type", ""),
            description=p.get("description", ""),
            source_chunk_id=p.get("source_chunk_id", ""),
            generated_by_provider=p.get("generated_by_provider", ""),
            generated_by_model=p.get("generated_by_model", ""),
            metadata=json.loads(p.get("metadata", "{}"))
            if p.get("metadata")
            else {},
        )

    @staticmethod
    def _hit_to_entity(hit) -> Entity:
        p = hit.payload
        return Entity(
            id=hit.id,
            document_id=p.get("document_id", ""),
            name=p.get("name", ""),
            entity_type=p.get("entity_type", ""),
            description=p.get("description", ""),
        )
