"""Context assembly — builds a context string from retrieved chunks within a token budget."""

from __future__ import annotations

from bigbrain.rag.retriever import RetrievedChunk
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


def assemble_context(
    chunks: list[RetrievedChunk],
    *,
    max_chars: int = 12000,
    separator: str = "\n\n---\n\n",
) -> str:
    """Assemble retrieved chunks into a single context string.

    Chunks are added in order until the character budget is exhausted.
    Each chunk is labeled with its source for attribution.

    Args:
        chunks: Retrieved chunks in relevance order
        max_chars: Maximum total characters for the context
        separator: Separator between chunks

    Returns:
        Assembled context string
    """
    parts: list[str] = []
    total_chars = 0

    for chunk in chunks:
        # Build labeled chunk
        label = f"[{chunk.source_title}"
        if chunk.section_title:
            label += f" — {chunk.section_title}"
        label += "]"

        entry = f"{label}\n{chunk.text}"
        entry_len = len(entry) + len(separator)

        if total_chars + entry_len > max_chars:
            # Try to fit a truncated version
            remaining = max_chars - total_chars - len(separator) - len(label) - 5
            if remaining > 200:
                truncated = chunk.text[:remaining] + "..."
                parts.append(f"{label}\n{truncated}")
            break

        parts.append(entry)
        total_chars += entry_len

    return separator.join(parts)
