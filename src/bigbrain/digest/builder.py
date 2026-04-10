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

_DIGEST_BATCH_TEMPLATE = '''Write comprehensive study notes for EACH of the following chapters from "{doc_title}".

For EACH chapter, write a complete section starting with:
# <Chapter Title>

Then include:
- ## Overview paragraph
- ## Key Concepts with bullet points
- ## Algorithms and Techniques with ### per algorithm (how it works, time/space complexity)
- ## Complexity Analysis table if applicable
- Theorems stated formally, data structures with operations, concrete examples

CRITICAL: You MUST write ALL chapters listed below. Do NOT truncate, skip, or say "continue later". Separate each with "# <Chapter Title>" on its own line.

{chapters_block}

Study notes (write ALL chapters, separated by # headings):'''

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


def _format_raw_text(text: str, chapter_title: str = "") -> str:
    """Convert raw PDF text into readable markdown.

    Detects section headings (15.1, 15.2...), theorem/lemma/corollary
    labels, procedure names, and adds markdown structure.
    """
    lines = text.split("\n")
    out: list[str] = []

    if chapter_title:
        out.append(f"# {chapter_title}\n")

    # Patterns
    # Section heading: "15.1 Rod cutting" or "15.1  Rod cutting"
    section_re = re.compile(r'^(\d+\.\d+(?:\.\d+)?)\s{1,4}([A-Z].*)')
    # Theorem/Lemma/Corollary: "Theorem 15.1" or "Lemma 15.2"
    theorem_re = re.compile(r'^(Theorem|Lemma|Corollary|Definition|Property)\s+[\d.]+')
    # Procedure name: all-caps with hyphens like "CUT-ROD", "MERGE-SORT"
    procedure_re = re.compile(r'^([A-Z][A-Z-]+(?:\.[A-Z-]+)?)\s*\(')
    # Exercise heading: "Exercises" or "Problems"
    exercise_re = re.compile(r'^(Exercises|Problems)\s*$')
    # Equation label: "(15.1)" at end of line
    equation_re = re.compile(r'\((\d+\.\d+)\)\s*$')

    in_procedure = False
    prev_blank = False

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if not prev_blank:
                out.append("")
            prev_blank = True
            in_procedure = False
            continue
        prev_blank = False

        # Detect section headings → ## heading
        m = section_re.match(stripped)
        if m:
            out.append(f"\n## {m.group(1)} {m.group(2)}\n")
            continue

        # Detect theorem/lemma → **bold** block
        m = theorem_re.match(stripped)
        if m:
            out.append(f"\n> **{stripped}**\n")
            continue

        # Detect procedure start → code block
        m = procedure_re.match(stripped)
        if m:
            out.append(f"\n```\n{stripped}")
            in_procedure = True
            continue

        if in_procedure:
            # Lines that look like pseudocode (indented or short)
            if stripped and (line.startswith("  ") or line.startswith("\t") or len(stripped) < 80):
                out.append(stripped)
                continue
            else:
                out.append("```\n")
                in_procedure = False

        # Detect exercise headers
        if exercise_re.match(stripped):
            out.append(f"\n## {stripped}\n")
            continue

        # Format equations: wrap in $$ if it looks like math
        if equation_re.search(stripped):
            eq_match = equation_re.search(stripped)
            label = eq_match.group(1) if eq_match else ""
            out.append(f"{stripped}")
            continue

        # Regular text
        out.append(stripped)

    # Close any open procedure block
    if in_procedure:
        out.append("```")

    result = "\n".join(out)
    # Clean up excessive blank lines
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip() + "\n"


# Max chars of source text per batch — keep small so AI response fits in ~16K output tokens
# 2-3 chapters per batch is optimal for detailed study notes
_BATCH_MAX_CHARS = 15000


def _split_batch_response(response: str, titles: list[str]) -> dict[str, str]:
    """Split a batched AI response into per-chapter sections.

    Looks for '# <title>' headings to split. Falls back to splitting
    on any '# ' heading if exact titles aren't found.
    """
    result: dict[str, str] = {}

    # Try splitting on exact titles first
    parts = re.split(r'^# ', response, flags=re.MULTILINE)

    for part in parts:
        if not part.strip():
            continue
        # First line is the title
        lines = part.split("\n", 1)
        heading = lines[0].strip()
        body = lines[1].strip() if len(lines) > 1 else ""

        if not body:
            continue

        # Match to one of the expected titles
        matched = False
        for title in titles:
            if title.lower().strip() in heading.lower():
                result[title] = f"# {heading}\n\n{body}"
                matched = True
                break

        if not matched:
            result[heading] = f"# {heading}\n\n{body}"

    return result


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
        no_ai: bool = False,
        notion_parent_id: str = "",
        on_duplicate: str = "skip",
    ) -> DigestResult:
        """Generate digest for a document.

        Args:
            no_ai: If True, extract raw chapter text without AI calls (instant).
        """
        doc = self._store.get_document(doc_id)
        if doc is None:
            logger.warning("Document not found: %s", doc_id)
            return DigestResult(errors=[f"Document not found: {doc_id}"])

        # Check if KB content has changed since last digest
        # Also verify all chapters are present (not just hash match)
        if not force and self._is_digest_current(doc):
            doc_slug = _slugify(doc.title)
            out_dir = self._output_dir / doc_slug
            existing = sorted(
                str(p) for p in out_dir.glob("*.md") if not p.stem.startswith(".")
            ) if out_dir.is_dir() else []

            # Count expected chapters to verify completeness
            chapters = self._group_into_chapters(doc)
            expected = sum(1 for _, c in chapters if c.strip())

            if len(existing) >= expected:
                logger.info("Digest up-to-date for %s (%d/%d chapters)", doc.title, len(existing), expected)
                result = DigestResult()
                result.output_dir = str(out_dir)
                result.digest_files = existing
                result.skipped = len(existing)

                if target == "markdown":
                    return result
                if target in ("flashcard", "cheatsheet", "qa"):
                    return self._reformat(doc, result, target=target, model=model, force=force)
                elif target == "wiki":
                    return self._to_wiki(doc, result)
                elif target == "notion":
                    return self._to_notion(doc, result, parent_id=notion_parent_id)
                return result
            else:
                logger.info("Digest incomplete: %d/%d chapters, continuing...", len(existing), expected)

        # Step 1: Generate base digest
        if no_ai:
            base_result = self._generate_raw_digest(doc, force=force)
        else:
            base_result = self._generate_base_digest(doc, model=model, force=force)

        self._save_digest_hash(doc)

        if target == "markdown":
            return base_result

        # Step 2: Reformat or route to target
        if target in ("flashcard", "cheatsheet", "qa"):
            if no_ai:
                base_result.errors.append(f"--no-ai incompatible with --to {target} (needs AI to reformat)")
                return base_result
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

    def _generate_raw_digest(
        self, doc: Document, *, force: bool = False,
    ) -> DigestResult:
        """Extract raw chapter text with basic markdown formatting.

        Zero API calls. Groups sections into chapters (via PDF TOC),
        detects section headings, formats pseudocode blocks, and adds
        paragraph structure.
        """
        result = DigestResult()
        doc_slug = _slugify(doc.title)
        out_dir = self._output_dir / doc_slug
        out_dir.mkdir(parents=True, exist_ok=True)
        result.output_dir = str(out_dir)

        chapters = self._group_into_chapters(doc)
        if not chapters:
            result.errors.append("No content available")
            return result

        for title, content in chapters:
            if not content.strip():
                result.skipped += 1
                continue

            slug = _slugify(title) or f"chapter-{result.written + result.skipped + 1:02d}"
            out_path = out_dir / f"{slug}.md"

            if out_path.exists() and not force:
                result.skipped += 1
                result.digest_files.append(str(out_path))
                continue

            formatted = _format_raw_text(content, chapter_title=title)
            out_path.write_text(formatted, encoding="utf-8")
            result.written += 1
            result.digest_files.append(str(out_path))
            logger.info("Wrote: %s (%d chars)", out_path.name, len(formatted))

        logger.info("Raw digest: %d chapters, 0 API calls", result.written)
        return result

    def _generate_base_digest(
        self, doc: Document, *, model: str = "", force: bool = False,
    ) -> DigestResult:
        """Generate study notes: one API call per chapter.

        With TOC-based grouping, a 1300-page PDF becomes ~35 chapters.
        Each call gets the full chapter text and produces detailed notes.
        Cached files are skipped on re-runs.
        """
        result = DigestResult()
        doc_slug = _slugify(doc.title)
        out_dir = self._output_dir / doc_slug
        out_dir.mkdir(parents=True, exist_ok=True)
        result.output_dir = str(out_dir)

        # Build chapter-level items from sections
        chapters = self._group_into_chapters(doc)
        if not chapters:
            result.errors.append("No content available to digest")
            return result

        # Filter to chapters that need processing
        to_process: list[tuple[str, str, Path]] = []
        for title, content in chapters:
            if not content.strip():
                result.skipped += 1
                continue
            slug = _slugify(title) or f"chapter-{len(to_process) + result.skipped + 1:02d}"
            out_path = out_dir / f"{slug}.md"
            if out_path.exists() and not force:
                result.skipped += 1
                result.digest_files.append(str(out_path))
                continue
            to_process.append((title, content, out_path))

        if not to_process:
            logger.info("All chapters cached for %s", doc.title)
            return result

        logger.info(
            "Digest: %d chapters to process (%d cached) for %s",
            len(to_process), result.skipped, doc.title,
        )

        for i, (title, content, out_path) in enumerate(to_process):
            prompt = _DIGEST_TEMPLATE.format(
                doc_title=doc.title,
                section_title=title,
                content=content[:12000],
            )

            try:
                resp = self._registry.chat(
                    [{"role": "system", "content": _DIGEST_SYSTEM},
                     {"role": "user", "content": prompt}],
                    model=model, max_tokens=4096,
                )
                markdown = f"# {title}\n\n{resp.text.strip()}\n"
                out_path.write_text(markdown, encoding="utf-8")
                result.written += 1
                result.digest_files.append(str(out_path))
                logger.info("[%d/%d] Wrote: %s", i + 1, len(to_process), out_path.name)
            except Exception as exc:
                result.errors.append(f"{title}: {exc}")
                logger.warning("[%d/%d] Failed: %s — %s", i + 1, len(to_process), title, exc)

        return result

    def _group_into_chapters(
        self, doc: Document,
    ) -> list[tuple[str, str]]:
        """Group document sections into chapters using PDF TOC.

        Strategy:
        1. If the source is a PDF, extract TOC via PyMuPDF for exact
           chapter boundaries (page numbers).
        2. Fall back to regex heading detection if no TOC.
        3. Fall back to fixed-size page groups as last resort.
        """
        import re

        sections = doc.sections or []
        if not sections:
            chunks = self._store.get_chunks(doc.id)
            if chunks:
                return [(c.section_title or f"Section {c.chunk_index + 1}", c.content or "") for c in chunks]
            if doc.content:
                return [("Full Document", doc.content)]
            return []

        # Try PDF TOC first
        source_path = doc.source.file_path if doc.source else ""
        if source_path and Path(source_path).is_file() and source_path.lower().endswith(".pdf"):
            toc_chapters = self._chapters_from_toc(source_path, sections)
            if toc_chapters:
                logger.info("Detected %d chapters from PDF TOC", len(toc_chapters))
                return toc_chapters

        # Fallback: regex chapter detection on content
        chapters = self._chapters_from_content(sections)
        if chapters and len(chapters) > 1:
            logger.info("Detected %d chapters from content headings", len(chapters))
            return chapters

        # Last resort: group by ~80 pages
        chapters = []
        pages_per_group = 80
        for i in range(0, len(sections), pages_per_group):
            batch = sections[i:i + pages_per_group]
            batch_content = "\n\n".join(s.content for s in batch if s.content)
            if batch_content.strip():
                chapters.append((
                    f"Pages {i + 1}-{min(i + pages_per_group, len(sections))}",
                    batch_content,
                ))
        logger.info("Grouped %d sections into %d page-range chapters", len(sections), len(chapters))
        return chapters

    @staticmethod
    def _chapters_from_toc(
        pdf_path: str, sections: list,
    ) -> list[tuple[str, str]]:
        """Extract chapters from PDF Table of Contents.

        Uses PyMuPDF to read the TOC, then maps TOC entries to document
        sections by page number. Also extracts images from each chapter's
        page range and saves them alongside the chapter text.
        """
        try:
            import fitz
            pdf_doc = fitz.open(pdf_path)
            toc = pdf_doc.get_toc()
        except Exception:
            return []

        if not toc:
            return []

        # Build list of chapter entries: (title, start_page)
        chapter_entries: list[tuple[str, int]] = []
        for level, title, page in toc:
            if level <= 2:
                chapter_entries.append((title.strip(), page))

        if not chapter_entries:
            pdf_doc.close()
            return []

        # Build page_number → section content lookup
        page_content: dict[int, str] = {}
        for sec in sections:
            page_num = sec.metadata.get("page_number", 0) if sec.metadata else 0
            if page_num and sec.content:
                page_content[page_num] = sec.content

        # Group sections by chapter boundaries + extract images
        chapters: list[tuple[str, str]] = []
        for i, (title, start_page) in enumerate(chapter_entries):
            if i + 1 < len(chapter_entries):
                end_page = chapter_entries[i + 1][1]
            else:
                end_page = len(pdf_doc) + 1

            # Collect text
            parts: list[str] = []
            for pg in range(start_page, end_page):
                content = page_content.get(pg, "")
                if content.strip():
                    parts.append(content)

            if not parts:
                continue

            # Extract images from this chapter's page range
            chapter_slug = _slugify(title) or f"chapter-{len(chapters) + 1}"
            img_dir = Path("digest") / "images" / chapter_slug
            image_refs: list[str] = []
            img_count = 0

            for pg_num in range(start_page - 1, min(end_page - 1, len(pdf_doc))):
                try:
                    page = pdf_doc[pg_num]
                    page_area = page.rect.width * page.rect.height
                    images = page.get_images(full=True)

                    for img_tuple in images:
                        xref = img_tuple[0]
                        width = img_tuple[2]
                        height = img_tuple[3]

                        # Skip tiny images (icons, bullets)
                        if width < 50 or height < 50:
                            continue
                        # Skip 1x1 placeholder images
                        if width <= 1 or height <= 1:
                            continue

                        try:
                            img_data = pdf_doc.extract_image(xref)
                            img_bytes = img_data["image"]
                            ext = img_data.get("ext", "png")

                            # Skip very small files (likely decorations)
                            if len(img_bytes) < 500:
                                continue

                            img_dir.mkdir(parents=True, exist_ok=True)
                            img_count += 1
                            img_name = f"p{pg_num + 1}_img{img_count}.{ext}"
                            img_path = img_dir / img_name
                            img_path.write_bytes(img_bytes)

                            # Find caption near the image
                            caption = f"Figure (page {pg_num + 1})"
                            image_refs.append(
                                f"\n![{caption}](images/{chapter_slug}/{img_name})\n"
                            )
                        except Exception:
                            continue
                except Exception:
                    continue

            # Build chapter content with image references interspersed
            chapter_text = "\n\n".join(parts)
            if image_refs:
                # Append images at the end of the chapter
                chapter_text += "\n\n## Figures\n" + "\n".join(image_refs)

            chapters.append((title, chapter_text))

        pdf_doc.close()
        return chapters

        return chapters

    @staticmethod
    def _chapters_from_content(sections: list) -> list[tuple[str, str]]:
        """Detect chapters from content headings (fallback when no TOC)."""
        import re
        chapter_re = re.compile(
            r'^(?:Chapter|CHAPTER)\s+(\d+)\s*\n\s*(.*)',
            re.MULTILINE,
        )

        chapters: list[tuple[str, str]] = []
        current_title = ""
        current_chapter_num = ""
        current_parts: list[str] = []

        for sec in sections:
            content = sec.content or ""
            if not content.strip():
                continue

            head = content[:300]
            match = chapter_re.search(head)

            if match:
                num = match.group(1)
                if num != current_chapter_num:
                    if current_parts:
                        chapters.append((
                            current_title or f"Chapter {len(chapters) + 1}",
                            "\n\n".join(current_parts),
                        ))
                        current_parts = []
                    current_chapter_num = num
                    name = match.group(2).strip().split("\n")[0].strip()
                    name = re.sub(r'\s{2,}.*', '', name)
                    current_title = f"Chapter {num}: {name}" if name else f"Chapter {num}"

            if not current_title:
                current_title = sec.title or f"Section {len(chapters) + 1}"

            current_parts.append(content)

        if current_parts:
            chapters.append((
                current_title or f"Chapter {len(chapters) + 1}",
                "\n\n".join(current_parts),
            ))

        return chapters

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
