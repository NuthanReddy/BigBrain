"""Neo4j graph backend for entity and relationship storage."""

from __future__ import annotations

import json

from bigbrain.distill.models import Entity, Relationship
from bigbrain.logging_config import get_logger
from bigbrain.stores.base import EntityStoreBackend

logger = get_logger(__name__)


class Neo4jBackend(EntityStoreBackend):
    """Stores entities as nodes and relationships as edges in Neo4j."""

    def __init__(
        self, url: str, user: str = "neo4j", password: str = ""
    ) -> None:
        self._url = url
        self._user = user
        self._password = password
        self._driver = None

    def _get_driver(self):
        if self._driver is None:
            from neo4j import GraphDatabase

            self._driver = GraphDatabase.driver(
                self._url, auth=(self._user, self._password)
            )
        return self._driver

    @property
    def name(self) -> str:
        return "neo4j"

    def is_available(self) -> bool:
        try:
            driver = self._get_driver()
            driver.verify_connectivity()
            return True
        except Exception:
            return False

    def save_entities(self, entities: list[Entity]) -> int:
        driver = self._get_driver()
        with driver.session() as session:
            for e in entities:
                session.run(
                    "MERGE (n:Entity {id: $id}) "
                    "SET n.document_id=$doc_id, n.name=$name, "
                    "n.entity_type=$etype, n.description=$desc, "
                    "n.source_chunk_id=$chunk, "
                    "n.generated_by_provider=$provider, "
                    "n.generated_by_model=$model, "
                    "n.metadata_json=$meta",
                    id=e.id,
                    doc_id=e.document_id,
                    name=e.name,
                    etype=e.entity_type,
                    desc=e.description,
                    chunk=e.source_chunk_id,
                    provider=e.generated_by_provider,
                    model=e.generated_by_model,
                    meta=json.dumps(e.metadata, default=str),
                )
        return len(entities)

    def get_entities(self, document_id: str) -> list[Entity]:
        driver = self._get_driver()
        with driver.session() as session:
            result = session.run(
                "MATCH (n:Entity {document_id: $doc_id}) "
                "RETURN n ORDER BY n.name",
                doc_id=document_id,
            )
            return [self._node_to_entity(record["n"]) for record in result]

    def list_all_entities(
        self,
        *,
        entity_type: str = "",
        search: str = "",
        limit: int = 500,
    ) -> list[Entity]:
        driver = self._get_driver()
        conditions: list[str] = []
        params: dict = {"limit": limit}
        if entity_type:
            conditions.append("n.entity_type = $etype")
            params["etype"] = entity_type
        if search:
            conditions.append(
                "(toLower(n.name) CONTAINS toLower($search) "
                "OR toLower(n.description) CONTAINS toLower($search))"
            )
            params["search"] = search
        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        query = (
            f"MATCH (n:Entity) {where} "
            "RETURN n ORDER BY n.entity_type, n.name LIMIT $limit"
        )
        with driver.session() as session:
            result = session.run(query, **params)
            return [self._node_to_entity(record["n"]) for record in result]

    def delete_entities(self, document_id: str) -> int:
        driver = self._get_driver()
        with driver.session() as session:
            result = session.run(
                "MATCH (n:Entity {document_id: $doc_id}) "
                "DETACH DELETE n RETURN count(n) as cnt",
                doc_id=document_id,
            )
            return result.single()["cnt"]

    def save_relationships(self, relationships: list[Relationship]) -> int:
        driver = self._get_driver()
        with driver.session() as session:
            for r in relationships:
                session.run(
                    "MATCH (a:Entity {id: $src}), (b:Entity {id: $tgt}) "
                    "MERGE (a)-[rel:RELATED {id: $id}]->(b) "
                    "SET rel.relationship_type=$rtype, rel.description=$desc, "
                    "rel.document_id=$doc_id, rel.confidence=$conf, "
                    "rel.generated_by_provider=$provider, "
                    "rel.generated_by_model=$model",
                    id=r.id,
                    src=r.source_entity_id,
                    tgt=r.target_entity_id,
                    rtype=r.relationship_type,
                    desc=r.description,
                    doc_id=r.document_id,
                    conf=r.confidence,
                    provider=r.generated_by_provider,
                    model=r.generated_by_model,
                )
        return len(relationships)

    def get_relationships(self, document_id: str) -> list[Relationship]:
        driver = self._get_driver()
        with driver.session() as session:
            result = session.run(
                "MATCH (a)-[r:RELATED {document_id: $doc_id}]->(b) "
                "RETURN r",
                doc_id=document_id,
            )
            return [
                self._rel_to_relationship(record["r"]) for record in result
            ]

    def delete_relationships(self, document_id: str) -> int:
        driver = self._get_driver()
        with driver.session() as session:
            result = session.run(
                "MATCH ()-[r:RELATED {document_id: $doc_id}]->() "
                "DELETE r RETURN count(r) as cnt",
                doc_id=document_id,
            )
            return result.single()["cnt"]

    def close(self) -> None:
        if self._driver:
            self._driver.close()

    @staticmethod
    def _node_to_entity(node) -> Entity:
        return Entity(
            id=node["id"],
            document_id=node.get("document_id", ""),
            name=node.get("name", ""),
            entity_type=node.get("entity_type", ""),
            description=node.get("description", ""),
            source_chunk_id=node.get("source_chunk_id", ""),
            generated_by_provider=node.get("generated_by_provider", ""),
            generated_by_model=node.get("generated_by_model", ""),
            metadata=json.loads(node.get("metadata_json", "{}"))
            if node.get("metadata_json")
            else {},
        )

    @staticmethod
    def _rel_to_relationship(rel) -> Relationship:
        return Relationship(
            id=rel["id"],
            source_entity_id="",
            target_entity_id="",
            relationship_type=rel.get("relationship_type", ""),
            description=rel.get("description", ""),
            document_id=rel.get("document_id", ""),
            generated_by_provider=rel.get("generated_by_provider", ""),
            generated_by_model=rel.get("generated_by_model", ""),
            confidence=rel.get("confidence", 1.0),
        )
