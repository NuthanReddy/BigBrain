# BigBrain

**A knowledge compiler that ingests, distills, and compiles knowledge.**

## Current Status

**Phase 3 – AI Provider Integration.** Ollama and LM Studio backends with automatic fallback. Phase 2 storage and Phase 1 ingestion remain active.

## Quick Start

```bash
# Clone and enter the repo
cd BigBrain

# Install dependencies (pyyaml, pymupdf, pypdf, httpx)
pip install -e .

# Or run directly from repo root
python main.py --help
```

## CLI Commands

| Command              | Description                                              | Phase  |
|----------------------|----------------------------------------------------------|--------|
| `bigbrain ingest`    | Ingest content from local files or external sources      | 1 ✅   |
| `bigbrain status`    | Show knowledge base status and statistics                | 2 ✅   |
| `bigbrain kb-search` | Search the knowledge base (full-text)                    | 2 ✅   |
| `bigbrain kb-export` | Export knowledge base to JSONL file                      | 2 ✅   |
| `bigbrain kb-import` | Import documents from a JSONL file                       | 2 ✅   |
| `bigbrain distill`   | Distill content into summaries, entities, relationships  | 4      |
| `bigbrain compile`   | Compile knowledge base into output formats               | 5      |
| `bigbrain update`    | Run incremental update on changed sources                | 7      |

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

# Search the knowledge base
python main.py kb-search "sorting algorithms"
python main.py kb-search "binary tree" --limit 5

# Export / import
python main.py kb-export -o backup.jsonl
python main.py kb-import backup.jsonl
```

### KB Configuration
```yaml
# config/example.yaml
kb:
  backend: sqlite
  db_path: ""  # empty = derived from paths.kb_dir
```

Environment variables: `BIGBRAIN_KB_BACKEND`, `BIGBRAIN_KB_DB_PATH`

### Python API

```python
from bigbrain.kb.service import KBService

with KBService.from_config() as svc:
    # Search documents
    docs = svc.search("algorithms")

    # Retrieve by ID or source path
    doc = svc.get_document_by_path("/path/to/file.md")

    # List all documents (with optional type filter)
    all_docs = svc.list_documents()
    pdfs = svc.list_documents(source_type="pdf")

    # Stats and ingestion history
    stats = svc.get_stats()
    runs = svc.list_ingestion_runs()

    # Export / import
    svc.export_jsonl("backup.jsonl")
    svc.import_jsonl("backup.jsonl")
```

## AI Providers (Phase 3)

BigBrain integrates with local LLM providers for text generation, summarization, and entity extraction. Providers are tried in order with automatic fallback.

### Supported Providers

| Provider | API | Default URL |
|----------|-----|-------------|
| Ollama | Native REST API | http://localhost:11434 |
| LM Studio | OpenAI-compatible | http://localhost:1234 |

### Configuration

Enable providers in `config/example.yaml`:
```yaml
providers:
  ollama:
    enabled: true
    base_url: "http://localhost:11434"
    default_model: "llama3.2"
    timeout: 120
  lm_studio:
    enabled: true
    base_url: "http://localhost:1234"
    timeout: 120
```

### Python API

```python
from bigbrain.providers import ProviderRegistry

registry = ProviderRegistry.from_app_config()

# Check what's available
print(registry.health_check())

# Generate text (auto-fallback between providers)
response = registry.complete("Explain quicksort in one paragraph")
print(response.text)

# Chat
response = registry.chat([
    {"role": "user", "content": "What is a binary tree?"}
])
```

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
| `BIGBRAIN_KB_BACKEND` | string | `sqlite` |
| `BIGBRAIN_KB_DB_PATH` | string | `/custom/path.db` |

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
│   │   ├── store.py       # KBStore – SQLite persistence + FTS5 search
│   │   └── service.py     # KBService – high-level API for later phases
│   ├── providers/         # AI providers (Phase 3 ✅)
│   │   ├── base.py        # BaseProvider ABC, ProviderResponse
│   │   ├── config.py      # OllamaConfig, LMStudioConfig, ProviderConfig
│   │   ├── registry.py    # ProviderRegistry with fallback
│   │   ├── ollama.py      # Ollama REST API client
│   │   └── lm_studio.py   # LM Studio OpenAI-compatible client
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
# Run full test suite (190 tests)
python -m pytest tests/ -v

# Run only ingestion tests
python -m pytest tests/ingest/ -v

# Run KB store tests
python -m pytest tests/test_kb_store.py -v

# Run provider tests
python -m pytest tests/test_providers.py -v

# Run a specific test module
python -m pytest tests/ingest/test_pdf_ingester.py -v
```

## Phase Roadmap

| Phase | Goal                                              |
|-------|---------------------------------------------------|
| 0     | Foundation and CLI scaffold                  ✅   |
| 1     | File ingestion (local files into raw store)  ✅   |
| 2     | Knowledge base storage and status reporting  ✅   |
| 3     | AI provider integration (Ollama, LM Studio)  ✅   |
| 4     | Content distillation (summaries, entities)        |
| 5     | Knowledge compilation into output formats         |
| 6     | Relationship extraction and knowledge graph       |
| 7     | Incremental updates and knowledge base search     |
| 8     | Multi-source ingestion (URLs, APIs)               |
| 9     | Plugin system and extensibility                   |
| 10    | Production hardening and performance optimization |

## License

TBD
