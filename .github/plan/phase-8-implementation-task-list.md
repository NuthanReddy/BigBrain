# BigBrain Phase 8 Implementation Task List
<!-- PLAN:TEMPLATE v1 -->
<!-- PLAN:SOURCE .github/plan/_phase-task-template.md -->


## Goal

Implement **extended ingestion and study outputs** after the summary-first core workflow is stable.

This phase intentionally contains several feature streams that should be made as independent as possible for maximum parallelization.

---

## Parallelization Strategy

Use a two-layer approach:
1. agree on any shared extension contracts first
2. execute independent feature streams in parallel

Parallelizable streams in this phase:
- DOCX ingestion
- Obsidian ingest
- OCR fallback for scanned PDFs
- PowerPoint ingestion
- Web crawling
- Cheatsheet generation
- Flashcard generation
- Q&A generation

---

## Scope Boundaries

### In scope
- DOCX ingestion
- Obsidian ingest
- OCR fallback
- PPT ingestion
- same-domain-configurable web crawl
- cheatsheets
- flashcards
- Q&A outputs

### Out of scope
- podcast script/audio
- generic UI/dashboard
- non-Python source language ingestion

---

## Phase 1–7 Carry-Over Issues / Preconditions

- [ ] extension points exist in ingest/compile modules
- [ ] `Document` and distilled artifact models are stable
- [ ] search/status/orchestration foundation exists

### Minimum preflight acceptance criteria
- new ingesters can plug into the existing registry without redesign
- study outputs can consume distilled artifacts without redefining contracts

---

## Recommended Implementation Order

0. Close shared extension-contract blockers
1. Define shared extension contracts for new ingesters/output generators
2. Run ingestion and study-output feature streams in parallel
3. Integrate each stream into CLI and config incrementally
4. Add fixtures/docs for each stream independently

---

## Shared Workstream - Extension Contracts

### Tasks
- [ ] confirm plugin/registry extension pattern for new ingesters
- [ ] confirm output artifact contract for study outputs
- [ ] confirm config sections for extended ingestion/output modules

### Acceptance criteria
- feature teams can build independently against stable interfaces
- new streams do not require redesign of Phase 1–7 foundations

---

## Workstream A - DOCX Ingestion

### Tasks
- [ ] add DOCX dependency
- [ ] implement DOCX parsing
- [ ] preserve headings, paragraphs, lists, and tables where practical
- [ ] integrate with ingest registry and CLI

### Acceptance criteria
- DOCX files convert into the shared `Document` shape
- structure is preserved sufficiently for later distillation

---

## Workstream B - Obsidian Ingest

### Tasks
- [ ] implement vault discovery
- [ ] parse Markdown notes, wikilinks, backlinks, frontmatter, tags
- [ ] preserve vault-relative metadata
- [ ] integrate with ingest registry and CLI

### Acceptance criteria
- Obsidian vaults ingest cleanly
- wikilinks/backlinks survive as metadata/relationships

---

## Workstream C - OCR Fallback for PDFs

### Tasks
- [ ] detect low-text/image-heavy PDFs
- [ ] add OCR provider integration behind optional dependency/config
- [ ] record confidence and fallback behavior
- [ ] fail gracefully when OCR is unavailable

### Acceptance criteria
- scanned PDFs can be handled when OCR is enabled
- OCR remains optional and non-blocking

---

## Workstream D - PowerPoint Ingestion

### Tasks
- [ ] parse slide text
- [ ] parse speaker notes when available
- [ ] preserve slide ordering/metadata
- [ ] integrate with ingest registry and CLI

### Acceptance criteria
- PPT/PPTX files ingest into the shared `Document` model
- slide ordering is preserved

---

## Workstream E - Web Crawling

### Tasks
- [ ] implement seed URL crawl flow
- [ ] enforce same-domain-only by default
- [ ] allow configurability for depth and domain behavior
- [ ] respect robots/timeouts/retries
- [ ] dedupe visited URLs

### Acceptance criteria
- crawl depth and domain behavior are configurable
- default crawl behavior remains safe and bounded
- loops and duplicate visits are controlled

---

## Workstream F - Cheatsheets

### Tasks
- [ ] define cheatsheet artifact contract
- [ ] implement dense summary rendering
- [ ] support tables/lists/code snippets
- [ ] wire compile CLI surface

### Acceptance criteria
- cheatsheets are readable and scannable
- output is structurally predictable

---

## Workstream G - Flashcards

### Tasks
- [ ] define flashcard artifact contract
- [ ] generate concept-per-card outputs
- [ ] support Markdown/JSON export
- [ ] add tagging/difficulty metadata

### Acceptance criteria
- flashcards are importable and consistently structured
- one concept is not fragmented across many low-value cards unnecessarily

---

## Workstream H - Q&A Output

### Tasks
- [ ] define Q&A artifact contract
- [ ] generate multiple question types
- [ ] include answer/source attribution
- [ ] wire compile CLI surface

### Acceptance criteria
- Q&A outputs are specific, answerable, and attributable
- output is exportable in stable formats

---

## Workstream I - Docs, Fixtures, and Integration

### Tasks
- [ ] add per-stream fixtures and tests
- [ ] update docs for each new ingestion/output path
- [ ] keep each feature toggleable/configurable

### Acceptance criteria
- each stream is testable independently
- documentation makes clear which features are optional or dependency-gated

---

## Definition of Done for Phase 8

- [ ] shared extension contracts are stable
- [ ] at least one new ingestion stream and one new study-output stream can land independently
- [ ] all implemented streams integrate without breaking prior phases
- [ ] docs/tests exist per implemented stream
- [ ] the phase remains modular enough for parallel team execution

---

## Recommended First Commit Slice

### Slice 0
- extension contracts and config scaffolding

### Slice 1
- parallel ingestion streams (DOCX / Obsidian / PPT / web / OCR)

### Slice 2
- parallel study-output streams (cheatsheets / flashcards / Q&A)

### Slice 3
- CLI/docs/tests/integration polish per stream

