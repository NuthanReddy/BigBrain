# BigBrain

**A knowledge compiler that ingests, distills, and compiles knowledge.**

## Current Status

**Phase 2 – Knowledge Base Storage.** SQLite-backed persistence for ingested documents with full-text search. Phase 1 ingestion and Phase 0 foundation remain active.

## Quick Start

```bash
# Clone and enter the repo
cd BigBrain

# Install dependencies
pip install -e .

# Or run directly from repo root
python main.py --help
```

## CLI Commands

| Command              | Description                                              | Phase  |
|----------------------|----------------------------------------------------------|--------|
| `bigbrain ingest`    | Ingest content from local files or external sources      | 1 ✅   |
| `bigbrain distill`   | Distill content into summaries, entities, relationships  | 4      |
| `bigbrain compile`   | Compile knowledge base into output formats               | 5      |
| `bigbrain update`    | Run incremental update on changed sources                | 7      |
| `bigbrain status`    | Show knowledge base status and statistics                | 2 ✅   |
| `bigbrain kb-search` | Search the knowledge base                                | 7      |

## Ingestion (Phase 1)

BigBrain can ingest content from local files in these formats:

| Format | Extension | Features |
|--------|-----------|----------|
| Plain text | `.txt` | UTF-8 with fallback encoding |
| Markdown | `.md` | Heading structure, internal links preserved |
| PDF | `.pdf` | Page boundaries, metadata extraction |
| Python | `.py` | AST symbol extraction, docstrings |

### Usage Examples

```bash
# Ingest a single file
python main.py ingest --source path/to/file.md

# Ingest a directory recursively
python main.py ingest --source path/to/docs/

# Ingest only PDF files
python main.py ingest --source ./docs --type pdf

# Include hidden files
python main.py ingest --source ./project --include-hidden

# Non-recursive directory scan
python main.py ingest --source ./docs --no-recursive
```

### Ingestion Configuration

Edit `config/example.yaml` to customize:
```yaml
ingestion:
  supported_extensions: [".txt", ".md", ".pdf", ".py"]
  recursive: true
  skip_hidden: true
  max_file_size_mb: 50
```

## Knowledge Base (Phase 2)

Ingested documents are automatically stored in a local SQLite database. The knowledge base supports CRUD operations and full-text search.

### Status Command
```bash
python main.py status
```
Shows document count, size, type breakdown, and last ingestion run.

### Storage Options
```bash
# Ingest and store (default)
python main.py ingest --source shelf/

# Ingest without storing
python main.py ingest --source shelf/ --no-store
```

### KB Configuration
```yaml
# config/example.yaml
kb:
  backend: sqlite
  db_path: ""  # empty = derived from paths.kb_dir
```

Environment variables: `BIGBRAIN_KB_BACKEND`, `BIGBRAIN_KB_DB_PATH`

## Configuration

1. Copy `config/example.yaml` and customize for your environment.
2. Environment variables with the `BIGBRAIN_` prefix override YAML values.
3. Config precedence: **defaults → YAML → env vars → CLI flags**

### Environment Variable Overrides

Top-level settings use the `BIGBRAIN_` prefix. Nested ingestion settings use `BIGBRAIN_INGESTION_`:

| Variable | Type | Example |
|----------|------|---------|
| `BIGBRAIN_DEBUG` | bool | `true` |
| `BIGBRAIN_LOG_LEVEL` | string | `DEBUG` |
| `BIGBRAIN_INGESTION_RECURSIVE` | bool | `false` |
| `BIGBRAIN_INGESTION_SKIP_HIDDEN` | bool | `false` |
| `BIGBRAIN_INGESTION_MAX_FILE_SIZE_MB` | int | `100` |
| `BIGBRAIN_INGESTION_SUPPORTED_EXTENSIONS` | list | `.txt,.md,.pdf` |
| `BIGBRAIN_INGESTION_ENCODING` | string | `latin-1` |

## Project Structure

```
BigBrain/
├── src/bigbrain/          # Main package
│   ├── cli.py             # CLI entry point
│   ├── config.py          # Configuration loading
│   ├── logging_config.py  # Centralized logging
│   ├── errors.py          # UserError hierarchy
│   ├── ingest/            # Content ingestion (Phase 1 ✅)
│   │   ├── service.py     # ingest_path() entry point
│   │   ├── registry.py    # BaseIngester ABC + extension registry
│   │   ├── discovery.py   # File discovery and filtering
│   │   ├── text_ingester.py
│   │   ├── markdown_ingester.py
│   │   ├── pdf_ingester.py
│   │   └── python_ingester.py
│   ├── kb/                # Knowledge base (Phase 2 ✅)
│   │   ├── models.py      # Document, SourceMetadata, etc.
│   │   └── store.py       # KBStore – SQLite persistence + FTS5 search
│   ├── orchestrator/      # Pipeline orchestration (future)
│   ├── distill/           # Content distillation (future)
│   └── compile/           # Output compilation (future)
├── tests/                 # Test suite
│   ├── ingest/            # Ingestion pipeline tests
│   └── fixtures/ingest/   # Ingestion test fixtures
├── digest/                # Generated chapter summaries
├── shelf/                 # Source material (books, PDFs)
├── config/                # Configuration files
├── main.py                # Development entry point
└── pyproject.toml         # Package metadata
```

## Development

- **Python** >= 3.10
- `pip install -e .` for editable install
- `python main.py` for direct execution

### Running Tests

```bash
# Run full test suite
python -m pytest tests/ -v

# Run only ingestion tests
python -m pytest tests/ingest/ -v

# Run a specific test module
python -m pytest tests/ingest/test_pdf_ingester.py -v
```

## Phase Roadmap

| Phase | Goal                                              |
|-------|---------------------------------------------------|
| 0     | Foundation and CLI scaffold                       |
| 1     | File ingestion (local files into raw store)       |
| 2     | Knowledge base storage and status reporting  ✅   |
| 3     | AI provider integration (Copilot, Ollama, etc.)   |
| 4     | Content distillation (summaries, entities)        |
| 5     | Knowledge compilation into output formats         |
| 6     | Relationship extraction and knowledge graph       |
| 7     | Incremental updates and knowledge base search     |
| 8     | Multi-source ingestion (URLs, APIs)               |
| 9     | Plugin system and extensibility                   |
| 10    | Production hardening and performance optimization |

## License

TBD
