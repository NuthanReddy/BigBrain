# AGENTS Guide

## Project Snapshot
- **BigBrain** is a structured Python CLI application for ingesting, distilling, and compiling knowledge from multiple sources.
- Package layout: `src/bigbrain/` with subpackages for each pipeline stage.
- Runtime entry point is `main.py` (thin wrapper that calls `bigbrain.cli.main()`).
- Packaging metadata lives in `pyproject.toml` (`[project]` with Python `>=3.10`).
- Console script: `bigbrain` (via `pyproject.toml` `[project.scripts]`).
- Dependency: `pyyaml>=6.0` for config loading, `httpx>=0.27` for AI provider APIs, `pymupdf>=1.23` and `pypdf>=3.0` for PDF ingestion.

## Architecture and Flow

### Call Chain
1. `main.py` → `bigbrain.cli.main()` → argparse dispatch → subcommand handlers.
2. Startup sequence: `setup_logging()` → parse args → subcommand handler calls `load_config()` as needed → run subcommand.

### Key Modules
| Module | Responsibility |
|---|---|
| `bigbrain.cli` | Argparse-based CLI with subcommand dispatch |
| `bigbrain.config` | `load_config()` – loads YAML config with `BIGBRAIN_*` env var overrides; returns `BigBrainConfig` dataclass |
| `bigbrain.logging_config` | `setup_logging()` – called once at startup; `get_logger(__name__)` for per-module loggers |
| `bigbrain.errors` | `UserError` → `IngestionError` → `UnsupportedFormatError`, `FileAccessError`; `ConfigError`; `ProviderError` → `NoProviderAvailableError` |
| `bigbrain.kb.models` | `Document`, `SourceMetadata`, `DocumentSection`, `IngestionResult` data models |
| `bigbrain.kb.store` | `KBStore` – SQLite CRUD, FTS5 search, JSONL export/import, ingestion run tracking |
| `bigbrain.kb.service` | `KBService` – high-level API wrapping KBStore for use by later phases |
| `bigbrain.ingest.service` | `ingest_path()` – main ingestion entry point; accepts a path and returns `IngestionResult` |
| `bigbrain.ingest.registry` | `BaseIngester` ABC + extension-to-ingester registry |
| `bigbrain.ingest.discovery` | File discovery and filtering (recursive traversal, hidden-file skipping, extension filtering) |
| `bigbrain.ingest.text_ingester` | Plain-text ingester (UTF-8 with fallback encoding) |
| `bigbrain.ingest.markdown_ingester` | Markdown ingester (heading structure, internal links) |
| `bigbrain.ingest.pdf_ingester` | PDF ingester (page boundaries, metadata) |
| `bigbrain.ingest.python_ingester` | Python ingester (AST symbol extraction, docstrings) |
| `bigbrain.ingest.url_ingester` | URL/web page ingester (HTML fetch, text extraction via BeautifulSoup + html2text) |
| `bigbrain.ingest.api_ingester` | REST API JSON ingester (fetch JSON, flatten to text, json-path extraction, pagination) |
| `bigbrain.providers.base` | `BaseProvider` ABC and `ProviderResponse` dataclass for all AI providers |
| `bigbrain.providers.config` | `OllamaConfig`, `LMStudioConfig`, `GitHubCopilotConfig`, `ProviderConfig` dataclasses |
| `bigbrain.providers.registry` | `ProviderRegistry` – loads enabled providers, preferred provider routing with automatic fallback |
| `bigbrain.providers.ollama` | `OllamaProvider` – Ollama native REST API client (`/api/generate`, `/api/chat`) |
| `bigbrain.providers.lm_studio` | `LMStudioProvider` – LM Studio OpenAI-compatible client (`/v1/completions`, `/v1/chat/completions`) |
| `bigbrain.providers.github_copilot` | `GitHubCopilotProvider` – GitHub Copilot OpenAI-compatible client (`/chat/completions`, `/models`) |
| `bigbrain.providers.github_auth` | GitHub token discovery (env vars, CLI config) and authentication helpers |
| `bigbrain.notion.client` | `NotionClient` – Notion API wrapper (search, get/create pages, block CRUD) |
| `bigbrain.notion.importer` | `NotionImporter` – converts Notion blocks → KB `Document` with sections |
| `bigbrain.notion.exporter` | `NotionExporter` – exports KB docs + distilled content → Notion pages |
| `bigbrain.notion.sync` | `SyncEngine` – bidirectional sync with conflict detection and `SyncResult` tracking |
| `bigbrain.orchestrator.change_detector` | `ChangeDetector` – file change detection via mtime + content hash; `ChangeResult` with changed/new/deleted file lists |
| `bigbrain.orchestrator.pipeline` | `Orchestrator` – end-to-end update pipeline (detect changes → ingest → distill → compile); `OrchestratorResult` tracking |

### Subpackages
| Subpackage | Purpose |
|---|---|
| `bigbrain.ingest` | **Active (Phase 1, 8)** – Reads source material into a common Document model via format-specific ingesters; supports local files, URLs, and REST APIs |
| `bigbrain.kb` | **Active (Phase 2)** – Document/SourceMetadata/IngestionResult models; `KBStore` provides SQLite persistence and FTS5 search |
| `bigbrain.providers` | **Active (Phase 3)** – AI provider integration with Ollama, LM Studio, and GitHub Copilot; preferred provider routing with automatic fallback |
| `bigbrain.orchestrator` | **Active (Phase 7)** – End-to-end pipeline orchestration with file change detection and incremental processing |
| `bigbrain.distill` | Chunk, normalize, summarize, extract entities, build relationships |
| `bigbrain.compile` | Render reusable outputs from stored/distilled content |
| `bigbrain.notion` | **Active (Phase 6)** – Bidirectional sync between KB and Notion workspace; import, export, and sync engine |

### Ingestion Pipeline (Phase 1)
1. `bigbrain.cli` parses `ingest --source <path>` and calls `bigbrain.ingest.service.ingest_path()`.
2. `discovery.discover_files()` walks the path, filters by extension, skips hidden files.
3. For each discovered file, `registry.get_ingester(extension)` returns the appropriate `BaseIngester`.
4. The ingester's `.ingest(path)` method returns a `Document` with sections and metadata.
5. Results are collected into an `IngestionResult` (successes, failures, skipped counts).

### Storage Pipeline (Phase 2)
1. CLI parses `ingest --source <path>` and calls `bigbrain.ingest.service.ingest_path()` (pure, no side effects).
2. CLI persists each successfully ingested `Document` via `KBStore.save_document()` (upsert by content-hash ID).
3. CLI saves the `IngestionResult` as a run record via `KBStore.save_ingestion_run()`.
4. The `status` command reads aggregate statistics via `KBStore.get_stats()` (document count, size, type breakdown, last run).
5. `--no-store` flag skips steps 2–3, making the ingest command behave like Phase 1 (dry-run).

### Provider Pipeline (Phase 3)
1. `ProviderRegistry.from_config(config.providers)` reads the `providers:` YAML section and instantiates only enabled providers.
2. `ProviderRegistry.from_app_config()` is a convenience that calls `load_config()` automatically.
3. If `preferred_provider` is set in config, that provider is tried first before falling back to others.
4. Each provider implements `BaseProvider` ABC: `is_available()`, `complete()`, `chat()`, `summarize()`, `extract_entities()`.
5. `registry.complete(prompt)` (and other operations) use `_with_fallback()` — tries the preferred provider first (if set), then remaining providers in order; on `ProviderError`, logs a warning and tries the next.
6. `registry.health_check()` returns a dict of `provider_name → bool` for all registered providers.
7. `OllamaProvider` uses Ollama's native REST API (`/api/generate`, `/api/chat`, `/api/tags`).
8. `LMStudioProvider` uses the OpenAI-compatible API (`/v1/completions`, `/v1/chat/completions`, `/v1/models`).
9. `GitHubCopilotProvider` uses the OpenAI-compatible API at `https://api.githubcopilot.com` (`/chat/completions`, `/models`); authentication via OAuth device flow (`bigbrain auth login`).
10. `github_auth` handles token lifecycle: OAuth device flow login, token caching at `~/.bigbrain/github_token.json`, and validation (rejects classic PATs).
11. `ProviderResponse` is the common return type: `text`, `model`, `provider`, `usage` (token counts), `metadata`.

### Notion Sync Pipeline (Phase 6)
1. `bigbrain.cli` parses `notion <subcommand>` and dispatches to the appropriate handler.
2. `NotionClient.from_config(config.notion)` creates a Notion API wrapper using the configured token (config or `BIGBRAIN_NOTION_TOKEN` env var).
3. **Import**: `NotionImporter.import_pages()` searches Notion workspace → converts blocks to `Document` sections → stores via `KBStore.save_document()` → records sync mapping.
4. **Export**: `NotionExporter.export_documents()` reads KB documents → renders content as Notion blocks → creates/updates pages via `NotionClient` → records sync mapping.
5. **Sync**: `SyncEngine.sync()` compares `notion_last_edited` vs `local_last_edited` timestamps → detects conflicts → imports newer Notion pages and exports newer local docs.
6. **Status**: `notion status` checks API connectivity via `NotionClient.is_available()` and lists sync mappings from `KBStore.list_sync_mappings()`.
7. Sync mappings are stored in the `notion_sync` table (KB schema v4) with `document_id ↔ notion_page_id` tracking, direction, timestamps, and status.

### Orchestrator Pipeline (Phase 7)
1. `bigbrain.cli` parses `update --source <path>` with optional `--force`, `--steps`, and `--model` flags.
2. `ChangeDetector` scans the source path and compares file mtime + content hashes against `file_hashes` table in `KBStore` (KB schema v5).
3. `ChangeDetector.scan()` returns a `ChangeResult` listing changed, new, and deleted files.
4. `Orchestrator.run()` executes the pipeline steps in order: ingest → distill → compile, processing only changed/new files (or all files if `--force`).
5. `_run_ingest()` calls `ingest_path()` for changed files and persists results via `KBStore`, then updates `file_hashes` via `KBStore.save_file_hash()`.
6. `_run_distill()` runs the distillation pipeline on newly ingested/changed documents.
7. `_run_compile()` runs the compilation pipeline on updated content.
8. Deleted files are cleaned up: `KBStore.delete_file_hash()` removes tracking records.
9. `--steps` flag allows running a subset of the pipeline (e.g., `ingest` only, or `ingest,distill`).
10. Results are collected into an `OrchestratorResult` with per-step status and timing.

### Error Handling
- `UserError` for user-facing errors (displayed cleanly, no traceback).
- Top-level `try/except` in `main.py` catches `UserError` and prints the message.
- Unexpected exceptions propagate with full traceback for debugging.

### Config Precedence
1. `BIGBRAIN_*` environment variables (highest priority).
2. YAML config file (passed via `--config` flag or default `config/example.yaml`).
3. Hardcoded defaults in `BigBrainConfig` dataclass (lowest priority).

## Developer Workflows

### Running the CLI
```powershell
# See all commands
python main.py --help

# See subcommand help
python main.py <subcommand> --help

# Editable install (then use 'bigbrain' command directly)
pip install -e .
bigbrain --help
```

### Ingestion (Phase 1)
```powershell
# Ingest a single file
python main.py ingest --source path/to/file.md

# Ingest a directory recursively
python main.py ingest --source path/to/docs/

# Ingest only PDF files
python main.py ingest --source ./docs --type pdf
```

### Adding a New Ingester
1. Create `src/bigbrain/ingest/<format>_ingester.py`.
2. Implement a class that extends `BaseIngester` from `bigbrain.ingest.registry`.
3. Override `ingest(path) -> Document` and `supported_extensions() -> list[str]`.
4. Register the ingester in `bigbrain/ingest/registry.py` by adding it to the extension map.

### Configuration
- Example config: `config/example.yaml`
- Override any setting with `BIGBRAIN_*` environment variables.
- Config is loaded per-command (each handler calls `load_config()` internally).

### Testing
- Tests use **pytest** (`python -m pytest tests/ -v`).
- Test fixtures live in `tests/fixtures/ingest/` (sample files for each supported format).
- KB store tests use `tmp_path` for isolated databases.
- Provider tests use `unittest.mock` to mock HTTP calls (no real LLM needed).

## Project-Specific Coding Conventions
- Keep `main.py` as a thin entry point; all business logic goes in `src/bigbrain/`.
- Use `from bigbrain.logging_config import get_logger; logger = get_logger(__name__)` for logging in every module.
- Raise `UserError` for user-facing error messages (never raw `print` + `sys.exit`).
- Use `from bigbrain.errors import UserError, IngestionError` for ingestion-related errors.
- New ingesters must extend `BaseIngester` from `bigbrain.ingest.registry` and register their supported extensions.
- All ingesters return `Document` from `bigbrain.kb.models`.
- Add new CLI subcommands in `src/bigbrain/cli.py` under the argparse subparser group.
- Record new dependencies in `pyproject.toml` under `dependencies`.
- Config sections are reserved per phase; extend the `BigBrainConfig` dataclass for new settings.
- Subpackage `__init__.py` files contain docstrings describing each module's purpose.

## File Structure (Phase 8)
```
BigBrain/
├── main.py                          # Thin entry point → bigbrain.cli.main()
├── pyproject.toml                   # Package metadata, dependencies, console script
├── config/
│   └── example.yaml                 # Example YAML config with all sections
├── docs/
│   └── .gitkeep
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # sys.path setup for src/ layout
│   ├── test_config.py               # Config loading, env overrides, KBConfig, DistillConfig, CompileConfig
│   ├── test_errors.py               # Error hierarchy and messages
│   ├── test_kb_store.py             # KBStore CRUD, upsert, FTS5, JSONL, edge cases
│   ├── test_kb_service.py           # KBService integration tests
│   ├── test_providers.py            # Provider mocked HTTP tests + registry fallback + GitHub auth
│   ├── test_rag.py                  # RAG pipeline: retriever, context, prompts, pipeline
│   ├── test_distill.py              # Chunker, summarizer, entities, relationships, pipeline
│   ├── test_compile.py              # Compilers, pipeline, config
│   ├── test_notion.py               # Notion client, importer, exporter, sync, KB mappings
│   ├── test_orchestrator.py         # Change detector, orchestrator pipeline, KB file hashes
│   ├── ingest/                      # Ingestion pipeline tests
│   │   ├── test_discovery.py
│   │   ├── test_registry.py
│   │   ├── test_text_ingester.py
│   │   ├── test_markdown_ingester.py
│   │   ├── test_pdf_ingester.py
│   │   ├── test_python_ingester.py
│   │   ├── test_url_ingester.py
│   │   ├── test_api_ingester.py
│   │   └── test_service.py
│   └── fixtures/
│       └── ingest/
│           ├── sample.txt           # Plain-text fixture
│           ├── sample.md            # Markdown fixture
│           ├── sample.py            # Python fixture (symbol extraction)
│           ├── sample.pdf           # PDF fixture (2 pages, metadata)
│           ├── empty.txt            # Empty file edge case
│           ├── unsupported.xyz      # Unsupported extension fixture
│           └── nested/
│               └── deep.txt         # Recursive traversal fixture
├── src/
│   └── bigbrain/
│       ├── __init__.py              # Package root, __version__
│       ├── cli.py                   # Argparse CLI with subcommand dispatch
│       ├── config.py                # load_config(), BigBrainConfig, IngestionConfig, KBConfig, DistillConfig, CompileConfig
│       ├── logging_config.py        # setup_logging(), get_logger()
│       ├── errors.py                # UserError, IngestionError, ProviderError, etc.
│       ├── orchestrator/
│       │   ├── __init__.py          # Orchestrator exports (ChangeDetector, Orchestrator)
│       │   ├── change_detector.py   # File change detection (mtime + content hash)
│       │   └── pipeline.py          # Orchestrator – end-to-end update pipeline
│       ├── ingest/
│       │   ├── __init__.py          # Ingestion subpackage
│       │   ├── service.py           # ingest_path() – main entry point
│       │   ├── registry.py          # BaseIngester ABC + extension registry
│       │   ├── discovery.py         # File discovery and filtering
│       │   ├── text_ingester.py     # Plain-text ingester
│       │   ├── markdown_ingester.py # Markdown ingester
│       │   ├── pdf_ingester.py      # PDF ingester
│       │   ├── python_ingester.py   # Python AST ingester
│       │   ├── url_ingester.py     # URL/web page ingester (HTML → text)
│       │   └── api_ingester.py     # REST API JSON ingester
│       ├── kb/
│       │   ├── __init__.py          # Knowledge base subpackage
│       │   ├── models.py            # Document, SourceMetadata, DocumentSection, IngestionResult
│       │   ├── store.py             # KBStore – SQLite persistence, FTS5, distill tables, JSONL
│       │   └── service.py           # KBService – high-level API for later phases
│       ├── providers/
│       │   ├── __init__.py          # Provider subpackage
│       │   ├── base.py              # BaseProvider ABC, ProviderResponse dataclass
│       │   ├── config.py            # OllamaConfig, LMStudioConfig, GitHubCopilotConfig, ProviderConfig
│       │   ├── registry.py          # ProviderRegistry – preferred provider routing + fallback
│       │   ├── ollama.py            # OllamaProvider – native REST API client
│       │   ├── lm_studio.py         # LMStudioProvider – OpenAI-compatible client
│       │   ├── github_copilot.py    # GitHubCopilotProvider – with retry + rate limit handling
│       │   └── github_auth.py       # OAuth device flow, token caching, validation
│       ├── rag/
│       │   ├── __init__.py          # RAG pipeline exports
│       │   ├── retriever.py         # KB search + chunk extraction
│       │   ├── context.py           # Context assembly with char budget
│       │   ├── prompts.py           # Prompt templates (QA, summarize, explain)
│       │   └── pipeline.py          # RAGPipeline – retrieve→assemble→generate
│       ├── distill/
│       │   ├── __init__.py          # Distillation exports
│       │   ├── models.py            # Chunk, Summary, Entity, Relationship, DistillResult
│       │   ├── chunker.py           # Chunking strategies (section, sliding window, paragraph)
│       │   ├── summarizer.py        # AI-powered summarization
│       │   ├── entities.py          # AI entity extraction with dedup
│       │   ├── relationships.py     # AI relationship building
│       │   └── pipeline.py          # DistillPipeline – parallel chunk→summarize→extract→relate
│       └── compile/
│           ├── __init__.py          # Compilation exports
│           ├── models.py            # CompileOutput, Flashcard, QAPair, OutputFormat
│           ├── markdown.py          # Markdown summary renderer
│           ├── flashcard.py         # AI/template flashcard generator
│           ├── cheatsheet.py        # Entity-based cheatsheet renderer
│           ├── qa_generator.py      # AI/template Q&A pair generator
│           ├── study_guide.py       # AI/template study guide generator
│           └── pipeline.py          # CompilePipeline – format dispatch + file output
│       ├── notion/
│       │   ├── __init__.py          # Notion integration exports
│       │   ├── client.py            # NotionClient – API wrapper (search, pages, blocks)
│       │   ├── importer.py          # NotionImporter – Notion blocks → KB Documents
│       │   ├── exporter.py          # NotionExporter – KB docs → Notion pages
│       │   └── sync.py              # SyncEngine – bidirectional sync with conflict detection
└── AGENTS.md                        # This file
```

## Integration Points and Dependencies

### Current (Phase 0–8)
- **pyyaml** (`>=6.0`) – YAML config file loading.
- **sqlite3** (stdlib) – SQLite-backed knowledge base persistence with FTS5 full-text search (Phase 2).
- **httpx** (`>=0.27`) – HTTP client for AI provider APIs (Phase 3) and URL/API ingestion (Phase 8).
- **Ollama** – Local LLM inference via native REST API (Phase 3).
- **LM Studio** – Local LLM inference via OpenAI-compatible API (Phase 3).
- **GitHub Copilot** – Cloud LLM inference via OAuth device flow at `api.githubcopilot.com` (Phase 3B).
- **notion-client** (`>=2.0`) – Notion SDK for Python; page/block CRUD and search (Phase 6).
- **beautifulsoup4** – HTML parsing for URL ingestion (Phase 8).
- **html2text** – HTML-to-text conversion for URL ingestion (Phase 8).

### Future
| Phase | Integration |
|---|---|
| Phase 11 | Polyglot entity/vector store backends (PostgreSQL+pgvector, Neo4j, Qdrant, Weaviate, Pinecone) |

## Phase Roadmap

| Phase | Name | Description |
|---|---|---|
| 0 | Skeleton | Project structure, CLI, config, logging, error handling ✅ |
| 1 | Ingest | Read files (txt, md, pdf, py) into Document model ✅ |
| 2 | Knowledge Base | SQLite/JSONL storage, CRUD, FTS5 search, status ✅ |
| 3 | AI Providers | Ollama, LM Studio, GitHub Copilot with preferred routing + fallback ✅ |
| 3C | RAG Pipeline | Retrieve→assemble→generate for Q&A ✅ |
| 4 | Distill | Chunking, summarization, entity extraction, relationships ✅ |
| 5 | Compile | Markdown, flashcards, cheatsheets, Q&A, study guides ✅ |
| 6 | Notion Integration | Bidirectional sync between KB and Notion workspace ✅ |
| 7 | Orchestrator | End-to-end pipeline, incremental updates ✅ |
| 8 | Multi-source Ingestion | URL/web page ingestion and REST API JSON ingestion ✅ |
| 9 | Plugin system | Extensibility for custom ingesters/compilers |
| 10 | Production hardening | Progress bars, rich output, error recovery, performance optimization |
| 11 | Polyglot Entity Store | Pluggable distilled-entity/vector backends; keep SQLite default for local/dev |

