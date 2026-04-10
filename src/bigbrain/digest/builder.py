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


def _extract_chapter_images(
    pdf_path: str, start_page: int, end_page: int,
    chapter_slug: str, total_pages: int, output_dir: str = "digest",
) -> list[str]:
    """Extract raster images + render vector figure pages as PNG.

    Images saved inside the chapter folder: digest/<doc>/<chapter>/images/
    Returns list of markdown image references (relative paths).
    """
    import fitz
    doc = fitz.open(pdf_path)
    img_dir = Path(output_dir) / chapter_slug / "images"
    img_refs: list[str] = []
    img_count = 0

    for pg_idx in range(start_page - 1, min(end_page - 1, total_pages)):
        try:
            page = doc[pg_idx]

            # Raster images
            for img_tuple in page.get_images(full=True):
                xref, width, height = img_tuple[0], img_tuple[2], img_tuple[3]
                if width < 50 or height < 50 or width <= 1 or height <= 1:
                    continue
                try:
                    img_data = doc.extract_image(xref)
                    if len(img_data["image"]) < 500:
                        continue
                    img_dir.mkdir(parents=True, exist_ok=True)
                    img_count += 1
                    ext = img_data.get("ext", "png")
                    img_name = f"p{pg_idx + 1}_img{img_count}.{ext}"
                    (img_dir / img_name).write_bytes(img_data["image"])
                    img_refs.append(f"![Figure (page {pg_idx + 1})](images/{img_name})")
                except Exception:
                    continue
        except Exception:
            continue

    doc.close()
    return img_refs


def _process_one_chapter(args: tuple) -> tuple[str, str]:
    """Process a single chapter: extract markdown + images. Thread-safe."""
    pdf_path, title, start_page, end_page, total_pages, idx, output_dir = args

    content = _extract_structured_markdown(
        pdf_path, start_page, end_page, chapter_title=title,
    )

    if not content.strip():
        return (title, "")

    chapter_slug = _slugify(title) or f"chapter-{idx + 1}"
    img_refs = _extract_chapter_images(
        pdf_path, start_page, end_page, chapter_slug, total_pages,
        output_dir=output_dir,
    )

    if img_refs:
        content += "\n\n## Figures\n\n" + "\n\n".join(img_refs)

    return (title, content)


def _slugify(text: str) -> str:
    """Convert a title to a filesystem-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:80]


def _extract_structured_markdown(pdf_path: str, start_page: int, end_page: int, chapter_title: str = "") -> str:
    """Extract structured markdown from PDF pages using font-size detection.

    Uses PyMuPDF get_text("dict") to detect headings (large/bold font),
    code blocks (monospace font), bold/italic terms, and paragraph breaks.
    ~500 pages/sec — only marginally slower than raw get_text("text").
    """
    import fitz

    doc = fitz.open(pdf_path)
    out: list[str] = []

    if chapter_title:
        out.append(f"# {chapter_title}")
        out.append("")

    # Track font stats for this chapter to detect heading thresholds
    body_size = 0.0
    chapter_num = re.match(r'^(\d+)\s', chapter_title or "")
    chapter_num_str = chapter_num.group(1) if chapter_num else ""
    chapter_name = re.sub(r'^\d+\s*', '', chapter_title).strip() if chapter_title else ""

    para_lines: list[str] = []

    def flush_para():
        if para_lines:
            text = " ".join(para_lines)
            out.append(text)
            out.append("")
            para_lines.clear()

    for pg_idx in range(start_page - 1, min(end_page - 1, len(doc))):
        page = doc[pg_idx]
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                spans = line["spans"]
                if not spans:
                    continue

                # Get dominant font properties for this line
                line_text = "".join(s["text"] for s in spans).strip()
                if not line_text:
                    continue

                # Skip bare page numbers
                if re.match(r'^\d{1,4}$', line_text):
                    continue

                # Skip running headers
                if line_text.startswith("Chapter ") and chapter_num_str:
                    if re.match(rf'^Chapter\s+{re.escape(chapter_num_str)}$', line_text):
                        continue
                if chapter_name and line_text == chapter_name:
                    continue

                # Analyze font properties of first significant span
                main_span = max(spans, key=lambda s: len(s["text"]))
                font_size = main_span["size"]
                font_name = main_span["font"]
                is_bold = bool(main_span["flags"] & 16)
                is_italic = bool(main_span["flags"] & 2)
                is_mono = any(m in font_name for m in ("Mono", "Courier", "Consolas", "mono"))

                # Detect body text size (most common)
                if not body_size and font_size < 14 and len(line_text) > 40:
                    body_size = font_size

                # Chapter title (>16pt bold) — skip since we add # heading
                if font_size > 16 and is_bold:
                    continue

                # Section heading (>11pt bold, e.g., "15.1 Rod cutting")
                if font_size > 11 and is_bold and len(line_text) < 80:
                    flush_para()
                    # Check if it's a numbered section
                    sec_match = re.match(r'^(\d+\.\d+(?:\.\d+)?)\s*(.*)', line_text)
                    if sec_match:
                        out.append(f"## {sec_match.group(1)} {sec_match.group(2)}")
                    else:
                        out.append(f"## {line_text}")
                    out.append("")
                    continue

                # Monospace font → code block
                if is_mono and len(line_text) > 3:
                    flush_para()
                    # Collect consecutive mono lines
                    out.append(f"`{line_text}`")
                    continue

                # Theorem/Lemma detection
                if re.match(r'^(Theorem|Lemma|Corollary|Definition)\s+[\d.]+', line_text):
                    flush_para()
                    out.append(f"> **{line_text}**")
                    out.append("")
                    continue

                # Bold+italic key terms inline
                if is_bold and is_italic and len(line_text) < 40:
                    para_lines.append(f"***{line_text}***")
                    continue
                elif is_bold and len(line_text) < 40 and font_size <= 11:
                    para_lines.append(f"**{line_text}**")
                    continue

                # Regular body text — accumulate into paragraph
                # Join hyphenated line breaks
                if para_lines and para_lines[-1].endswith("-"):
                    last = para_lines[-1][:-1]
                    para_lines[-1] = last + line_text
                else:
                    para_lines.append(line_text)

                # Detect paragraph break: sentence ends
                if line_text.endswith('.') or line_text.endswith(':') or line_text.endswith('?'):
                    flush_para()

    flush_para()
    doc.close()

    result = "\n".join(out)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip() + "\n"


def _format_raw_text(text: str, chapter_title: str = "") -> str:
    """Fallback: convert raw PDF text into markdown using regex heuristics.

    PDF text has NO paragraph breaks — every line is a single \\n.
    Paragraphs are detected by: line ends with sentence-ending punctuation
    AND the next line starts with a capital letter or is a structural element.
    """
    # Step 1: Join hyphenated words at line breaks
    text = re.sub(r'([a-z])-\n\s*([a-z])', r'\1\2', text)

    # Build chapter info for header stripping
    chapter_num_match = re.match(r'^(\d+)\s', chapter_title or "")
    chapter_num = chapter_num_match.group(1) if chapter_num_match else ""
    chapter_name = re.sub(r'^\d+\s*', '', chapter_title).strip() if chapter_title else ""

    lines = text.split("\n")

    # Step 2: Filter out noise (page numbers, running headers)
    page_num_re = re.compile(r'^\d{1,4}$')
    running_header_re = re.compile(r'^Chapter\s+\d+$')

    filtered: list[str] = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()

        # Skip bare page numbers
        if page_num_re.match(s):
            i += 1
            continue
        # Skip running header "Chapter N"
        if running_header_re.match(s):
            i += 1
            if i < len(lines) and chapter_name and lines[i].strip() == chapter_name:
                i += 1
            continue
        # Skip standalone chapter title repetition
        if chapter_name and s == chapter_name:
            i += 1
            continue
        # Skip bare chapter number
        if chapter_num and s == chapter_num and i < 5:
            i += 1
            continue

        if s:
            filtered.append(s)
        else:
            filtered.append("")
        i += 1

    # Step 3: Detect structure and group into paragraphs
    section_num_re = re.compile(r'^(\d+\.\d+(?:\.\d+)?)\s*$')
    section_inline_re = re.compile(r'^(\d+\.\d+(?:\.\d+)?)\s{1,4}([A-Z].*)')
    theorem_re = re.compile(r'^(Theorem|Lemma|Corollary|Definition|Property)\s+[\d.]+')
    procedure_re = re.compile(r'^([A-Z][A-Z-]{2,})\s*\(')
    exercise_re = re.compile(r'^(Exercises|Problems)\s*$')

    out: list[str] = []
    if chapter_title:
        out.append(f"# {chapter_title}")
        out.append("")

    para_lines: list[str] = []

    def flush_para():
        if para_lines:
            out.append(" ".join(para_lines))
            out.append("")
            para_lines.clear()

    i = 0
    while i < len(filtered):
        line = filtered[i]

        if not line:
            flush_para()
            i += 1
            continue

        # Section number on its own line
        m = section_num_re.match(line)
        if m and i + 1 < len(filtered) and filtered[i + 1] and filtered[i + 1][0].isupper():
            flush_para()
            out.append(f"## {m.group(1)} {filtered[i + 1]}")
            out.append("")
            i += 2
            continue

        # Inline section heading
        m = section_inline_re.match(line)
        if m:
            flush_para()
            out.append(f"## {m.group(1)} {m.group(2)}")
            out.append("")
            i += 1
            continue

        # Theorem / Lemma
        if theorem_re.match(line):
            flush_para()
            out.append(f"> **{line}**")
            out.append("")
            i += 1
            continue

        # Procedure (pseudocode)
        if procedure_re.match(line):
            flush_para()
            out.append("```")
            while i < len(filtered) and filtered[i]:
                out.append(filtered[i])
                i += 1
                # End code block at blank line or next paragraph start
                if i < len(filtered) and (not filtered[i] or (filtered[i][0].isupper() and len(filtered[i]) > 60)):
                    break
            out.append("```")
            out.append("")
            continue

        # Exercise heading
        if exercise_re.match(line):
            flush_para()
            out.append(f"## {line}")
            out.append("")
            i += 1
            continue

        # Regular line — accumulate into paragraph
        para_lines.append(line)

        # Detect paragraph break: sentence ends AND next line starts new thought
        if (line.endswith('.') or line.endswith(':') or line.endswith('?') or line.endswith('!')) \
                and i + 1 < len(filtered) and filtered[i + 1]:
            next_line = filtered[i + 1]
            # New paragraph if next line starts with capital and isn't a continuation
            if next_line[0].isupper() and not next_line[0:2] in ('We', 'Th', 'It', 'In', 'An', 'As', 'If', 'By', 'On', 'No', 'So', 'To'):
                flush_para()

        i += 1

    flush_para()

    result = "\n".join(out)
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
        """Extract chapters as structured markdown — zero API calls.

        Uses pymupdf4llm for rich markdown (headings, bold, lists) when
        available, falls back to basic text formatting otherwise.
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
            chapter_dir = out_dir / slug
            chapter_dir.mkdir(parents=True, exist_ok=True)
            out_path = chapter_dir / "index.md"

            if out_path.exists() and not force:
                result.skipped += 1
                result.digest_files.append(str(out_path))
                continue

            # Content from _extract_structured_markdown is already formatted
            if not content.startswith("# "):
                markdown = f"# {title}\n\n{content.strip()}\n"
            else:
                markdown = content.strip() + "\n"

            out_path.write_text(markdown, encoding="utf-8")
            result.written += 1
            result.digest_files.append(str(out_path))
            logger.info("Wrote: %s (%d chars)", f"{slug}/index.md", len(markdown))

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
            toc_chapters = self._chapters_from_toc(
                source_path, sections, output_dir=str(self._output_dir / _slugify(doc.title)),
            )
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
        pdf_path: str, sections: list, output_dir: str = "digest",
    ) -> list[tuple[str, str]]:
        """Extract chapters using PDF TOC + get_text('dict') for font-based structure.

        Uses PyMuPDF's font size/bold detection to produce structured markdown
        with proper headings, bold terms, code blocks — no AI, ~500 pages/sec.
        """
        try:
            import fitz
            pdf_doc = fitz.open(pdf_path)
            toc = pdf_doc.get_toc()
        except Exception:
            return []

        if not toc:
            pdf_doc.close()
            return []

        chapter_entries: list[tuple[str, int]] = []
        for level, title, page in toc:
            if level <= 2:
                chapter_entries.append((title.strip(), page))

        if not chapter_entries:
            pdf_doc.close()
            return []

        total_pages = len(pdf_doc)
        pdf_doc.close()

        # Build work items for parallel processing
        work_items: list[tuple] = []
        for i, (title, start_page) in enumerate(chapter_entries):
            end_page = chapter_entries[i + 1][1] if i + 1 < len(chapter_entries) else total_pages + 1
            work_items.append((pdf_path, title, start_page, end_page, total_pages, i, output_dir))

        # Process chapters in parallel (each opens its own PDF handle)
        from concurrent.futures import ThreadPoolExecutor
        import os
        workers = min(os.cpu_count() or 4, len(work_items), 8)

        chapters: list[tuple[str, str]] = []
        with ThreadPoolExecutor(max_workers=workers) as pool:
            results = pool.map(_process_one_chapter, work_items)
            for title, content in results:
                if content.strip():
                    chapters.append((title, content))

        logger.info("Extracted %d chapters using %d threads", len(chapters), workers)
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
