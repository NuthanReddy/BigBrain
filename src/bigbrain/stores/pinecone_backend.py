"""Pinecone managed vector backend for entity similarity search."""
from __future__ import annotations

import hashlib
import json

from bigbrain.distill.models import Entity, Relationship
from bigbrain.stores.base import EntityStoreBackend
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


class PineconeBackend(EntityStoreBackend):
    def __init__(
        self,
        api_key: str,
        index_name: str = "bigbrain-entities",
        environment: str = "",
    ) -> None:
        self._api_key = api_key
        self._index_name = index_name
        self._environment = environment
        self._index = None

    def _get_index(self):
        if self._index is None:
            from pinecone import Pinecone

            pc = Pinecone(api_key=self._api_key)
            existing = [idx.name for idx in pc.list_indexes()]
            if self._index_name not in existing:
                from pinecone import ServerlessSpec

                pc.create_index(
                    name=self._index_name,
                    dimension=384,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                )
            self._index = pc.Index(self._index_name)
        return self._index

    @property
    def name(self) -> str:
        return "pinecone"

    def is_available(self) -> bool:
        try:
            idx = self._get_index()
            idx.describe_index_stats()
            return True
        except Exception:
            return False

    def save_entities(self, entities: list[Entity]) -> int:
        idx = self._get_index()
        vectors = []
        for e in entities:
            vector = self._text_to_vector(f"{e.name} {e.description}")
            vectors.append(
                {
                    "id": e.id,
                    "values": vector,
                    "metadata": {
                        "document_id": e.document_id,
                        "name": e.name,
                        "entity_type": e.entity_type,
                        "description": e.description,
                        "source_chunk_id": e.source_chunk_id,
                    },
                }
            )
        if vectors:
            for i in range(0, len(vectors), 100):
                idx.upsert(vectors=vectors[i : i + 100])
        return len(vectors)

    def get_entities(self, document_id: str) -> list[Entity]:
        idx = self._get_index()
        dummy_vector = [0.0] * 384
        results = idx.query(
            vector=dummy_vector,
            top_k=1000,
            filter={"document_id": {"$eq": document_id}},
            include_metadata=True,
        )
        return [self._match_to_entity(m) for m in results.get("matches", [])]

    def list_all_entities(
        self, *, entity_type: str = "", search: str = "", limit: int = 500
    ) -> list[Entity]:
        if search:
            return self.search_similar(search, limit=limit, entity_type=entity_type)
        idx = self._get_index()
        dummy_vector = [0.0] * 384
        filters: dict = {}
        if entity_type:
            filters["entity_type"] = {"$eq": entity_type}
        results = idx.query(
            vector=dummy_vector,
            top_k=limit,
            filter=filters if filters else None,
            include_metadata=True,
        )
        return [self._match_to_entity(m) for m in results.get("matches", [])]

    def delete_entities(self, document_id: str) -> int:
        idx = self._get_index()
        entities = self.get_entities(document_id)
        if entities:
            idx.delete(ids=[e.id for e in entities])
        return len(entities)

    def search_similar(
        self, query: str, *, limit: int = 10, entity_type: str = ""
    ) -> list[Entity]:
        idx = self._get_index()
        vector = self._text_to_vector(query)
        filters: dict = {}
        if entity_type:
            filters["entity_type"] = {"$eq": entity_type}
        results = idx.query(
            vector=vector,
            top_k=limit,
            filter=filters if filters else None,
            include_metadata=True,
        )
        return [self._match_to_entity(m) for m in results.get("matches", [])]

    def save_relationships(self, relationships: list[Relationship]) -> int:
        logger.warning(
            "Pinecone does not support relationships; use Neo4j or SQLite"
        )
        return 0

    def get_relationships(self, document_id: str) -> list[Relationship]:
        return []

    def delete_relationships(self, document_id: str) -> int:
        return 0

    def close(self) -> None:
        pass

    @staticmethod
    def _text_to_vector(text: str, dim: int = 384) -> list[float]:
        h = hashlib.sha512(text.encode()).digest()
        raw = [b / 255.0 for b in h]
        while len(raw) < dim:
            raw.extend(raw)
        return raw[:dim]

    @staticmethod
    def _match_to_entity(match) -> Entity:
        m = (
            match.get("metadata", {})
            if isinstance(match, dict)
            else match.metadata
        )
        mid = match.get("id", "") if isinstance(match, dict) else match.id
        return Entity(
            id=mid,
            document_id=m.get("document_id", ""),
            name=m.get("name", ""),
            entity_type=m.get("entity_type", ""),
            description=m.get("description", ""),
            source_chunk_id=m.get("source_chunk_id", ""),
        )
