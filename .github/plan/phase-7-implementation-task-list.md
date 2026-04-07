# BigBrain Phase 7 Implementation Task List
<!-- PLAN:TEMPLATE v1 -->
<!-- PLAN:SOURCE .github/plan/_phase-task-template.md -->


## Goal

Implement **search, status, and incremental updates** so the knowledge base becomes operable at larger scale.

---

## Parallelization Strategy

After manifest/change contracts are defined, the following can proceed mostly independently:
- change tracking and manifests
- incremental pipeline orchestration
- local search indexing/query logic
- status/reporting surfaces
- fixtures and performance validation

---

## Scope Boundaries

### In scope
- file/input hashing and manifests
- incremental run planning
- skip/reprocess behavior
- local search over stored content
- status reporting
- processing reports

### Out of scope
- semantic/vector search
- UI dashboards
- cloud-hosted search services

---

## Phase 2–6 Carry-Over Issues / Preconditions

- [ ] KB store contracts and query helpers are stable
- [ ] compiled artifacts and sync metadata have stable IDs
- [ ] CLI has consistent management command structure

### Minimum preflight acceptance criteria
- stored items have stable identity and timestamps
- pipeline stages produce inspectable artifacts and metadata

---

## Recommended Implementation Order

0. Close artifact identity/blocker issues
1. Define manifest/change-tracking contracts
2. Implement hashing and incremental planning
3. Implement search service/index usage
4. Implement status/report/reporting
5. Wire orchestration and CLI surfaces
6. Add fixture/perf validation and docs

---

## Workstream A - Manifests and Change Tracking

### Tasks
- [ ] Define manifest format for tracked inputs and outputs
- [ ] Define file/document hashing rules
- [ ] Track timestamps, hashes, and relevant config fingerprints
- [ ] Add persistence for processing reports/manifests

### Suggested files
- `src/bigbrain/orchestrator/manifest.py`
- `src/bigbrain/orchestrator/change_tracker.py`

### Acceptance criteria
- change detection is deterministic
- manifests can explain why an item was processed or skipped

---

## Workstream B - Incremental Execution Planning

### Tasks
- [ ] Determine which stages need rerun when inputs change
- [ ] Skip unchanged inputs safely
- [ ] Re-run only affected downstream artifacts
- [ ] Surface skipped/changed counts in reports

### Suggested files
- `src/bigbrain/orchestrator/pipeline.py`
- `src/bigbrain/orchestrator/planner.py`

### Acceptance criteria
- repeated runs are faster when nothing changed
- downstream regeneration is scoped to impacted items
- skip behavior is observable and debuggable

---

## Workstream C - Search Service

### Tasks
- [ ] Define search query contract
- [ ] Implement local search over stored documents/chunks/entities
- [ ] Add ranking rules using title/type/metadata/entity matches
- [ ] Return concise search result summaries

### Suggested files
- `src/bigbrain/kb/search.py`
- `src/bigbrain/kb/service.py`

### Acceptance criteria
- users can query stored knowledge locally
- results are deterministic and reasonably ranked
- search does not require external services

---

## Workstream D - Status and Reporting

### Tasks
- [ ] Implement status summaries for KB health, counts, and last-run info
- [ ] Add processing reports for ingestion/distill/compile state
- [ ] Show missing/empty-store cases clearly

### Suggested files
- `src/bigbrain/orchestrator/status.py`
- `src/bigbrain/cli.py`

### Acceptance criteria
- `status` provides useful operational visibility
- reports are script-friendly and human-readable

---

## Workstream E - Validation and Docs

### Tasks
- [ ] Add fixtures for unchanged/changed/mixed incremental runs
- [ ] Add search relevance sanity checks
- [ ] Update README and AGENTS guidance for status/search/update flows

### Suggested files
- `tests/orchestrator/`
- `tests/kb/`
- `README.md`
- `AGENTS.md`

### Acceptance criteria
- incremental behavior is validated by fixtures
- docs explain search/update/status usage clearly

---

## Definition of Done for Phase 7

- [ ] manifest/change-tracking contracts exist
- [ ] incremental runs skip unchanged work safely
- [ ] local search works on stored content
- [ ] status/reporting commands are useful
- [ ] fixtures/docs cover the operational workflow

---

## Recommended First Commit Slice

### Slice 0
- close identity/metadata blockers

### Slice 1
- manifest models
- hashing/change tracking

### Slice 2
- incremental planner
- scoped rerun logic

### Slice 3
- search service
- status/reporting

### Slice 4
- CLI/docs/tests

