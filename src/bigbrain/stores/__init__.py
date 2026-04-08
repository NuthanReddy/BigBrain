"""Polyglot entity store — pluggable backends for entities, relationships, and vectors."""

from bigbrain.stores.base import EntityStoreBackend
from bigbrain.stores.factory import create_entity_store

__all__ = ["EntityStoreBackend", "create_entity_store"]
