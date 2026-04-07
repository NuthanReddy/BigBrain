# BigBrain Phase 6 Implementation Task List

## Goal

Implement **Notion bidirectional page sync** for summary outputs.

This phase should support:
- publishing compiled summaries into Notion pages
- re-ingesting synced Notion pages back into the KB
- tracking sync metadata, cursors, remote IDs, and conflicts

---

## Parallelization Strategy

After sync contracts are defined, these workstreams can proceed with limited coupling:
- Notion page mapping model
- outbound publish adapter
- inbound reconciliation adapter
- sync state/conflict handling
- CLI/config/docs/tests

---

## Scope Boundaries

### In scope
- Notion page mapping contracts
- outbound page publishing
- inbound page re-ingest/reconciliation
- sync metadata/state tracking
- conflict detection and retry strategy
- CLI/config integration

### Out of scope
- generic multi-target sync
- Notion database sync
- UI sync dashboards

---

## Phase 5 Carry-Over Issues / Preconditions

- [ ] compiled summary outputs are stable
- [ ] summary provenance is preserved in compiled artifacts
- [ ] config can already store provider/integration settings

### Minimum preflight acceptance criteria
- Phase 5 outputs can be selected deterministically for publish/reconcile
- Notion credentials/config can be loaded safely

---

## Recommended Implementation Order

0. Close summary artifact and config blockers
1. Define Notion sync contracts and mapping rules
2. Implement outbound publish flow
3. Implement inbound pull/re-ingest flow
4. Implement sync state and conflict handling
5. Wire CLI and reporting
6. Add fixtures/docs/tests

---

## Workstream A - Sync Contracts and Mapping

### Tasks
- [ ] Define Notion page sync models
- [ ] Define mapping from compiled summary artifact -> Notion page
- [ ] Define remote ID, sync cursor, and timestamp fields
- [ ] Define conflict states and resolution markers

### Suggested files
- `src/bigbrain/compile/notion_models.py`
- `src/bigbrain/sync/notion_mapping.py`

### Acceptance criteria
- page sync inputs/outputs are stable and explicit
- sync state is represented in a reusable contract

---

## Workstream B - Outbound Publish

### Tasks
- [ ] Implement Notion page publish client/service
- [ ] Preserve source links and metadata
- [ ] Support idempotent or update-aware publishing
- [ ] Add retry behavior for transient failures

### Suggested files
- `src/bigbrain/compile/notion_compiler.py`
- `src/bigbrain/sync/notion_publish.py`

### Acceptance criteria
- summaries can be published to Notion pages
- repeated publishes do not create uncontrolled duplication
- publish failures are actionable and retryable

---

## Workstream C - Inbound Pull and Reconciliation

### Tasks
- [ ] Implement Notion page fetch/re-ingest flow
- [ ] Map remote page updates back into KB-compatible structures
- [ ] Preserve provenance and sync state
- [ ] Add reconciliation hooks for local/remote divergence

### Suggested files
- `src/bigbrain/sync/notion_pull.py`
- `src/bigbrain/ingest/notion_ingester.py`

### Acceptance criteria
- previously synced pages can be re-imported
- page changes are visible to the KB layer
- reconciliation flow is deterministic

---

## Workstream D - Sync State and Conflict Handling

### Tasks
- [ ] Persist sync metadata/state
- [ ] Detect conflicts using timestamps/version markers/content hashes
- [ ] Define retry strategy and user-facing conflict reporting
- [ ] Add sync audit logging

### Suggested files
- `src/bigbrain/sync/notion_state.py`
- `src/bigbrain/sync/notion_conflicts.py`

### Acceptance criteria
- sync state survives across runs
- conflicts are visible and actionable
- retries do not hide permanent failures

---

## Workstream E - CLI, Docs, and Validation

### Tasks
- [ ] Wire Notion sync commands/flags into CLI
- [ ] Update config example with Notion settings
- [ ] Add publish/pull/conflict fixtures or mocks
- [ ] Update README and AGENTS guidance

### Suggested files
- `src/bigbrain/cli.py`
- `config/example.yaml`
- `README.md`
- `AGENTS.md`
- `tests/sync/`

### Acceptance criteria
- users can publish and sync back through the CLI
- docs explain what page-level sync means
- tests cover publish, pull, and conflict cases

---

## Definition of Done for Phase 6

- [ ] Notion page mapping contracts exist
- [ ] summaries can be published to Notion pages
- [ ] previously synced pages can be re-ingested
- [ ] sync metadata and conflicts are tracked
- [ ] sync CLI flows are usable
- [ ] tests/docs cover page-level bidirectional sync

---

## Recommended First Commit Slice

### Slice 0
- close Phase 5 output/config blockers

### Slice 1
- sync contracts
- mapping rules

### Slice 2
- outbound publish

### Slice 3
- inbound reconciliation
- sync state/conflicts

### Slice 4
- CLI/docs/tests

