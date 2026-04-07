"""Shared data models for the BigBrain knowledge base.

These contracts define the canonical shapes that ingestion, distillation,
and compilation passes all operate on.  Phase 1 uses them for ingestion
output; Phase 2+ will persist them into JSON/JSONL and SQLite stores.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class SourceMetadata:
    """Provenance information about the original source file."""

    file_path: str
    file_extension: str
    source_type: str  # "txt", "md", "pdf", "py"
    modified_at: datetime | None = None
    size_bytes: int = 0
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentSection:
    """A logical section within a document (heading, page, code block, etc.)."""

    title: str
    content: str
    level: int = 0  # heading depth or page number
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Document:
    """Canonical knowledge-base document produced by ingestion.

    Every ingester must return Document instances with at least *title*,
    *content*, and *source* populated.  Sections and metadata are optional
    enrichments.
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    content: str = ""
    source: SourceMetadata | None = None
    language: str = ""  # e.g. "python", "markdown", ""
    sections: list[DocumentSection] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class IngestionResult:
    """Aggregate result from an ingestion run (one or more files)."""

    documents: list[Document] = field(default_factory=list)
    processed: int = 0
    skipped: int = 0
    failed: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
