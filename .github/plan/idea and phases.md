# BigBrain Roadmap

## 1. Product Vision

BigBrain is a **knowledge compiler**: it ingests content from multiple sources, normalizes and distills that content into a canonical knowledge base, and compiles it into formats that are easier to browse, study, search, and reuse.

### Target inputs
- Local files: PDF, TXT, Markdown, Python/source files
- Extended file support: DOCX, PowerPoint
- Knowledge tools: Notion, Obsidian
- Web content: seed URL + controlled crawl depth

### Target outputs
- Consolidated Markdown knowledge packs
- Distilled summaries
- Cheatsheets
- Flashcards
- Q&A sets
- Podcast scripts and optional audio
- Searchable knowledge base artifacts

---

## 2. Current Starting Point

The repository is currently a **minimal Python CLI script**:
- entry point: `main.py`
- packaging: `pyproject.toml`
- Python version: `>=3.10`
- no dependencies yet
- no test suite yet

That means the roadmap should start with **foundation work first**, then move into ingestion, storage, distillation, and output generation.

---

## 3. Recommended Delivery Strategy

### Confirmed product decisions
- **Deployment/runtime strategy:** Option B - **hybrid**
- **Primary AI integration:** **GitHub Copilot Enterprise** comes first
- **Required local model support:** **Ollama** and **LM Studio** must also be supported
- **Authentication:** **GitHub authentication is mandatory on first run**
- **Provider selection:** use **automatic fallback** based on availability/capability, with an optional configured default/override
- **Top-priority MVP inputs:** **PDF + Markdown + TXT**
- **Initial source-code scope:** **Python only first**
- **Knowledge store baseline:** **JSON/JSONL + SQLite early**
- **Routing policy:** **no forced local-only providers in MVP**
- **MVP output priority:** **distilled summaries first**, then **external sync**
- **MVP external sync scope:** **Notion bidirectional sync for pages only**
- **Web crawling:** **same-domain-only by default**, but configurable

### Recommended MVP order
1. CLI foundation and project structure
2. Local file ingestion (`.txt`, `.md`, `.pdf`, `.py`)
3. Canonical knowledge store (`JSON/JSONL` + early `SQLite`)
4. AI provider layer (`GitHub Copilot Enterprise` first, `Ollama`/`LM Studio` required)
5. Distillation pipeline with summary-first flows
6. External sync integrations
7. Search + incremental updates
8. Extended ingestion and advanced outputs (`.docx`, `.pptx`, web, study outputs)

### Why this order
- It matches the current state of the repo.
- It prioritizes the highest-value user outcome: summaries.
- It supports a hybrid runtime instead of forcing cloud-only or offline-only behavior.
- It creates a stable schema before adding more input/output adapters.
- It keeps external sync important, but behind a usable summary-generation core.

---

## 4. Target Architecture

```text
main.py / CLI
    |
    +-- orchestrator/
    |     +-- pipeline.py
    |
    +-- ingest/
    |     +-- pdf_ingester.py
    |     +-- docx_ingester.py
    |     +-- text_ingester.py
    |     +-- ppt_ingester.py
    |     +-- notion_ingester.py
    |     +-- obsidian_ingester.py
    |     +-- web_crawler.py
    |
    +-- kb/
    |     +-- models.py
    |     +-- store.py
    |     +-- index.py
    |
    +-- distill/
    |     +-- chunker.py
    |     +-- normalizer.py
    |     +-- summarizer.py
    |     +-- entity_extractor.py
    |     +-- relationship_builder.py
    |
    +-- compile/
          +-- markdown_compiler.py
          +-- cheatsheet_compiler.py
          +-- flashcard_compiler.py
          +-- qa_compiler.py
          +-- notion_compiler.py
          +-- podcast_script_compiler.py
          +-- podcast_audio.py
```

### Core layers
- **Ingest**: read source material into a common `Document` model
- **Distill**: chunk, normalize, summarize, extract entities, build relationships
- **KB Store**: persist documents, chunks, entities, metadata, and provenance
- **Compile**: render reusable outputs from stored/distilled content
- **Orchestrator**: manage end-to-end workflows and incremental processing

---

## 5. Cross-Cutting Product Rules

These should apply across all phases:

1. **Hybrid runtime with local execution support**
   - GitHub authentication is required on first run, after which supported jobs can run through GitHub Copilot Enterprise, Ollama, or LM Studio depending on routing and availability.

2. **Strong provenance**
   - Every output should track where each fact came from.

3. **Structured schemas early**
   - Define stable dataclasses / models before adding many connectors.

4. **Incremental processing**
   - Re-process only changed inputs where possible.

5. **Configurable AI behavior**
   - Keep extractive and abstractive modes configurable, and route requests through a provider abstraction that supports GitHub Copilot Enterprise, Ollama, and LM Studio.

6. **Provider-aware execution**
   - Distillation and compilation flows must support an optional configured default/override plus automatic fallback based on availability and capability, while still recording which provider actually handled each step.

7. **No forced local-only routing in MVP**
   - In the MVP, no source type or command is hard-pinned to local-only providers; local providers remain available through preference, fallback, or manual selection.

8. **Mandatory authenticated startup**
   - First-run setup must establish GitHub authentication before the product is considered fully initialized.

9. **Testability first**
   - Each ingester/compiler should have fixture-driven tests.

10. **Graceful degradation**
   - Optional features like OCR, Notion, or audio should fail clearly, not crash the whole pipeline.

---

## 6. Phase Summary

| Phase | Goal | Main Output | Priority |
|---|---|---|---|
| 0 | Foundation and project skeleton | Runnable CLI + package structure | 🔴 Critical |
| 1 | Core local ingestion | `Document` objects from TXT/Markdown/PDF/Python files | 🔴 Critical |
| 2 | Canonical KB store | Persistent JSON/JSONL + SQLite store | 🔴 Critical |
| 3 | AI provider layer | Copilot Enterprise + Ollama + LM Studio runtime support | 🔴 Critical |
| 4 | Distillation pipeline | Summary-first distillation, chunks, entities, links | 🔴 Critical |
| 5 | Summary compilation MVP | Consolidated summaries + Markdown output | 🔴 Critical |
| 6 | External sync integrations | Notion bidirectional page sync | 🟠 High |
| 7 | Search and incremental updates | Query + faster reruns | 🟠 High |
| 8 | Extended ingestion and study outputs | PPT, OCR, web, cheatsheets, flashcards, Q&A | 🟡 Medium |
| 9 | Audio and rich UX | Podcast scripts/audio, dashboard | 🟢 Future |
| 10 | Hardening and release readiness | tests, docs, packaging, versioning | 🔴 Critical |

---

## 7. Detailed Roadmap

## Phase 0 - Foundation and CLI

### Goal
Turn the repository from a single script into a structured, extensible CLI application.

### Detailed task list
- See `./phase-0-implementation-task-list.md` for the implementation-ready breakdown of Phase 0 work.

### Deliverables
- Create `src/` package layout
- Keep `main.py` as a thin entry point
- Add CLI command groups:
  - `ingest`
  - `distill`
  - `compile`
  - `update`
  - `status`
  - `kb-search`
- Add logging and error handling
- Add config loading from YAML + environment variables
- Add `README.md`
- Add sample config files

### Suggested files
```text
src/
├── bigbrain/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── logging_config.py
│   ├── orchestrator/
│   ├── ingest/
│   ├── kb/
│   ├── distill/
│   └── compile/
main.py
```

### Success criteria
- `python main.py --help` works
- CLI subcommands are discoverable
- config/env override pattern is established
- logging is consistent across modules

---

## Phase 1 - Core Local Ingestion MVP

### Goal
Support the highest-value local inputs first.

### Detailed task list
- See `./phase-1-implementation-task-list.md` for the implementation-ready breakdown of Phase 1 work.

### Scope
#### 1A. TXT / Markdown ingestion
- parse plain text files
- preserve Markdown headings
- preserve internal links where possible
- attach metadata: file path, modified time, source type

#### 1B. PDF ingestion
- extract machine-readable text
- preserve page boundaries
- retain document metadata where available

#### 1C. Source code / `.py` ingestion
- ingest Python files as structured text sources
- preserve code fences in downstream Markdown output
- optionally extract docstrings and top-level symbols

### Success criteria
- TXT, Markdown, PDF, and Python files convert to a common `Document` schema
- folder ingestion works recursively
- unsupported files are skipped with warnings

---

## Phase 2 - Canonical Knowledge Store

### Goal
Persist normalized content in a way that all downstream phases can reuse.

### Detailed task list
- See `./phase-2-implementation-task-list.md` for the implementation-ready breakdown of Phase 2 work.

### Deliverables
- `Document`, `Chunk`, `Entity`, `Relationship`, `CompilationArtifact` schemas
- JSON/JSONL persistence
- SQLite support for local indexing/querying from the start
- append + merge behavior
- provenance tracking per chunk
- stable IDs and timestamps
- index metadata for fast lookup

### Success criteria
- store survives across runs
- content can be loaded back without loss of core metadata
- JSON/JSONL remains the canonical interchange format while SQLite is available for local querying
- downstream phases consume the store, not raw files directly

---

## Phase 3 - AI Provider Layer

### Goal
Introduce the runtime AI abstraction that powers distillation and compilation.

### Detailed task list
- See `./phase-3-implementation-task-list.md` for the implementation-ready breakdown of Phase 3 work.

### Provider priorities
1. **GitHub Copilot Enterprise** - first priority
2. **Ollama** - required local provider
3. **LM Studio** - required local provider

### Deliverables
- provider abstraction/interface
- provider-specific adapters
- mandatory first-run GitHub auth/config strategy
- local endpoint configuration for Ollama and LM Studio
- provider capability metadata (summary, extraction, long-context, etc.)
- configured default/override support plus automatic fallback and retry policy
- audit/provenance metadata showing which provider generated which output

### Success criteria
- distillation/compilation can execute through Copilot Enterprise
- the same flows can be executed through Ollama or LM Studio
- optional configured provider preferences are honored when possible
- automatic fallback works when a preferred provider is unavailable or unsuitable
- no source or command is forced to local-only providers in MVP
- provider choice is visible in outputs and logs

---

## Phase 4 - Distillation Pipeline

### Goal
Transform raw documents into reusable knowledge units.

### Detailed task list
- See `./phase-4-implementation-task-list.md` for the implementation-ready breakdown of Phase 4 work.

### Modes
- **Extractive**: quote and organize important source passages
- **Abstractive**: generate rewritten summaries and synthesis
- **Both**: produce both side-by-side

### Deliverables
- chunking strategy
- normalization rules
- **summary-first** summarization pipeline
- entity extraction
- relationship discovery
- confidence scores
- provider-aware execution built on the Phase 3 abstraction

### Config example
```yaml
distillation:
  mode: both
  chunk_size: 500
  overlap: 100
  summary_ratio: 0.3
  entity_confidence_min: 0.7
```

### 4B. Vision-based figure and diagram understanding
- detect pages or regions with figures, diagrams, charts, or tables
- render figure regions as images using PyMuPDF page-to-image
- send rendered images to a vision-capable AI provider for description
- store figure descriptions as `DocumentSection` entries or metadata
- support captioned and uncaptioned figures
- fall back gracefully when no vision provider is available

### 4C. Math-aware content extraction
- detect pages with heavy mathematical notation, pseudocode, or formulas
- use AI providers to re-interpret garbled math symbols into readable LaTeX or plain text
- preserve equation boundaries and numbering where possible
- store corrected math content alongside raw extraction for traceability

### Success criteria
- summaries are the first polished user-facing artifact
- summaries are generated deterministically where possible
- entities and relationships are attached to KB objects
- outputs remain traceable to source chunks
- figures and diagrams are described in text form when a vision provider is available
- math-heavy pages produce readable output rather than symbol debris

---

## Phase 5 - Summary Compilation MVP

### Goal
Produce the first end-user-friendly output format with summaries first.

### Detailed task list
- See `./phase-5-implementation-task-list.md` for the implementation-ready breakdown of Phase 5 work.

### Deliverables
- compiled summary documents by topic
- nested Markdown by topic
- merged Markdown output for a collection/folder
- source attribution inline or in footnotes
- timestamps and contributing-source sections
- code block preservation for technical content

### CLI examples
```powershell
python .\main.py ingest md --folder .\docs\ --recursive
python .\main.py ingest pdf --folder .\pdfs\ --recursive
python .\main.py distill --config .\config\distill_config.yaml
python .\main.py compile md --merge
```

### Success criteria
- duplicate topic folders are avoided
- source contributions are visible
- outputs are readable without opening raw sources
- summary output is good enough to demo before external sync ships

---

## Phase 6 - Notion Bidirectional Sync

### Goal
Publish and re-import summary-first outputs through Notion pages after the local summary workflow is solid.

### Detailed task list
- See `./phase-6-implementation-task-list.md` for the implementation-ready breakdown of Phase 6 work.

### 6A. Notion publish
- publish summaries into target Notion pages
- preserve source links and metadata
- allow sync status tracking

### 6B. Notion pull / re-ingest
- fetch previously synced Notion pages and metadata back into the KB
- track remote IDs, sync cursors, and last-updated timestamps
- support conflict detection between local and remote changes

### 6C. Sync semantics
- bidirectional sync should preserve provenance
- sync operations should be retryable and observable
- keep the design extensible for future connectors beyond Notion

### Success criteria
- summaries can be published to Notion with provenance
- Notion page changes can be synchronized back into the KB
- sync failures and conflicts are isolated, visible, and retryable

---

## Phase 7 - Search, Status, and Incremental Updates

### Goal
Make the knowledge base operable as it grows.

### Detailed task list
- See `./phase-7-implementation-task-list.md` for the implementation-ready breakdown of Phase 7 work.

### Deliverables
- input hashing / change tracking
- skip unchanged inputs
- `status` command
- `kb-search --query ...`
- simple ranking over titles, chunks, tags, and entities
- processing reports / manifests

### Success criteria
- second run is noticeably faster
- changed files trigger only impacted downstream updates
- users can search compiled knowledge locally

---

## Phase 8 - Extended Ingestion and Study Outputs

### Goal
Expand source coverage and add secondary output types after summaries and sync are working.

### Detailed task list
- See `./phase-8-implementation-task-list.md` for the implementation-ready breakdown of Phase 8 work.

### 8A. DOCX ingestion
- extract headings, paragraphs, lists, and tables
- preserve document structure as much as possible

### 8B. Obsidian ingest
- read vault Markdown files
- parse wikilinks/backlinks
- preserve frontmatter and tags
- reflect vault hierarchy in the KB

### 8C. OCR fallback for scanned PDFs
- detect low-text pages
- OCR fallback
- confidence logging
- graceful skip if OCR dependency is missing

### 8C½. High-fidelity PDF extraction (marker / nougat)
- integrate `marker-pdf` or Meta `nougat` for academic/technical PDFs
- preserve LaTeX math as `$...$` / `$$...$$` in Markdown output
- preserve pseudocode blocks with proper formatting
- detect and render figures as embedded images in output
- page-as-image rendering pipeline using PyMuPDF for visual content
- configurable: choose between fast text extraction (Phase 1 default) and high-fidelity mode
- benchmark extraction quality against Phase 1 pypdf/pymupdf baseline

### 8D. PowerPoint ingestion
- extract slide text
- speaker notes
- slide order and metadata

### 8E. Web crawling
- same-domain-only by default
- configurable depth
- robots.txt awareness
- timeout/retry handling
- dedupe visited URLs

### 8F. Cheatsheets
- dense summaries
- tables/lists
- code snippets and formulas

### 8G. Flashcards
- concept-per-card design
- Markdown + JSON export
- difficulty/topic tags

### 8H. Q&A compiler
- definition / how / why / comparison questions
- answers cite source chunks

### Success criteria
- DOCX support lands after the initial MVP ingestion slice
- Obsidian notes preserve graph relationships
- no infinite crawl loops
- OCR is optional, not mandatory
- high-fidelity PDF mode produces readable math and preserves figures
- richer source types feed the same core `Document` model
- study outputs remain secondary to summaries

### 8I. Future file types
- HTML files
- CSV/TSV for structured notes
- images with OCR metadata
- additional source code languages beyond Python

---

## Phase 9 - Audio and Rich UX

### Goal
Support richer knowledge consumption workflows.

### Detailed task list
- See `./phase-9-implementation-task-list.md` for the implementation-ready breakdown of Phase 9 work.

### 9A. Podcast script generation
- conversational scripts from compiled content
- estimated duration
- multi-speaker markup

### 9B. Podcast audio generation
- local TTS first
- optional premium provider later
- output `.mp3` / `.wav`

### 9C. UI / visualization
- browse documents/chunks/entities
- trigger pipeline runs
- inspect provenance
- visualize knowledge graph

### Success criteria
- scripts are usable before audio exists
- audio is optional and modular
- UI is layered on top of the same KB store

---

## Phase 10 - Hardening, Testing, and Release Readiness

### Goal
Make the project maintainable and safe to evolve.

### Detailed task list
- See `./phase-10-implementation-task-list.md` for the implementation-ready breakdown of Phase 10 work.

### Deliverables
- unit tests for each ingester/compiler
- fixture corpus for PDFs, DOCX, Markdown, PPT, web pages
- snapshot tests for compiled Markdown
- schema validation tests
- linting / formatting
- dependency update policy
- semantic versioning plan
- release checklist
- contributor guide
- API / module docs

### Success criteria
- confidence to refactor without breaking outputs
- reproducible behavior on sample corpora
- basic release process documented

---

## 8. Missing Items Added to the Original Plan

The original plan was strong, but these important items were missing or under-specified:

1. **Phase 0 foundation work**
   - CLI structure, config, logging, package layout

2. **DOCX ingestion**
   - Mentioned in the idea, but not broken into a phase

3. **Python/source code ingestion**
   - Mentioned in the idea, but not planned explicitly

4. **Search and query capability**
   - Needed if this becomes a usable knowledge base

5. **Testing strategy and fixtures**
   - Essential for a multi-ingester project

6. **Prompt/provider abstraction for AI work**
   - Needed before using LLM-backed distillation safely

7. **Provenance and schema design**
   - Critical for trust and debugging

8. **Operational concerns**
   - retries, timeout handling, manifests, error isolation

9. **Release readiness**
   - docs, versioning, contributor workflow, packaging quality

---

## 9. Dependency Plan by Phase

### Foundation / config
- `python-dotenv>=1.0`
- `PyYAML>=6.0`

### Ingestion
- `pypdf>=3.0` or `pdfplumber>=0.9`
- `python-pptx>=0.6.21`
- `requests>=2.31`
- `beautifulsoup4>=4.12`
- `notion-client>=2.0`

### Extended ingestion (post-MVP)
- `python-docx>=1.1`

### OCR (optional)
- `pytesseract>=0.3.10` and external Tesseract install
  - or `paddleocr>=2.7`

### AI / distillation abstraction
- provider should be abstracted; exact package depends on chosen runtime strategy

### Audio (optional)
- `pyttsx3>=2.90`

---

## 10. Suggested Milestone Plan

### Milestone A - Local MVP
- Phase 0
- Phase 1
- Phase 2
- Phase 3
- Phase 4
- Phase 5

**Outcome:** local files in, provider-backed distilled summaries + KB store out.

### Milestone B - Syncable KB
- Phase 6

**Outcome:** summary outputs can sync bidirectionally with Notion pages.

### Milestone C - Operable KB
- Phase 7
- selected testing from Phase 10

**Outcome:** searchable, incremental, repeatable local workflow.

### Milestone D - Extended Integrations and Study Outputs
- Phase 8

**Outcome:** Notion/Obsidian/web/PPT sources and study outputs join the same pipeline.

### Milestone E - Polished Platform
- Phase 9A
- Phase 9B
- Phase 9C
- remaining hardening from Phase 10

**Outcome:** richer UX and release-ready tooling.

---

## 11. AI / GitHub Integration Notes

Confirmed direction:

- GitHub Copilot Enterprise is an **in-product dependency** for distillation and compilation flows.
- BigBrain should use a **hybrid AI model strategy**.
- BigBrain must also support **local models through Ollama and LM Studio**.
- GitHub authentication is **mandatory on first run**.
- Provider selection should use **automatic fallback**, with support for an optional configured default/override.
- MVP-adjacent external sync means **Notion bidirectional page sync**.

### Architecture decision
Treat AI support as a **pluggable provider layer** with:
- **primary provider:** GitHub Copilot Enterprise
- **required local providers:** Ollama and LM Studio
- **selection policy:** optional configured default/override, then automatic fallback based on availability/capability
- **routing stance:** no source-based forced local-only routing in the MVP
- **shared abstractions:** prompts, model capabilities, auth/config, retries, provenance, fallback

### Product implications
- GitHub authentication/login is required during first-run setup.
- Runtime flows must not assume a single provider forever.
- Privacy-sensitive or offline workloads should be able to target local providers, but MVP does not require forced local-only routing rules.
- Output metadata should record which provider and model handled each step.
- Notion sync must support both outbound publishing and inbound reconciliation for pages.
- Initial source-code workflows target Python only; broader language support can be added later.

---

## 12. Finalized MVP Decisions

All major MVP direction-setting decisions are now resolved:

- deployment/runtime strategy = **hybrid**
- GitHub Copilot Enterprise = **in-product dependency**
- required local model support = **Ollama + LM Studio**
- GitHub authentication = **mandatory on first run**
- provider selection = **automatic fallback with optional configured default/override**
- top-priority MVP inputs = **PDF + Markdown + TXT**
- initial source-code scope = **Python only first**
- knowledge store = **JSON/JSONL + SQLite early**
- routing policy = **no forced local-only providers in MVP**
- first MVP output = **summaries**, then **external sync**
- external sync scope = **Notion bidirectional page sync**
- web crawling = **same-domain-only by default, but configurable**

---

## 13. Immediate Implementation Checklist

- [ ] Create `src/` package structure
- [ ] Keep `main.py` as a thin orchestrator entry point
- [ ] Add CLI parser and help text
- [ ] Add config loading (YAML + env)
- [ ] Add provider config for GitHub Copilot Enterprise, Ollama, and LM Studio
- [ ] Add first-run GitHub authentication flow
- [ ] Add `Document` / `Chunk` / `Entity` / `Relationship` schemas
- [ ] Add provider abstraction and runtime metadata/provenance schema
- [ ] Add optional provider default/override config plus automatic fallback routing across Copilot Enterprise, Ollama, and LM Studio
- [ ] Implement TXT/MD ingestion first
- [ ] Implement PDF ingestion second
- [ ] Implement Python source ingestion third
- [ ] Implement JSON/JSONL knowledge store plus early SQLite support
- [ ] Implement summary-first distillation pipeline skeleton
- [ ] Implement summary compilation MVP
- [ ] Implement Notion bidirectional page sync after summaries
- [ ] Implement DOCX ingestion in the extended-ingestion phase
- [ ] Add tests and sample fixtures
- [ ] Update `AGENTS.md` once architecture changes land
- [ ] Update `pyproject.toml` as dependencies are introduced
- [ ] Add `README.md` quick-start instructions
