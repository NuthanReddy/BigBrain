"""Data models for the knowledge compilation pipeline."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class OutputFormat(str, Enum):
    """Supported compilation output formats."""
    MARKDOWN = "markdown"
    FLASHCARD = "flashcard"
    CHEATSHEET = "cheatsheet"
    QA = "qa"
    STUDY_GUIDE = "study_guide"


@dataclass
class Flashcard:
    """A single flashcard with front (question) and back (answer)."""
    front: str = ""
    back: str = ""
    tags: list[str] = field(default_factory=list)
    source_entity_id: str = ""


@dataclass
class QAPair:
    """A question-answer pair for study/review."""
    question: str = ""
    answer: str = ""
    difficulty: str = "medium"  # easy, medium, hard
    topic: str = ""
    source_chunk_id: str = ""


@dataclass
class CompileOutput:
    """Result of a compilation run."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    format: OutputFormat = OutputFormat.MARKDOWN
    title: str = ""
    content: str = ""  # The rendered output (markdown string, JSON, etc.)
    source_doc_id: str = ""
    source_doc_title: str = ""
    flashcards: list[Flashcard] = field(default_factory=list)
    qa_pairs: list[QAPair] = field(default_factory=list)
    generated_by_provider: str = ""
    generated_by_model: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CompileResult:
    """Aggregate result from a compilation run."""
    outputs: list[CompileOutput] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    total_documents: int = 0
