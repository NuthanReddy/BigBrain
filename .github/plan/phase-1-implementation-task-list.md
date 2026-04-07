# BigBrain Phase 1 Implementation Task List

## Goal

Implement the **core local ingestion MVP** for:
- TXT
- Markdown
- PDF
- Python source files

Phase 1 should produce a stable ingestion layer that converts supported files into a shared `Document` model and exposes that workflow through the CLI.

This phase should **not** implement persistence, distillation, provider runtime logic, or Notion sync yet.

---

## Scope Boundaries

### In scope
- shared ingestion data contracts
- ingestion-specific config defaults
- file discovery and filtering
- TXT ingestion
- Markdown ingestion
- PDF ingestion
- Python source ingestion
- CLI wiring for `ingest`
- user-facing summaries and error handling
- fixture-based validation scaffolding

### Out of scope
- KB persistence to JSON/JSONL or SQLite
- distillation/summarization
- GitHub Copilot / Ollama / LM Studio runtime execution
- Notion sync
- OCR for scanned PDFs
- DOCX and PPT ingestion

---

## Phase 0 Carry-Over Issues / Preconditions

Phase 1 should not assume Phase 0 is already complete. If any of the following foundation items are still unfinished, they become **Phase 1 blockers or carry-over tasks** and must be completed first:

- [ ] `src/bigbrain/` package structure exists and imports cleanly
- [ ] `main.py` is a thin entry point that delegates into `bigbrain.cli.main()`
- [ ] `src/bigbrain/cli.py` exists with scaffolded top-level commands, especially `ingest`
- [ ] `src/bigbrain/config.py` exists and can load defaults plus `config/example.yaml`
- [ ] `src/bigbrain/logging_config.py` exists with shared logger setup
- [ ] `pyproject.toml` supports `src` layout packaging
- [ ] `config/example.yaml` exists
- [ ] `README.md` and `AGENTS.md` reflect the package-based structure

### Why these matter
- Phase 1 adds real behavior to the `ingest` command rather than creating a second CLI path.
- Ingestion defaults should extend the Phase 0 config model rather than inventing a parallel config system.
- All new ingestion modules should use the shared Phase 0 logging pattern and error boundary.
- Packaging and imports must work before fixture-based validation or CLI smoke tests are meaningful.

### Minimum preflight acceptance criteria
- `python main.py --help` succeeds before Phase 1 feature work begins
- `python main.py ingest --help` succeeds before wiring real ingestion behavior
- `src/bigbrain/` is the canonical import root used by all Phase 1 modules

---

## Recommended Implementation Order

0. Close any unresolved Phase 0 foundation gaps that block ingestion work
1. Define the shared `Document` and ingestion result contracts
2. Normalize user-facing error handling
3. Extend config for ingestion defaults
4. Add file discovery and ingester registry/dispatcher
5. Implement TXT ingester
6. Implement Markdown ingester
7. Implement PDF ingester
8. Implement Python ingester
9. Wire the `ingest` CLI handler
10. Add docs and validation fixtures

---

## Workstream 0 - Phase 0 Foundation Closure

### Tasks
- [ ] Verify the package-based structure from Phase 0 is present
- [ ] Verify `main.py` delegates into `bigbrain.cli.main()`
- [ ] Verify `ingest` already exists as a scaffolded CLI command
- [ ] Verify config loading exists before adding ingestion-specific settings
- [ ] Verify logging setup exists before creating ingestion modules
- [ ] Verify packaging/imports work from the repo root
- [ ] If any of the above is missing, implement that missing Phase 0 item first

### Suggested files
- `main.py`
- `src/bigbrain/cli.py`
- `src/bigbrain/config.py`
- `src/bigbrain/logging_config.py`
- `pyproject.toml`
- `README.md`
- `AGENTS.md`

### Acceptance criteria
- Phase 1 work starts from the shared Phase 0 foundation, not from ad hoc file creation
- there is exactly one CLI entry path
- there is exactly one config-loading path
- there is exactly one shared logging pattern

### Validation ideas
- run `python .\main.py --help`
- run `python .\main.py ingest --help`
- verify package imports resolve from `src/bigbrain/`

---

## Workstream A - Shared Schema and Result Contracts

### Tasks
- [ ] Add a shared `Document` dataclass in `src/bigbrain/kb/models.py`
- [ ] Add supporting types such as:
  - [ ] `SourceMetadata`
  - [ ] `DocumentSection` or `DocumentPart`
  - [ ] `IngestionResult`
- [ ] Include Phase 1-ready fields such as:
  - [ ] `id`
  - [ ] `source_path`
  - [ ] `source_type`
  - [ ] `file_extension`
  - [ ] `modified_at`
  - [ ] `title`
  - [ ] `content`
  - [ ] `language`
  - [ ] `metadata`
  - [ ] optional `parts`
- [ ] Keep the schema rich enough for Phase 2 KB persistence handoff

### Suggested files
- `src/bigbrain/kb/models.py`

### Acceptance criteria
- every ingester returns the same core `Document` shape
- the schema is suitable for later KB storage without redesign
- file-type-specific metadata can be stored without changing the base contract

### Validation ideas
- verify each ingester returns the same required top-level fields
- verify optional metadata works without breaking the shared contract

---

## Workstream B - Errors, Logging, and User-Facing Failures

### Tasks
- [ ] Add or normalize `UserError` in `src/bigbrain/errors.py`
- [ ] Ensure ingestion modules use `get_logger(__name__)`
- [ ] Map user-facing problems to `UserError`, including:
  - [ ] missing path
  - [ ] unreadable file
  - [ ] unsupported extension when explicitly targeted
  - [ ] invalid directory path
- [ ] Keep unexpected internal exceptions debuggable while user-facing misuse stays clean

### Suggested files
- `src/bigbrain/errors.py`
- `src/bigbrain/logging_config.py`
- `src/bigbrain/cli.py`

### Acceptance criteria
- normal user mistakes do not emit raw tracebacks
- ingestion failures are concise and actionable
- logs are available for debugging skipped/failed files

### Validation ideas
- invalid file path test
- unsupported file extension test
- unreadable/corrupt file test

---

## Workstream C - Config and Ingestion Defaults

### Tasks
- [ ] Extend `BigBrainConfig` with an ingestion section
- [ ] Add defaults for:
  - [ ] supported extensions
  - [ ] recursive directory traversal
  - [ ] hidden-file behavior
  - [ ] max file size or safety limits
  - [ ] PDF extraction options
- [ ] Update `config/example.yaml`
- [ ] Ensure config precedence stays consistent with project rules:
  1. hardcoded defaults
  2. YAML config
  3. `BIGBRAIN_*` environment variables

### Suggested files
- `src/bigbrain/config.py`
- `config/example.yaml`

### Acceptance criteria
- ingestion behavior is driven by config, not scattered constants
- example config documents the available ingestion settings clearly
- env overrides can change ingestion defaults without code edits

### Validation ideas
- test recursive on/off behavior through config
- test supported-extension overrides through config/env

---

## Workstream D - File Discovery, Filtering, and Dispatch

### Tasks
- [ ] Add a discovery layer for files and directories
- [ ] Support single-file input and directory input
- [ ] Support recursive traversal
- [ ] Filter by supported extensions
- [ ] Skip unsupported files with warnings instead of failing the whole run
- [ ] Add an extension-to-ingester registry/dispatcher
- [ ] Return structured counts for processed/skipped/failed inputs

### Suggested files
- `src/bigbrain/ingest/discovery.py`
- `src/bigbrain/ingest/registry.py`
- `src/bigbrain/ingest/service.py`

### Acceptance criteria
- folders can be ingested recursively
- mixed directories process supported files and skip the rest
- routing is deterministic and easy to extend later

### Validation ideas
- mixed fixture directory test
- empty directory test
- recursive nested-directory test

---

## Workstream E - TXT and Markdown Ingestion

### Tasks
- [ ] Implement `text_ingester.py`
- [ ] Support UTF-8-first decoding with clear fallback/error behavior
- [ ] Implement `markdown_ingester.py`
- [ ] Preserve heading structure in Markdown metadata/parts
- [ ] Preserve relative/internal links where possible
- [ ] Infer title from filename or first heading when useful

### Suggested files
- `src/bigbrain/ingest/text_ingester.py`
- `src/bigbrain/ingest/markdown_ingester.py`

### Acceptance criteria
- TXT files ingest into clean `Document` objects
- Markdown files preserve heading structure sufficiently for later distillation
- title inference is stable and predictable

### Validation ideas
- plain TXT fixture
- Markdown fixture with nested headings and links
- empty/whitespace-only file fixture

---

## Workstream F - PDF Ingestion

### Tasks
- [ ] Add a Phase 1 PDF dependency in `pyproject.toml`
- [ ] Implement `pdf_ingester.py`
- [ ] Preserve page boundaries in metadata or document parts
- [ ] Capture available PDF metadata such as title/author if present
- [ ] Handle malformed or unreadable PDFs gracefully
- [ ] Keep Phase 1 limited to machine-readable PDFs only

### Suggested files
- `src/bigbrain/ingest/pdf_ingester.py`
- `pyproject.toml`

### Acceptance criteria
- machine-readable PDFs ingest successfully
- page separation is preserved
- malformed PDFs fail cleanly
- OCR is not required for Phase 1 success

### Validation ideas
- multi-page text PDF fixture
- malformed/corrupt PDF fixture
- PDF with missing metadata fixture

---

## Workstream G - Python Source Ingestion

### Tasks
- [ ] Implement `python_ingester.py`
- [ ] Preserve raw source code content
- [ ] Tag ingested source as Python
- [ ] Optionally extract module docstring
- [ ] Optionally extract top-level classes/functions into metadata
- [ ] Preserve enough code structure for later Markdown compilation and distillation

### Suggested files
- `src/bigbrain/ingest/python_ingester.py`

### Acceptance criteria
- Python files ingest into `Document` objects without altering code text
- basic symbol metadata is captured when available
- Python-only support is explicit; other languages are skipped or deferred cleanly

### Validation ideas
- Python fixture with module docstring
- Python fixture with top-level classes and functions
- Python fixture with no docstring

---

## Workstream H - CLI Integration

### Tasks
- [ ] Replace the stub `ingest` handler with a real Phase 1 handler
- [ ] Allow ingestion from either a file path or directory path
- [ ] Add useful flags only as needed, such as:
  - [ ] `--recursive`
  - [ ] `--type`
  - [ ] `--include-hidden`
- [ ] Print a concise summary of:
  - [ ] processed files
  - [ ] skipped files
  - [ ] failed files
  - [ ] warnings
- [ ] Keep `main.py` thin and all ingestion logic in `src/bigbrain/`

### Suggested files
- `src/bigbrain/cli.py`
- `main.py`

### Acceptance criteria
- `python main.py ingest ...` performs real ingestion work
- help text matches actual behavior
- results are understandable from CLI output alone
- user-facing failures stay concise

### Validation ideas
- single-file TXT ingestion
- single-file PDF ingestion
- mixed recursive folder ingestion
- bad path / invalid path CLI test

---

## Workstream I - Documentation and Fixtures

### Tasks
- [ ] Update `README.md` with real Phase 1 ingest usage
- [ ] Update `AGENTS.md` if Phase 1 introduces new architectural truth such as shared schemas or `errors.py`
- [ ] Add fixture-oriented tests for supported input types
- [ ] Add a small `tests/fixtures/ingest/` corpus

### Suggested files
- `README.md`
- `AGENTS.md`
- `tests/ingest/`
- `tests/fixtures/ingest/`

### Acceptance criteria
- docs reflect the actual supported Phase 1 formats
- fixture set covers the happy path and basic failure path for each supported type
- contributors can understand the ingestion architecture without reading all modules

---

## Suggested Phase 1 File Additions

```text
src/bigbrain/
├── errors.py
├── cli.py
├── config.py
├── ingest/
│   ├── __init__.py
│   ├── discovery.py
│   ├── registry.py
│   ├── service.py
│   ├── text_ingester.py
│   ├── markdown_ingester.py
│   ├── pdf_ingester.py
│   └── python_ingester.py
└── kb/
    └── models.py

tests/
├── ingest/
└── fixtures/
    └── ingest/
```

---

## Definition of Done for Phase 1

Phase 1 is done when all of the following are true:
- [ ] Phase 0 foundation blockers required by ingestion are closed
- [ ] TXT ingestion works for single files and directories
- [ ] Markdown ingestion works and preserves heading structure
- [ ] PDF ingestion works for machine-readable PDFs and preserves page boundaries
- [ ] Python ingestion works and preserves source content
- [ ] all supported ingesters return a common `Document` schema
- [ ] `python main.py ingest ...` is wired and usable
- [ ] skipped/unsupported files are reported clearly
- [ ] docs reflect the supported ingestion surface
- [ ] Phase 2 persistence is not required for ingestion to be useful

---

## Suggested Validation Commands

```powershell
python .\main.py ingest --help
python .\main.py ingest --source .\tests\fixtures\ingest\sample.txt
python .\main.py ingest --source .\tests\fixtures\ingest\sample.md
python .\main.py ingest --source .\tests\fixtures\ingest\sample.pdf
python .\main.py ingest --source .\tests\fixtures\ingest\sample.py
python .\main.py ingest --source .\tests\fixtures\ingest\ --recursive
```

---

## Recommended First Commit Slice

### Slice 0
- close any missing Phase 0 foundation gaps
- verify `main.py`, `cli.py`, config, logging, and packaging are usable

### Slice 1
- `Document` and ingestion result contracts
- `UserError` normalization
- ingestion config shape

### Slice 2
- discovery layer
- registry/dispatcher
- TXT and Markdown ingesters

### Slice 3
- PDF ingester
- Python ingester

### Slice 4
- CLI integration
- reporting
- docs and fixtures

---

## Phase 2 Handoff Notes

Phase 2 should consume the `Document` outputs created here without redesigning ingestion contracts.

That means this phase should leave behind:
- Phase 0 foundation conventions still intact
- a stable `Document` model in `src/bigbrain/kb/models.py`
- deterministic ingestion output for supported file types
- clear metadata for source path, type, timestamps, and structured parts
- CLI wiring that later phases can extend instead of replace

