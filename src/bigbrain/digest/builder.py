"""Digest generator — produces rich chapter-by-chapter study notes from KB data.

Reads chunks (sections) from the knowledge base, sends each to an AI provider
with the full source text, and writes comprehensive markdown summaries to the
``digest/`` directory.  Output quality matches hand-written study notes with
key concepts, algorithms, complexity analysis, theorems, and examples.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from bigbrain.config import BigBrainConfig, load_config
from bigbrain.kb.models import Document
from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger
from bigbrain.providers.registry import ProviderRegistry

logger = get_logger(__name__)

_DIGEST_SYSTEM = (
    "You are an expert technical writer creating comprehensive study notes. "
    "Write detailed, well-structured Markdown. "
    "Include key concepts, algorithms with complexity analysis, theorems with "
    "formal statements, data structures with operations, and concrete examples. "
    "Use ## for major sections and ### for subsections. "
    "Include tables for complexity comparisons where appropriate."
)

_DIGEST_TEMPLATE = '''Write comprehensive study notes for the following section of "{doc_title}".

Section title: {section_title}

Source text:
{content}

Requirements:
- Start with a brief ## Overview paragraph
- ## Key Concepts section with bullet points explaining each important idea
- ## Algorithms and Techniques section with ### per algorithm: how it works, pseudocode sketch, time/space complexity
- ## Complexity Analysis table if multiple algorithms are compared
- For theorems: state formally and explain significance
- For data structures: key operations and their complexities
- Include concrete examples from the source where available
- Be thorough — this should be reference-quality study notes
- Write in Markdown format

Study notes:'''

_DIGEST_TEMPLATE_SHORT = '''Write a concise summary of this section from "{doc_title}".

Section: {section_title}

Text:
{content}

Write a detailed Markdown summary with key concepts, definitions, and important details. Use ## headings.

Summary:'''


def _slugify(text: str) -> str:
    """Convert a title to a filesystem-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:80]


class DigestBuilder:
    """Generates digest markdown files from KB chunks."""

    def __init__(
        self,
        store: KBStore,
        registry: ProviderRegistry,
        output_dir: str | Path = "digest",
    ) -> None:
        self._store = store
        self._registry = registry
        self._output_dir = Path(output_dir)

    @classmethod
    def from_config(cls, config: BigBrainConfig | None = None) -> DigestBuilder:
        if config is None:
            config = load_config()
        store = KBStore(config.kb_db_path)
        registry = ProviderRegistry.from_config(config.providers)
        return cls(store=store, registry=registry)

    def close(self) -> None:
        self._store.close()

    def __enter__(self) -> DigestBuilder:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def build(
        self,
        doc_id: str,
        *,
        model: str = "",
        force: bool = False,
    ) -> DigestResult:
        """Generate digest for a document.

        Creates one markdown file per chunk (section/chapter) under
        ``digest/<doc-title>/<section-slug>.md``.
        """
        doc = self._store.get_document(doc_id)
        if doc is None:
            logger.warning("Document not found: %s", doc_id)
            return DigestResult(errors=[f"Document not found: {doc_id}"])

        chunks = self._store.get_chunks(doc_id)
        if not chunks:
            # Fall back to document sections
            logger.info("No chunks found, using document sections directly")
            return self._build_from_sections(doc, model=model, force=force)

        return self._build_from_chunks(doc, chunks, model=model, force=force)

    def _build_from_chunks(
        self, doc: Document, chunks: list, *, model: str = "", force: bool = False,
    ) -> DigestResult:
        """Generate digest from KB chunks."""
        result = DigestResult()
        doc_slug = _slugify(doc.title)
        out_dir = self._output_dir / doc_slug
        out_dir.mkdir(parents=True, exist_ok=True)

        for chunk in chunks:
            title = chunk.section_title or f"Section {chunk.chunk_index + 1}"
            slug = _slugify(title)
            if not slug:
                slug = f"section-{chunk.chunk_index + 1:02d}"
            out_path = out_dir / f"{slug}.md"

            if out_path.exists() and not force:
                logger.debug("Skipping existing: %s", out_path)
                result.skipped += 1
                continue

            content = chunk.content or ""
            if not content.strip():
                result.skipped += 1
                continue

            # Choose prompt based on content length
            if len(content) > 500:
                prompt = _DIGEST_TEMPLATE.format(
                    doc_title=doc.title,
                    section_title=title,
                    content=content[:12000],
                )
            else:
                prompt = _DIGEST_TEMPLATE_SHORT.format(
                    doc_title=doc.title,
                    section_title=title,
                    content=content,
                )

            try:
                resp = self._registry.chat(
                    [
                        {"role": "system", "content": _DIGEST_SYSTEM},
                        {"role": "user", "content": prompt},
                    ],
                    model=model,
                    max_tokens=4000,
                )
                markdown = f"# {title}\n\n{resp.text.strip()}\n"
                out_path.write_text(markdown, encoding="utf-8")
                result.written += 1
                logger.info("Wrote digest: %s", out_path)
            except Exception as exc:
                result.errors.append(f"{title}: {exc}")
                logger.warning("Digest failed for '%s': %s", title, exc)

        result.output_dir = str(out_dir)
        return result

    def _build_from_sections(
        self, doc: Document, *, model: str = "", force: bool = False,
    ) -> DigestResult:
        """Generate digest directly from document sections (no chunks in KB)."""
        result = DigestResult()
        doc_slug = _slugify(doc.title)
        out_dir = self._output_dir / doc_slug
        out_dir.mkdir(parents=True, exist_ok=True)

        sections = doc.sections or []
        if not sections:
            result.errors.append("No sections or chunks available")
            return result

        for i, sec in enumerate(sections):
            title = sec.title or f"Section {i + 1}"
            content = sec.content or ""
            if not content.strip():
                result.skipped += 1
                continue

            slug = _slugify(title)
            if not slug:
                slug = f"section-{i + 1:02d}"
            out_path = out_dir / f"{slug}.md"

            if out_path.exists() and not force:
                result.skipped += 1
                continue

            if len(content) > 500:
                prompt = _DIGEST_TEMPLATE.format(
                    doc_title=doc.title,
                    section_title=title,
                    content=content[:12000],
                )
            else:
                prompt = _DIGEST_TEMPLATE_SHORT.format(
                    doc_title=doc.title,
                    section_title=title,
                    content=content,
                )

            try:
                resp = self._registry.chat(
                    [
                        {"role": "system", "content": _DIGEST_SYSTEM},
                        {"role": "user", "content": prompt},
                    ],
                    model=model,
                    max_tokens=4000,
                )
                markdown = f"# {title}\n\n{resp.text.strip()}\n"
                out_path.write_text(markdown, encoding="utf-8")
                result.written += 1
                logger.info("Wrote digest: %s", out_path)
            except Exception as exc:
                result.errors.append(f"{title}: {exc}")
                logger.warning("Digest failed for '%s': %s", title, exc)

        result.output_dir = str(out_dir)
        return result


from dataclasses import dataclass, field


@dataclass
class DigestResult:
    """Result of a digest build."""
    written: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)
    output_dir: str = ""
