"""Unified digest pipeline — one AI call, multiple output targets.

Generates rich study-note-quality content from KB chunks, then renders
to the requested target format:

- ``markdown`` (default) — detailed study notes per section
- ``flashcard`` — Q/A flashcards for spaced repetition
- ``cheatsheet`` — condensed reference sheet
- ``qa`` — self-test question & answer pairs
- ``wiki`` — writes to wiki/ directory for MkDocs serving
- ``notion`` — creates Notion pages under a parent page
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from bigbrain.config import BigBrainConfig, load_config
from bigbrain.kb.models import Document
from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger
from bigbrain.providers.registry import ProviderRegistry

logger = get_logger(__name__)

VALID_TARGETS = ("markdown", "flashcard", "cheatsheet", "qa", "wiki", "notion")

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

# Reformat prompts — take existing digest markdown and reformat
_FLASHCARD_PROMPT = '''Convert these study notes into flashcard Q&A pairs.
Return as Markdown with ## Q: and **A:** format. Create 10-20 cards covering the most important concepts.

Study notes:
{content}

Flashcards:'''

_CHEATSHEET_PROMPT = '''Condense these study notes into a one-page cheatsheet.
Use compact formatting: tables, bullet points, code snippets. No prose paragraphs.
Focus on formulas, complexity, key properties, and quick-reference facts.

Study notes:
{content}

Cheatsheet:'''

_QA_PROMPT = '''Generate self-test questions from these study notes.
Each question should test understanding, not just recall. Include both conceptual and problem-solving questions.
Format: ## Q: question\\n**A:** detailed answer

Study notes:
{content}

Questions:'''


def _slugify(text: str) -> str:
    """Convert a title to a filesystem-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:80]


@dataclass
class DigestResult:
    """Result of a digest build."""
    written: int = 0
    skipped: int = 0
    errors: list[str] = field(default_factory=list)
    output_dir: str = ""
    digest_files: list[str] = field(default_factory=list)


class DigestBuilder:
    """Unified digest pipeline: KB chunks → AI → multiple output targets."""

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
        target: str = "markdown",
        model: str = "",
        force: bool = False,
        notion_parent_id: str = "",
        on_duplicate: str = "skip",
    ) -> DigestResult:
        """Generate digest for a document.

        1. Check if KB content changed since last digest (skip if unchanged)
        2. Generate markdown study notes (one per chunk) — cached in digest/<doc>/
        3. If target != markdown, reformat each file to the requested format
        4. If target is wiki/notion, copy/push to destination
        """
        doc = self._store.get_document(doc_id)
        if doc is None:
            logger.warning("Document not found: %s", doc_id)
            return DigestResult(errors=[f"Document not found: {doc_id}"])

        # Check if KB content has changed since last digest
        if not force and self._is_digest_current(doc):
            logger.info("Digest up-to-date for %s — skipping", doc.title)
            result = DigestResult()
            result.output_dir = str(self._output_dir / _slugify(doc.title))
            # Populate digest_files from existing files for downstream targets
            out_dir = Path(result.output_dir)
            if out_dir.is_dir():
                result.digest_files = sorted(
                    str(p) for p in out_dir.glob("*.md") if not p.stem.startswith(".")
                )
                result.skipped = len(result.digest_files)

            if target == "markdown":
                return result
            # For other targets, use cached digest files
            if target in ("flashcard", "cheatsheet", "qa"):
                return self._reformat(doc, result, target=target, model=model, force=force)
            elif target == "wiki":
                return self._to_wiki(doc, result)
            elif target == "notion":
                return self._to_notion(doc, result, parent_id=notion_parent_id)
            return result

        # Step 1: Generate base markdown digest (the expensive AI call)
        base_result = self._generate_base_digest(doc, model=model, force=force)

        # Save content hash for incremental check
        self._save_digest_hash(doc)

        if target == "markdown":
            return base_result

        # Step 2: Reformat or route to target
        if target in ("flashcard", "cheatsheet", "qa"):
            return self._reformat(doc, base_result, target=target, model=model, force=force)
        elif target == "wiki":
            return self._to_wiki(doc, base_result)
        elif target == "notion":
            return self._to_notion(doc, base_result, parent_id=notion_parent_id)

        base_result.errors.append(f"Unknown target: {target}")
        return base_result

    def _compute_content_hash(self, doc: Document) -> str:
        """Compute a hash of all chunk content for change detection."""
        import hashlib
        chunks = self._store.get_chunks(doc.id)
        if chunks:
            combined = "|".join(c.content_hash or c.content[:100] for c in chunks)
        elif doc.sections:
            combined = "|".join(s.content[:100] for s in doc.sections if s.content)
        else:
            combined = doc.content[:1000]
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def _is_digest_current(self, doc: Document) -> bool:
        """Check if digest output is up-to-date with KB content."""
        doc_slug = _slugify(doc.title)
        hash_path = self._output_dir / doc_slug / ".digest_hash"
        if not hash_path.exists():
            return False
        stored = hash_path.read_text(encoding="utf-8").strip()
        current = self._compute_content_hash(doc)
        return stored == current

    def _save_digest_hash(self, doc: Document) -> None:
        """Save content hash after successful digest generation."""
        doc_slug = _slugify(doc.title)
        hash_path = self._output_dir / doc_slug / ".digest_hash"
        hash_path.parent.mkdir(parents=True, exist_ok=True)
        hash_path.write_text(self._compute_content_hash(doc), encoding="utf-8")

    def _generate_base_digest(
        self, doc: Document, *, model: str = "", force: bool = False,
    ) -> DigestResult:
        """Generate base markdown study notes per chunk. Cached on disk."""
        result = DigestResult()
        doc_slug = _slugify(doc.title)
        out_dir = self._output_dir / doc_slug
        out_dir.mkdir(parents=True, exist_ok=True)
        result.output_dir = str(out_dir)

        # Get chunks or fall back to sections
        chunks = self._store.get_chunks(doc.id)
        items: list[tuple[str, str]] = []  # (title, content)

        if chunks:
            for c in chunks:
                title = c.section_title or f"Section {c.chunk_index + 1}"
                items.append((title, c.content or ""))
        elif doc.sections:
            for i, sec in enumerate(doc.sections):
                title = sec.title or f"Section {i + 1}"
                items.append((title, sec.content or ""))
        else:
            result.errors.append("No chunks or sections available")
            return result

        for title, content in items:
            if not content.strip():
                result.skipped += 1
                continue

            slug = _slugify(title) or f"section-{result.written + result.skipped + 1:02d}"
            out_path = out_dir / f"{slug}.md"

            if out_path.exists() and not force:
                logger.debug("Using cached: %s", out_path)
                result.skipped += 1
                result.digest_files.append(str(out_path))
                continue

            prompt = (
                _DIGEST_TEMPLATE if len(content) > 500 else _DIGEST_TEMPLATE_SHORT
            ).format(doc_title=doc.title, section_title=title, content=content[:12000])

            try:
                resp = self._registry.chat(
                    [{"role": "system", "content": _DIGEST_SYSTEM},
                     {"role": "user", "content": prompt}],
                    model=model, max_tokens=4000,
                )
                markdown = f"# {title}\n\n{resp.text.strip()}\n"
                out_path.write_text(markdown, encoding="utf-8")
                result.written += 1
                result.digest_files.append(str(out_path))
                logger.info("Wrote: %s", out_path)
            except Exception as exc:
                result.errors.append(f"{title}: {exc}")
                logger.warning("Failed for '%s': %s", title, exc)

        return result

    def _reformat(
        self, doc: Document, base_result: DigestResult,
        target: str, model: str = "", force: bool = False,
    ) -> DigestResult:
        """Reformat existing digest markdown into flashcard/cheatsheet/qa."""
        result = DigestResult()
        doc_slug = _slugify(doc.title)
        out_dir = self._output_dir / doc_slug
        result.output_dir = str(out_dir)

        prompts = {"flashcard": _FLASHCARD_PROMPT, "cheatsheet": _CHEATSHEET_PROMPT, "qa": _QA_PROMPT}
        reformat_prompt = prompts.get(target, _FLASHCARD_PROMPT)

        # Collect all digest files
        all_files = base_result.digest_files
        if not all_files:
            all_files = sorted(str(p) for p in out_dir.glob("*.md") if p.stem != target)

        for filepath in all_files:
            path = Path(filepath)
            if not path.exists():
                continue

            out_path = out_dir / f"{path.stem}-{target}.md"
            if out_path.exists() and not force:
                result.skipped += 1
                continue

            content = path.read_text(encoding="utf-8")
            prompt = reformat_prompt.format(content=content[:10000])

            try:
                resp = self._registry.chat(
                    [{"role": "system", "content": _DIGEST_SYSTEM},
                     {"role": "user", "content": prompt}],
                    model=model, max_tokens=4000,
                )
                out_path.write_text(f"# {path.stem} — {target.title()}\n\n{resp.text.strip()}\n", encoding="utf-8")
                result.written += 1
                logger.info("Wrote %s: %s", target, out_path)
            except Exception as exc:
                result.errors.append(f"{path.stem}: {exc}")

        return result

    def _to_wiki(self, doc: Document, base_result: DigestResult) -> DigestResult:
        """Copy digest files to wiki/ directory."""
        result = DigestResult()
        wiki_dir = Path("wiki")
        wiki_dir.mkdir(parents=True, exist_ok=True)
        doc_slug = _slugify(doc.title)

        all_files = base_result.digest_files
        if not all_files:
            out_dir = self._output_dir / doc_slug
            all_files = sorted(str(p) for p in out_dir.glob("*.md"))

        for filepath in all_files:
            path = Path(filepath)
            if not path.exists():
                continue
            dest = wiki_dir / f"{doc_slug}-{path.name}"
            content = path.read_text(encoding="utf-8")
            dest.write_text(content, encoding="utf-8")
            result.written += 1

        # Create/update index
        index = wiki_dir / "index.md"
        if not index.exists():
            links = [f"- [{Path(f).stem}]({doc_slug}-{Path(f).name})" for f in all_files]
            index.write_text(
                f"# BigBrain Wiki\n\n## {doc.title}\n\n" + "\n".join(links) + "\n",
                encoding="utf-8",
            )

        result.output_dir = str(wiki_dir)
        logger.info("Copied %d digest files to wiki/", result.written)
        return result

    def _to_notion(
        self, doc: Document, base_result: DigestResult, parent_id: str = "",
    ) -> DigestResult:
        """Push digest files as Notion child pages."""
        result = DigestResult()

        if not parent_id:
            result.errors.append("--notion-parent required for --to notion")
            return result

        try:
            from bigbrain.notion.client import NotionClient
            from bigbrain.notion.exporter import _paragraph, _heading, _divider
            from bigbrain.config import load_config
            cfg = load_config()
            client = NotionClient.from_config(cfg.notion)
        except Exception as exc:
            result.errors.append(f"Notion client error: {exc}")
            return result

        doc_slug = _slugify(doc.title)
        all_files = base_result.digest_files
        if not all_files:
            out_dir = self._output_dir / doc_slug
            all_files = sorted(str(p) for p in out_dir.glob("*.md"))

        # BigBrain marker block
        marker = {
            "object": "block",
            "type": "callout",
            "callout": {
                "icon": {"type": "emoji", "emoji": "🧠"},
                "rich_text": [{"type": "text", "text": {"content": "Generated by BigBrain — auto-imported pages will skip this page."}}],
                "color": "gray_background",
            },
        }

        for filepath in all_files:
            path = Path(filepath)
            if not path.exists():
                continue

            content = path.read_text(encoding="utf-8")
            title = content.split("\n")[0].lstrip("# ").strip() or path.stem

            # Convert markdown to Notion blocks (simplified)
            blocks = [marker]
            for line in content.split("\n"):
                line = line.strip()
                if not line:
                    continue
                if line.startswith("# "):
                    continue  # skip title (it's the page title)
                elif line.startswith("## "):
                    blocks.append(_heading(line[3:], level=2))
                elif line.startswith("### "):
                    blocks.append(_heading(line[4:], level=3))
                else:
                    for chunk in [line[i:i+1900] for i in range(0, len(line), 1900)]:
                        blocks.append(_paragraph(chunk))

            try:
                first = blocks[:100]
                rest = blocks[100:]
                page = client.create_page(parent_id, title, children=first)
                page_id = page["id"]
                while rest:
                    batch = rest[:100]
                    rest = rest[100:]
                    client._client.blocks.children.append(block_id=page_id, children=batch)
                result.written += 1
                logger.info("Created Notion page: %s", title)
            except Exception as exc:
                result.errors.append(f"{title}: {exc}")

        result.output_dir = "notion"
        return result
