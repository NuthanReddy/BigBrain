"""Text chunking strategies for the distillation pipeline."""

from __future__ import annotations

from bigbrain.distill.models import Chunk
from bigbrain.kb.models import Document
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


def chunk_by_section(doc: Document, *, min_length: int = 50) -> list[Chunk]:
    """Chunk by document sections. Each section becomes a chunk.
    Sections shorter than min_length are merged with the next section.
    Falls back to by_paragraph if no sections."""
    if not doc.sections:
        return chunk_by_paragraph(doc, min_length=min_length)

    chunks: list[Chunk] = []
    buffer = ""
    buffer_title = ""
    for i, sec in enumerate(doc.sections):
        text = sec.content.strip()
        if not text:
            continue
        if len(text) < min_length and i < len(doc.sections) - 1:
            buffer += f"\n\n{text}" if buffer else text
            buffer_title = buffer_title or sec.title
            continue

        content = f"{buffer}\n\n{text}".strip() if buffer else text
        title = buffer_title or sec.title
        chunks.append(Chunk(
            document_id=doc.id,
            content=content,
            section_title=title,
            chunk_index=len(chunks),
        ))
        buffer = ""
        buffer_title = ""

    if buffer:
        chunks.append(Chunk(
            document_id=doc.id,
            content=buffer,
            section_title=buffer_title,
            chunk_index=len(chunks),
        ))
    return chunks


def chunk_sliding_window(
    doc: Document, *, chunk_size: int = 1000, overlap: int = 200
) -> list[Chunk]:
    """Sliding window chunker. Splits content into fixed-size overlapping windows."""
    text = doc.content.strip()
    if not text:
        return []

    chunks: list[Chunk] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        content = text[start:end]
        chunks.append(Chunk(
            document_id=doc.id,
            content=content,
            start_offset=start,
            end_offset=min(end, len(text)),
            chunk_index=len(chunks),
        ))
        start += chunk_size - overlap
        if start >= len(text):
            break
    return chunks


def chunk_by_paragraph(doc: Document, *, min_length: int = 50) -> list[Chunk]:
    """Chunk by paragraphs (double newline separated). Merges short paragraphs."""
    text = doc.content.strip()
    if not text:
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[Chunk] = []
    buffer = ""

    for para in paragraphs:
        if len(para) < min_length:
            buffer += f"\n\n{para}" if buffer else para
            continue
        content = f"{buffer}\n\n{para}".strip() if buffer else para
        chunks.append(Chunk(
            document_id=doc.id,
            content=content,
            chunk_index=len(chunks),
        ))
        buffer = ""

    if buffer:
        chunks.append(Chunk(
            document_id=doc.id,
            content=buffer,
            chunk_index=len(chunks),
        ))
    return chunks


def chunk_document(
    doc: Document,
    *,
    strategy: str = "by_section",
    chunk_size: int = 1000,
    overlap: int = 200,
    min_length: int = 50,
    max_chunks: int = 50,
) -> list[Chunk]:
    """Main entry point — dispatch to the appropriate strategy."""
    if strategy == "by_section":
        chunks = chunk_by_section(doc, min_length=min_length)
    elif strategy == "sliding_window":
        chunks = chunk_sliding_window(doc, chunk_size=chunk_size, overlap=overlap)
    elif strategy == "by_paragraph":
        chunks = chunk_by_paragraph(doc, min_length=min_length)
    else:
        logger.warning("Unknown chunk strategy '%s', using by_section", strategy)
        chunks = chunk_by_section(doc, min_length=min_length)

    if len(chunks) > max_chunks:
        logger.warning(
            "Truncating %d chunks to %d for document %s",
            len(chunks), max_chunks, doc.id,
        )
        chunks = chunks[:max_chunks]

    # Compute content hashes for incremental distillation
    for chunk in chunks:
        chunk.compute_hash()

    return chunks
