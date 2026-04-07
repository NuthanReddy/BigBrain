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
2. Startup sequence: parse args → `load_config()` → `setup_logging()` → run subcommand.

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
| `bigbrain.providers.base` | `BaseProvider` ABC and `ProviderResponse` dataclass for all AI providers |
| `bigbrain.providers.config` | `OllamaConfig`, `LMStudioConfig`, `GitHubCopilotConfig`, `ProviderConfig` dataclasses |
| `bigbrain.providers.registry` | `ProviderRegistry` – loads enabled providers, preferred provider routing with automatic fallback |
| `bigbrain.providers.ollama` | `OllamaProvider` – Ollama native REST API client (`/api/generate`, `/api/chat`) |
| `bigbrain.providers.lm_studio` | `LMStudioProvider` – LM Studio OpenAI-compatible client (`/v1/completions`, `/v1/chat/completions`) |
| `bigbrain.providers.github_copilot` | `GitHubCopilotProvider` – GitHub Copilot OpenAI-compatible client (`/chat/completions`, `/models`) |
| `bigbrain.providers.github_auth` | GitHub token discovery (env vars, CLI config) and authentication helpers |

### Subpackages
| Subpackage | Purpose |
|---|---|
| `bigbrain.ingest` | **Active (Phase 1)** – Reads source material into a common Document model via format-specific ingesters |
| `bigbrain.kb` | **Active (Phase 2)** – Document/SourceMetadata/IngestionResult models; `KBStore` provides SQLite persistence and FTS5 search |
| `bigbrain.providers` | **Active (Phase 3)** – AI provider integration with Ollama, LM Studio, and GitHub Copilot; preferred provider routing with automatic fallback |
| `bigbrain.orchestrator` | Manages end-to-end workflows and incremental processing |
| `bigbrain.distill` | Chunk, normalize, summarize, extract entities, build relationships |
| `bigbrain.compile` | Render reusable outputs from stored/distilled content |

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
- Pass a custom config file: `python main.py --config path/to/config.yaml`

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

## File Structure (Phase 3B)
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
│   ├── test_config.py               # Config loading, env overrides, KBConfig
│   ├── test_errors.py               # Error hierarchy and messages
│   ├── test_kb_store.py             # KBStore CRUD, upsert, FTS5, JSONL, edge cases
│   ├── test_kb_service.py           # KBService integration tests
│   ├── test_providers.py            # Provider mocked HTTP tests + registry fallback
│   ├── ingest/                      # Ingestion pipeline tests
│   │   ├── test_discovery.py
│   │   ├── test_registry.py
│   │   ├── test_text_ingester.py
│   │   ├── test_markdown_ingester.py
│   │   ├── test_pdf_ingester.py
│   │   ├── test_python_ingester.py
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
│       ├── config.py                # load_config(), BigBrainConfig dataclass
│       ├── logging_config.py        # setup_logging(), get_logger()
│       ├── errors.py                # UserError, IngestionError, UnsupportedFormatError, FileAccessError, ConfigError
│       ├── orchestrator/
│       │   └── __init__.py          # Placeholder – workflow orchestration
│       ├── ingest/
│       │   ├── __init__.py          # Ingestion subpackage
│       │   ├── service.py           # ingest_path() – main entry point
│       │   ├── registry.py          # BaseIngester ABC + extension registry
│       │   ├── discovery.py         # File discovery and filtering
│       │   ├── text_ingester.py     # Plain-text ingester
│       │   ├── markdown_ingester.py # Markdown ingester
│       │   ├── pdf_ingester.py      # PDF ingester
│       │   └── python_ingester.py   # Python AST ingester
│       ├── kb/
│       │   ├── __init__.py          # Knowledge base subpackage
│       │   ├── models.py            # Document, SourceMetadata, DocumentSection, IngestionResult
│       │   ├── store.py             # KBStore – SQLite persistence, FTS5 search, ingestion runs
│       │   └── service.py           # KBService – high-level API for later phases
│       ├── providers/
│       │   ├── __init__.py          # Provider subpackage
│       │   ├── base.py              # BaseProvider ABC, ProviderResponse dataclass
│       │   ├── config.py            # OllamaConfig, LMStudioConfig, GitHubCopilotConfig, ProviderConfig
│       │   ├── registry.py          # ProviderRegistry – preferred provider routing + fallback
│       │   ├── ollama.py            # OllamaProvider – native REST API client
│       │   ├── lm_studio.py         # LMStudioProvider – OpenAI-compatible client
│       │   ├── github_copilot.py    # GitHubCopilotProvider – OpenAI-compatible client
│       │   └── github_auth.py       # GitHub token discovery and authentication
│       ├── distill/
│       │   └── __init__.py          # Placeholder – distillation pipeline
│       └── compile/
│           └── __init__.py          # Placeholder – output compilation
└── AGENTS.md                        # This file
```

## Integration Points and Dependencies

### Current (Phase 0–3B)
- **pyyaml** (`>=6.0`) – YAML config file loading.
- **sqlite3** (stdlib) – SQLite-backed knowledge base persistence with FTS5 full-text search (Phase 2).
- **httpx** (`>=0.27`) – HTTP client for AI provider APIs (Phase 3).
- **Ollama** – Local LLM inference via native REST API (Phase 3).
- **LM Studio** – Local LLM inference via OpenAI-compatible API (Phase 3).
- **GitHub Copilot** – Cloud LLM inference via OpenAI-compatible API at `api.githubcopilot.com` (Phase 3B).

### Future
| Phase | Integration |
|---|---|
| Phase 6+ | Notion API for bi-directional sync |

## Phase Roadmap

| Phase | Name | Description |
|---|---|---|
| 0 | Skeleton | Project structure, CLI, config, logging, error handling |
| 1 | Ingest | Read files (txt, md, pdf, py) into Document model |
| 2 | Knowledge Base | SQLite/JSONL storage, CRUD, search |
| 3 | AI Providers | Ollama, LM Studio, GitHub Copilot integration with preferred provider routing and automatic fallback ✅ |
| 4 | Distill | Chunking, summarization, entity extraction |
| 5 | Compile | Render flashcards, notes, study guides |
| 6 | Notion Sync | Bi-directional Notion integration |
| 7 | Orchestrator | End-to-end pipeline, incremental processing |
| 8 | Quality | Tests, linting, CI/CD pipeline |
| 9 | Polish | Error recovery, progress bars, rich output |
| 10 | Distribution | Packaging, docs, release automation |

