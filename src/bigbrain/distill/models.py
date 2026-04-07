"""Data models for the distillation pipeline."""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Chunk:
    """A chunk of text extracted from a document for processing."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    document_id: str = ""
    content: str = ""
    content_hash: str = ""  # SHA-256 hash for incremental distillation
    start_offset: int = 0
    end_offset: int = 0
    section_title: str = ""
    chunk_index: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def compute_hash(self) -> str:
        """Compute and store a content hash. Returns the hash."""
        self.content_hash = hashlib.sha256(self.content.encode()).hexdigest()[:16]
        return self.content_hash


@dataclass
class Summary:
    """A generated summary of a document or chunk."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    document_id: str = ""
    chunk_id: str = ""  # empty if summarizing whole document
    content: str = ""
    summary_type: str = "document"  # "document", "section", "chunk"
    generated_by_provider: str = ""
    generated_by_model: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Entity:
    """A named entity or key concept extracted from text."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    document_id: str = ""
    name: str = ""
    entity_type: str = ""  # "algorithm", "data_structure", "concept", "person", "theorem", etc.
    description: str = ""
    source_chunk_id: str = ""
    generated_by_provider: str = ""
    generated_by_model: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Relationship:
    """A relationship between two entities."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_entity_id: str = ""
    target_entity_id: str = ""
    relationship_type: str = ""  # "is_a", "part_of", "uses", "implements", "related_to", "prerequisite_of"
    description: str = ""
    document_id: str = ""
    generated_by_provider: str = ""
    generated_by_model: str = ""
    confidence: float = 1.0  # 0.0 to 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DistillResult:
    """Aggregate result from a distillation run on a document."""
    document_id: str = ""
    chunks: list[Chunk] = field(default_factory=list)
    summaries: list[Summary] = field(default_factory=list)
    entities: list[Entity] = field(default_factory=list)
    relationships: list[Relationship] = field(default_factory=list)
    provider: str = ""
    model: str = ""
    errors: list[str] = field(default_factory=list)
