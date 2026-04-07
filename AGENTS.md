# AGENTS Guide

## Project Snapshot
- **BigBrain** is a structured Python CLI application for ingesting, distilling, and compiling knowledge from multiple sources.
- Package layout: `src/bigbrain/` with subpackages for each pipeline stage.
- Runtime entry point is `main.py` (thin wrapper that calls `bigbrain.cli.main()`).
- Packaging metadata lives in `pyproject.toml` (`[project]` with Python `>=3.10`).
- Console script: `bigbrain` (via `pyproject.toml` `[project.scripts]`).
- Dependency: `pyyaml>=6.0` for config loading.

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
| `bigbrain.errors` | `UserError` → `IngestionError` → `UnsupportedFormatError`, `FileAccessError`; `ConfigError` |
| `bigbrain.kb.models` | `Document`, `SourceMetadata`, `DocumentSection`, `IngestionResult` data models |
| `bigbrain.ingest.service` | `ingest_path()` – main ingestion entry point; accepts a path and returns `IngestionResult` |
| `bigbrain.ingest.registry` | `BaseIngester` ABC + extension-to-ingester registry |
| `bigbrain.ingest.discovery` | File discovery and filtering (recursive traversal, hidden-file skipping, extension filtering) |
| `bigbrain.ingest.text_ingester` | Plain-text ingester (UTF-8 with fallback encoding) |
| `bigbrain.ingest.markdown_ingester` | Markdown ingester (heading structure, internal links) |
| `bigbrain.ingest.pdf_ingester` | PDF ingester (page boundaries, metadata) |
| `bigbrain.ingest.python_ingester` | Python ingester (AST symbol extraction, docstrings) |

### Subpackages
| Subpackage | Purpose |
|---|---|
| `bigbrain.ingest` | **Active (Phase 1)** – Reads source material into a common Document model via format-specific ingesters |
| `bigbrain.kb` | **Active (Phase 1)** – Document/SourceMetadata/IngestionResult models; storage coming in Phase 2 |
| `bigbrain.orchestrator` | Manages end-to-end workflows and incremental processing |
| `bigbrain.distill` | Chunk, normalize, summarize, extract entities, build relationships |
| `bigbrain.compile` | Render reusable outputs from stored/distilled content |

### Ingestion Pipeline (Phase 1)
1. `bigbrain.cli` parses `ingest --source <path>` and calls `bigbrain.ingest.service.ingest_path()`.
2. `discovery.discover_files()` walks the path, filters by extension, skips hidden files.
3. For each discovered file, `registry.get_ingester(extension)` returns the appropriate `BaseIngester`.
4. The ingester's `.ingest(path)` method returns a `Document` with sections and metadata.
5. Results are collected into an `IngestionResult` (successes, failures, skipped counts).

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
- Test fixtures live in `tests/fixtures/ingest/` (sample files for each supported format).
- No test runner is configured yet; tests will be added alongside Phase 1 implementation tests.

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

## File Structure (Phase 1)
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
│   └── fixtures/
│       └── ingest/
│           ├── sample.txt           # Plain-text fixture
│           ├── sample.md            # Markdown fixture
│           ├── sample.py            # Python fixture (symbol extraction)
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
│       │   └── models.py            # Document, SourceMetadata, DocumentSection, IngestionResult
│       ├── distill/
│       │   └── __init__.py          # Placeholder – distillation pipeline
│       └── compile/
│           └── __init__.py          # Placeholder – output compilation
└── AGENTS.md                        # This file
```

## Integration Points and Dependencies

### Current (Phase 0)
- **pyyaml** (`>=6.0`) – YAML config file loading.
- No external service integrations yet.

### Future
| Phase | Integration |
|---|---|
| Phase 2+ | SQLite for knowledge base persistence |
| Phase 3+ | GitHub Copilot Enterprise, Ollama, LM Studio (AI providers) |
| Phase 6+ | Notion API for bi-directional sync |

## Phase Roadmap

| Phase | Name | Description |
|---|---|---|
| 0 | Skeleton | Project structure, CLI, config, logging, error handling |
| 1 | Ingest | Read files (txt, md, pdf, py) into Document model |
| 2 | Knowledge Base | SQLite/JSONL storage, CRUD, search |
| 3 | AI Providers | GitHub Copilot, Ollama, LM Studio integration with fallback |
| 4 | Distill | Chunking, summarization, entity extraction |
| 5 | Compile | Render flashcards, notes, study guides |
| 6 | Notion Sync | Bi-directional Notion integration |
| 7 | Orchestrator | End-to-end pipeline, incremental processing |
| 8 | Quality | Tests, linting, CI/CD pipeline |
| 9 | Polish | Error recovery, progress bars, rich output |
| 10 | Distribution | Packaging, docs, release automation |

