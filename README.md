# BigBrain

**A knowledge compiler that ingests, distills, and compiles knowledge.**

## Current Status

**Phase 11 – Polyglot Entity Store.** Pluggable backends: SQLite (default), PostgreSQL+pgvector, Neo4j, Qdrant, Weaviate, Pinecone.

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
| `bigbrain ingest`    | Ingest from files, URLs, or APIs                     | 1 ✅   |
| `bigbrain status`    | Show knowledge base status and statistics                | 2 ✅   |
| `bigbrain kb-search` | Search the knowledge base (full-text)                    | 2 ✅   |
| `bigbrain kb-export` | Export knowledge base to JSONL file                      | 2 ✅   |
| `bigbrain kb-import` | Import documents from a JSONL file                       | 2 ✅   |
| `bigbrain providers` | Show AI provider status and availability                 | 3 ✅   |
| `bigbrain auth`      | Manage GitHub Copilot authentication (login/logout)      | 3 ✅   |
| `bigbrain ask`       | Ask a question using KB context + AI (RAG)               | 3 ✅   |
| `bigbrain distill`   | Distill content into summaries, entities, relationships  | 4 ✅   |
| `bigbrain distill-show` | Show distilled output (summaries, entities, relationships) | 4 ✅ |
| `bigbrain entities`  | List entities with type/search filters                   | 4 ✅   |
| `bigbrain compact`   | Deduplicate entities, optimize KB                        | 4 ✅   |
| `bigbrain compile`   | Compile knowledge base into output formats               | 5      |
| `bigbrain notion`    | Notion sync/import/export/status                         | 6 ✅   |
| `bigbrain update`    | Incremental update pipeline (ingest→distill→compile)     | 7 ✅   |
| `bigbrain plugins`   | List discovered plugins                                  | 9 ✅   |

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

### Web & API Ingestion

```bash
# Ingest a web page
bigbrain ingest --url https://example.com/article

# Ingest from a REST API
bigbrain ingest --api https://api.example.com/data
bigbrain ingest --api https://api.example.com/data --json-path results.items

# API with authentication
bigbrain ingest --api https://api.example.com/private --auth-token YOUR_TOKEN
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

BigBrain integrates with local and cloud LLM providers for text generation, summarization, and entity extraction. Providers are tried in order (or by preferred provider) with automatic fallback.

### Supported Providers

| Provider | API | Default URL |
|----------|-----|-------------|
| Ollama | Native REST API | http://localhost:11434 |
| LM Studio | OpenAI-compatible | http://localhost:1234 |
| GitHub Copilot | OpenAI-compatible | https://api.githubcopilot.com |

### Configuration

Enable providers in `config/example.yaml`:
```yaml
providers:
  preferred_provider: "ollama"  # Optional: override fallback order
  ollama:
    enabled: true
    base_url: "http://localhost:11434"
    default_model: "llama3.2"
    timeout: 120
  lm_studio:
    enabled: true
    base_url: "http://localhost:1234"
    timeout: 120
  github_copilot:
    enabled: true
    # Auth: run 'bigbrain auth login' (no env var needed)
    default_model: "claude-opus-4.6"
    timeout: 60
    max_retries: 3
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

### Provider Status CLI

```bash
# Authenticate with GitHub Copilot (one-time device flow)
python main.py auth login

# Check auth status
python main.py auth status

# Check provider status
python main.py providers

# Show available models
python main.py providers --models

# Logout (clear cached token)
python main.py auth logout
```

## Distillation (Phase 4)

AI-powered content analysis: chunking, summarization, entity extraction, and relationship building.

### Usage

```bash
# Distill all KB documents (incremental — skips unchanged chunks)
bigbrain distill

# Re-distill everything from scratch
bigbrain distill --force

# Distill only a specific step
bigbrain distill --step summarize
bigbrain distill --step entities
bigbrain distill --step relationships

# Use a specific model
bigbrain distill --model claude-opus-4.6

# Parallel workers for multi-doc distillation
bigbrain distill --workers 3
```

### Viewing Results

```bash
# Show distilled summaries, entities, and relationships
bigbrain distill-show

# List entities with filters
bigbrain entities --types                # Show entity type counts
bigbrain entities --type algorithm       # Filter by type
bigbrain entities --search "binary"      # Search by name

# Deduplicate entities
bigbrain compact
```

### Distillation Configuration

```yaml
# config/example.yaml
distillation:
  chunk_strategy: by_section     # by_section | sliding_window | by_paragraph
  chunk_size: 1000               # max chars per chunk (sliding_window)
  chunk_overlap: 200             # overlap between chunks
  summary_max_length: 500        # max words for summaries
  entity_extraction: true
  relationship_extraction: true
  max_chunks_per_doc: 50
```

## Compilation (Phase 5)

Render distilled content into study materials: markdown summaries, flashcards, cheatsheets, Q&A sets, and study guides.

### Usage

```bash
# Compile all documents as markdown summaries (default)
bigbrain compile

# Generate flashcards (AI-powered)
bigbrain compile --format flashcard

# Generate cheatsheet (template-based, no AI needed)
bigbrain compile --format cheatsheet

# Generate Q&A study questions (AI-powered)
bigbrain compile --format qa

# Generate comprehensive study guide (AI-powered)
bigbrain compile --format study_guide

# Compile a specific document
bigbrain compile --doc-id <id> --format flashcard -o flashcards.md

# Use a specific model
bigbrain compile --format study_guide --model claude-opus-4.6
```

Output files are written to `build/` by default (configurable via `compile.output_dir`).

### Compilation Configuration

```yaml
# config/example.yaml
compile:
  output_dir: build
  default_format: markdown    # markdown | flashcard | cheatsheet | qa | study_guide
  flashcard_count: 20
  qa_count: 15
  include_relationships: true
  include_entities: true
```

## Notion Integration (Phase 6)

Bidirectional sync between the BigBrain knowledge base and your Notion workspace.

### Setup

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Set your token: `$env:BIGBRAIN_NOTION_TOKEN = "ntn_your_token"`
3. Share target Notion pages with your integration

### Usage

```bash
# Check Notion connectivity and sync status
bigbrain notion status

# Import pages from Notion into KB
bigbrain notion import
bigbrain notion import --query "algorithms" --limit 10

# Export KB documents to Notion
bigbrain notion export --parent-page-id <page-id>

# Full bidirectional sync
bigbrain notion sync --parent-page-id <page-id>
```

### Configuration

```yaml
# config/example.yaml
notion:
  enabled: true
  sync_direction: bidirectional  # bidirectional | import_only | export_only
  auto_create_pages: true
```

### Visual Content
- **OCR**: Images in Notion pages are automatically OCR'd during import (requires Tesseract)
- **Diagrams**: Compiled pages include Mermaid flowcharts and mindmaps
- **Rich blocks**: Callouts, toggles, tables, code blocks, equations in Notion exports

## Incremental Updates (Phase 7)

Automatically detect changed files and run only the necessary pipeline steps.

### Usage

```bash
# Incremental update (only processes changed files)
bigbrain update --source path/to/docs/

# Force full reprocessing
bigbrain update --source path/to/docs/ --force

# Run specific steps only
bigbrain update --source path/to/docs/ --steps ingest
bigbrain update --source path/to/docs/ --steps ingest,distill

# With AI model override
bigbrain update --source path/to/docs/ --model claude-opus-4.6
```

Change detection uses file modification times and content hashes to skip unchanged files.

## Plugin System (Phase 9)

Extend BigBrain with custom ingesters, compilers, and processors.

### Creating a Plugin

Place a `.py` file in the `plugins/` directory:

```python
from bigbrain.plugins.base import IngestPlugin, PluginInfo
from bigbrain.kb.models import Document, SourceMetadata
from pathlib import Path

class MyIngester(IngestPlugin):
    def info(self):
        return PluginInfo(name="my_ingester", version="1.0", plugin_type="ingester")
    
    def supported_extensions(self):
        return [".xyz"]
    
    def ingest(self, path: Path) -> Document:
        content = path.read_text()
        return Document(title=path.stem, content=content,
                       source=SourceMetadata(file_path=str(path), file_extension=".xyz", source_type="xyz"))
```

### Plugin Types

| Type | Base Class | Purpose |
|------|-----------|---------|
| Ingester | `IngestPlugin` | Custom file format support |
| Compiler | `CompilePlugin` | Custom output formats |
| Processor | `ProcessorPlugin` | Document transformation |

### Usage

```bash
# List discovered plugins
bigbrain plugins

# Plugins are auto-discovered from plugins/ directory
```

### Included Example Plugins

- `csv_ingester` — Ingest CSV files as structured documents
- `html_compiler` — Export knowledge as standalone HTML pages

## Production Features (Phase 10)

### Progress Bars
Multi-file operations show progress bars (powered by [rich](https://github.com/Textualize/rich)):
```bash
bigbrain distill    # Shows progress bar for multi-doc distillation
bigbrain update --source docs/   # Shows ingestion progress
```

### Logging Options
```bash
bigbrain --quiet ingest --source docs/     # Suppress log output
bigbrain --log-file app.log distill        # Log to file
bigbrain --log-format json status          # Structured JSON logs
```

### Retry & Resilience
- AI provider calls retry with exponential backoff
- Circuit breaker prevents repeated calls to failing providers
- Connection pooling for HTTP requests

## Entity Store Backends (Phase 11)

BigBrain supports multiple storage backends for entities and relationships. SQLite is the default; external backends are available for larger deployments.

### Supported Backends

| Backend | Best For | Relationships | Vector Search |
|---------|----------|---------------|---------------|
| SQLite | Local/dev (default) | ✅ | Text only |
| PostgreSQL + pgvector | Production SQL + vectors | ✅ | ✅ |
| Neo4j | Graph queries | ✅ (native) | ❌ |
| Qdrant | Vector similarity | ❌ | ✅ |
| Weaviate | Vector + BM25 | ❌ | ✅ |
| Pinecone | Managed vector | ❌ | ✅ |

### Configuration

```yaml
entity_store:
  backend: sqlite  # sqlite | postgres | neo4j | qdrant | weaviate | pinecone
  # postgres_url: "postgresql://user:pass@localhost:5432/bigbrain"
  # neo4j_url: "bolt://localhost:7687"
  # qdrant_url: "http://localhost:6333"
  # weaviate_url: "http://localhost:8080"
  # pinecone_api_key: "your-key"
```

### Installation

Backends are optional dependencies:
```bash
pip install -e ".[postgres]"     # PostgreSQL + pgvector
pip install -e ".[neo4j]"        # Neo4j
pip install -e ".[qdrant]"       # Qdrant
pip install -e ".[all-stores]"   # All backends
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
| `BIGBRAIN_PROVIDERS_PREFERRED` | string | `ollama` |

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
│   │   ├── python_ingester.py
│   │   ├── url_ingester.py
│   │   └── api_ingester.py
│   ├── kb/                # Knowledge base (Phase 2 ✅)
│   │   ├── models.py      # Document, SourceMetadata, etc.
│   │   ├── store.py       # KBStore – SQLite persistence + FTS5 search
│   │   └── service.py     # KBService – high-level API for later phases
│   ├── providers/         # AI providers (Phase 3 ✅)
│   │   ├── base.py        # BaseProvider ABC, ProviderResponse
│   │   ├── config.py      # OllamaConfig, LMStudioConfig, GitHubCopilotConfig, ProviderConfig
│   │   ├── registry.py    # ProviderRegistry with preferred provider + fallback
│   │   ├── ollama.py      # Ollama REST API client
│   │   ├── lm_studio.py   # LM Studio OpenAI-compatible client
│   │   ├── github_copilot.py  # GitHub Copilot OpenAI-compatible client
│   │   └── github_auth.py     # GitHub token discovery and authentication
│   ├── orchestrator/      # Pipeline orchestration (Phase 7 ✅)
│   │   ├── change_detector.py  # File change detection (mtime + content hash)
│   │   └── pipeline.py         # Orchestrator – end-to-end update pipeline
│   ├── distill/           # Content distillation (Phase 4 ✅)
│   │   ├── models.py      # Chunk, Summary, Entity, Relationship
│   │   ├── chunker.py     # Chunking strategies (section, sliding window, paragraph)
│   │   ├── summarizer.py  # AI-powered summarization
│   │   ├── entities.py    # AI entity extraction
│   │   ├── relationships.py # AI relationship building
│   │   └── pipeline.py    # DistillPipeline orchestrator
│   ├── compile/           # Knowledge compilation (Phase 5 ✅)
│   │   ├── models.py      # CompileOutput, Flashcard, QAPair, OutputFormat
│   │   ├── markdown.py    # Markdown summary renderer
│   │   ├── flashcard.py   # AI/template flashcard generator
│   │   ├── cheatsheet.py  # Entity-based cheatsheet
│   │   ├── qa_generator.py # AI/template Q&A generator
│   │   ├── study_guide.py # AI/template study guide
│   │   └── pipeline.py    # CompilePipeline orchestrator
│   ├── notion/            # Notion integration (Phase 6 ✅)
│   │   ├── client.py      # Notion API client wrapper
│   │   ├── importer.py    # Import Notion pages to KB
│   │   ├── exporter.py    # Export KB content to Notion
│   │   └── sync.py        # Bidirectional sync engine
│   ├── plugins/           # Plugin system (Phase 9 ✅)
│   │   ├── base.py        # PluginBase, IngestPlugin, CompilePlugin, ProcessorPlugin ABCs
│   │   ├── discovery.py   # Directory scanning + entry_points discovery
│   │   └── loader.py      # PluginLoader – validate, filter, register
│   ├── stores/            # Polyglot entity store backends (Phase 11 ✅)
│   │   ├── base.py        # EntityStoreBackend ABC
│   │   ├── sqlite_backend.py  # SQLite adapter (default, wraps KBStore)
│   │   ├── postgres.py        # PostgreSQL + pgvector backend
│   │   ├── neo4j_backend.py   # Neo4j graph backend
│   │   ├── qdrant_backend.py  # Qdrant vector backend
│   │   ├── weaviate_backend.py # Weaviate vector + BM25 backend
│   │   └── pinecone_backend.py # Pinecone managed vector backend
│   ├── progress.py        # Progress bars with rich fallback (Phase 10 ✅)
│   ├── retry.py           # Retry decorator + circuit breaker (Phase 10 ✅)
│   ├── http.py            # Shared httpx connection pool (Phase 10 ✅)
│   └── validation.py      # Input validation helpers (Phase 10 ✅)
├── plugins/               # User plugin directory (auto-discovered)
│   ├── csv_ingester.py    # Example: CSV file ingester
│   └── html_compiler.py   # Example: HTML page compiler
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
# Run full test suite (524+ tests)
python -m pytest tests/ -v

# Run by module
python -m pytest tests/ingest/ -v          # Ingestion pipeline
python -m pytest tests/test_kb_store.py -v # KB store
python -m pytest tests/test_providers.py -v # AI providers
python -m pytest tests/test_rag.py -v      # RAG pipeline
python -m pytest tests/test_distill.py -v  # Distillation
python -m pytest tests/test_compile.py -v  # Compilation
python -m pytest tests/test_notion.py -v   # Notion integration
python -m pytest tests/test_orchestrator.py -v # Orchestrator pipeline
python -m pytest tests/test_plugins.py -v  # Plugin system
python -m pytest tests/test_hardening.py -v # Production hardening
python -m pytest tests/test_stores.py -v   # Entity store backends
```

## Phase Roadmap

| Phase | Goal                                              |
|-------|---------------------------------------------------|
| 0     | Foundation and CLI scaffold                  ✅   |
| 1     | File ingestion (local files into raw store)  ✅   |
| 2     | Knowledge base storage and status reporting  ✅   |
| 3     | AI provider integration (Ollama, LM Studio, GitHub Copilot)  ✅   |
| 4     | Content distillation (summaries, entities, relationships)   ✅   |
| 5     | Knowledge compilation into output formats    ✅   |
| 6     | Notion bidirectional page sync and knowledge updates  ✅  |
| 7     | Incremental updates and knowledge base search     ✅  |
| 8     | Multi-source ingestion (URLs, APIs)          ✅   |
| 9     | Plugin system and extensibility               ✅   |
| 10    | Production hardening and performance optimization ✅ |
| 11    | Polyglot entity store (Postgres+pgvector, Neo4j, Qdrant, Weaviate, Pinecone) ✅ |

### Phase 11 Summary

- Pluggable entity store backends via `EntityStoreBackend` ABC.
- SQLite (default, zero-config), PostgreSQL+pgvector, Neo4j, Qdrant, Weaviate, Pinecone.
- `StoreConfig` dataclass with per-backend connection settings.
- Optional dependencies via `pyproject.toml` extras.

## License

TBD
