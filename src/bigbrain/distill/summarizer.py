"""AI-powered summarization for the distillation pipeline."""

from __future__ import annotations

from bigbrain.distill.models import Chunk, Summary
from bigbrain.kb.models import Document
from bigbrain.logging_config import get_logger
from bigbrain.providers.registry import ProviderRegistry

logger = get_logger(__name__)

SUMMARIZE_SYSTEM = (
    "You are a precise summarizer. Create clear, accurate summaries "
    "focusing on key concepts, definitions, and important details. Be concise."
)

SUMMARIZE_DOC_TEMPLATE = (
    "Summarize the following document concisely in at most {max_length} words.\n\n"
    "Title: {title}\n\nContent:\n{content}\n\nSummary:"
)

SUMMARIZE_CHUNK_TEMPLATE = (
    "Summarize the following text concisely in at most {max_length} words. "
    "Focus on key ideas.\n\nText:\n{content}\n\nSummary:"
)


class Summarizer:
    """Generates summaries using an AI provider."""

    def __init__(self, registry: ProviderRegistry) -> None:
        self._registry = registry

    def summarize_document(
        self, doc: Document, *, max_length: int = 500, model: str = ""
    ) -> Summary:
        """Summarize an entire document."""
        content = doc.content[:8000]  # truncate for context window
        prompt = SUMMARIZE_DOC_TEMPLATE.format(
            title=doc.title, content=content, max_length=max_length
        )

        messages = [
            {"role": "system", "content": SUMMARIZE_SYSTEM},
            {"role": "user", "content": prompt},
        ]
        resp = self._registry.chat(messages, model=model)

        return Summary(
            document_id=doc.id,
            content=resp.text,
            summary_type="document",
            generated_by_provider=resp.provider,
            generated_by_model=resp.model,
        )

    def summarize_chunk(
        self, chunk: Chunk, *, max_length: int = 200, model: str = ""
    ) -> Summary:
        """Summarize a single chunk."""
        prompt = SUMMARIZE_CHUNK_TEMPLATE.format(
            content=chunk.content, max_length=max_length
        )

        messages = [
            {"role": "system", "content": SUMMARIZE_SYSTEM},
            {"role": "user", "content": prompt},
        ]
        resp = self._registry.chat(messages, model=model)

        return Summary(
            document_id=chunk.document_id,
            chunk_id=chunk.id,
            content=resp.text,
            summary_type="chunk",
            generated_by_provider=resp.provider,
            generated_by_model=resp.model,
        )

    def summarize_chunks(
        self, chunks: list[Chunk], *, max_length: int = 200, model: str = ""
    ) -> list[Summary]:
        """Summarize multiple chunks."""
        summaries = []
        for chunk in chunks:
            try:
                s = self.summarize_chunk(chunk, max_length=max_length, model=model)
                summaries.append(s)
            except Exception as exc:
                logger.warning("Failed to summarize chunk %s: %s", chunk.id, exc)
        return summaries

    def summarize_sections(
        self, doc: Document, *, max_length: int = 300, model: str = ""
    ) -> list[Summary]:
        """Generate a summary for each document section with enough content."""
        summaries: list[Summary] = []
        for i, section in enumerate(doc.sections):
            if len(section.content.strip()) < 100:
                continue
            try:
                prompt = SUMMARIZE_CHUNK_TEMPLATE.format(
                    content=section.content[:4000], max_length=max_length
                )
                messages = [
                    {"role": "system", "content": SUMMARIZE_SYSTEM},
                    {"role": "user", "content": prompt},
                ]
                resp = self._registry.chat(messages, model=model)
                summaries.append(Summary(
                    document_id=doc.id,
                    content=resp.text,
                    summary_type="section",
                    generated_by_provider=resp.provider,
                    generated_by_model=resp.model,
                    metadata={"section_title": section.title, "section_index": i},
                ))
            except Exception as exc:
                logger.warning("Section summary failed for '%s': %s", section.title, exc)
        return summaries
