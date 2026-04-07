# BigBrain Phase 2 Implementation Task List

## Goal

Implement the **canonical knowledge store** so Phase 1 `Document` outputs can be persisted, queried locally, and reused by later phases.

Phase 2 should establish:
- JSON/JSONL as the canonical interchange/storage format
- SQLite as an early local query/index layer
- stable storage contracts for `Document`, chunks, entities, and relationships
- repository/service APIs that later phases can consume without bypassing the store

---

## Parallelization Strategy

This phase can be parallelized well after the storage contracts are agreed:
- shared persistence contracts first
- JSON/JSONL persistence and SQLite indexing can proceed mostly in parallel
- CLI/status/query integration can proceed once the store service surface is stable
- fixtures/migration validation can proceed alongside implementation

---

## Scope Boundaries

### In scope
- persistence contracts for KB objects
- JSON/JSONL storage layout
- SQLite schema and query/index support
- repository/service APIs
- basic CRUD and local query helpers
- manifest/version metadata
- CLI surfaces needed to inspect/search stored content

### Out of scope
- provider runtime logic
- distillation algorithms
- summary rendering
- Notion sync
- advanced ranking or semantic search

---

## Phase 1 Carry-Over Issues / Preconditions

Before deep Phase 2 work begins, verify these Phase 1 outputs exist and are stable:
- [ ] `Document` model is defined and used consistently by Phase 1 ingesters
- [ ] ingestion metadata fields are stable enough for persistence
- [ ] `UserError` and logging conventions are established
- [ ] the CLI foundation can be extended without redesign
- [ ] Phase 1 fixture corpus exists or can be reused for persistence tests

### Minimum preflight acceptance criteria
- Phase 1 `Document` outputs can be serialized predictably
- `src/bigbrain/kb/` is available as the canonical store package

---

## Recommended Implementation Order

0. Close any Phase 1 model inconsistencies that block persistence
1. Finalize storage models and serialization rules
2. Implement JSON/JSONL persistence
3. Implement SQLite schema and indexing
4. Add repository/service APIs
5. Add search/read/query helpers
6. Add CLI and reporting integration
7. Add migration/fixture validation and docs

---

## Workstream A - Storage Contracts and Serialization Rules

### Tasks
- [ ] Confirm or refine `Document` contract for persistence use
- [ ] Define persistence-ready models for:
  - [ ] `StoredDocument`
  - [ ] `StoredChunk`
  - [ ] `StoredEntity`
  - [ ] `StoredRelationship`
  - [ ] `CompilationArtifactRef` placeholder
- [ ] Define stable IDs and version fields
- [ ] Define serialization/deserialization rules
- [ ] Define timestamps and provenance rules
- [ ] Define schema versioning strategy

### Suggested files
- `src/bigbrain/kb/models.py`
- `src/bigbrain/kb/serialization.py`

### Acceptance criteria
- all persisted objects have stable IDs and timestamps
- JSON serialization is deterministic
- schema evolution has a documented version field

---

## Workstream B - JSON/JSONL Persistence Layer

### Tasks
- [ ] Implement JSON/JSONL writers
- [ ] Implement JSON/JSONL readers
- [ ] Define storage layout on disk
- [ ] Support append and replace/update flows
- [ ] Validate atomic write strategy or safe-write behavior
- [ ] Add manifest/metadata file for KB state if needed

### Suggested files
- `src/bigbrain/kb/store.py`
- `src/bigbrain/kb/jsonl_store.py`

### Acceptance criteria
- documents can be saved and loaded without metadata loss
- JSON/JSONL remains the canonical interchange format
- partial writes do not silently corrupt the store

---

## Workstream C - SQLite Index and Query Layer

### Tasks
- [ ] Define SQLite schema for documents and queryable metadata
- [ ] Create schema initialization/migration bootstrap
- [ ] Index core fields like title, type, path, timestamps
- [ ] Add lookup/query helpers
- [ ] Keep SQLite aligned with JSON/JSONL source of truth
- [ ] Add consistency-check helpers between JSONL and SQLite

### Suggested files
- `src/bigbrain/kb/index.py`
- `src/bigbrain/kb/sqlite_index.py`

### Acceptance criteria
- local queries can run against SQLite without replacing JSON/JSONL as canonical
- re-indexing from JSON/JSONL is supported
- schema initialization is repeatable and safe

---

## Workstream D - Repository / Service API

### Tasks
- [ ] Add a store service or repository abstraction
- [ ] Support core operations:
  - [ ] add documents
  - [ ] get document by ID
  - [ ] list documents
  - [ ] update document metadata
  - [ ] delete/prune if needed
  - [ ] search/list via SQLite-backed helpers
- [ ] Keep the API independent from CLI concerns
- [ ] Use `UserError` for user-facing store misuse

### Suggested files
- `src/bigbrain/kb/service.py`
- `src/bigbrain/kb/store.py`

### Acceptance criteria
- later phases can depend on the KB service instead of file-level ad hoc access
- API boundaries are clean and testable
- store operations log through the shared logging pattern

---

## Workstream E - CLI and Local Query Surfaces

### Tasks
- [ ] Add or refine CLI support for store-related inspection
- [ ] Add `status` support for KB counts and health
- [ ] Add initial `kb-search` implementation over stored records
- [ ] Add user-friendly messages for empty store / missing store / malformed store
- [ ] Keep CLI output concise and script-friendly

### Suggested files
- `src/bigbrain/cli.py`
- `src/bigbrain/kb/service.py`

### Acceptance criteria
- users can inspect whether the KB exists and contains data
- users can run a basic local query/search against stored content
- failures remain clean and actionable

---

## Workstream F - Validation, Fixtures, and Docs

### Tasks
- [ ] Add persistence fixtures derived from Phase 1 documents
- [ ] Add round-trip tests for save/load
- [ ] Add JSONL-to-SQLite consistency tests
- [ ] Update `README.md` with KB storage behavior
- [ ] Update `AGENTS.md` if storage architecture changes materially

### Suggested files
- `tests/kb/`
- `tests/fixtures/kb/`
- `README.md`
- `AGENTS.md`

### Acceptance criteria
- round-trip serialization is tested
- JSONL and SQLite remain aligned for supported operations
- docs describe where the KB lives and how it is queried

---

## Definition of Done for Phase 2

Phase 2 is done when all of the following are true:
- [ ] Phase 1 persistence blockers are closed
- [ ] `Document` outputs can be saved and loaded from JSON/JSONL
- [ ] SQLite indexing/query support exists and is initialized automatically or explicitly
- [ ] store/repository APIs are usable by later phases
- [ ] basic CLI status/search over stored content works
- [ ] round-trip tests and consistency checks exist
- [ ] JSON/JSONL remains canonical while SQLite is available early for querying

---

## Recommended First Commit Slice

### Slice 0
- resolve any Phase 1 model issues that block persistence

### Slice 1
- persistence contracts
- schema versioning
- serialization helpers

### Slice 2
- JSON/JSONL store
- safe write/read flow

### Slice 3
- SQLite schema
- indexing/query helpers

### Slice 4
- repository/service API
- CLI integration
- fixtures/docs

