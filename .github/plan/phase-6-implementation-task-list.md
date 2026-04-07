# BigBrain Phase 6 Implementation Task List
<!-- PLAN:TEMPLATE v1 -->
<!-- PLAN:SOURCE .github/plan/_phase-task-template.md -->


## Goal

Implement **Notion MCP-based bidirectional page sync** for summary outputs.

This phase should support:
- publishing compiled summaries into Notion pages (BigBrain -> Notion)
- re-ingesting synced Notion pages back into the KB (Notion -> BigBrain)
- tracking sync metadata, cursors, remote IDs, and conflicts
- idempotent upserts and deterministic reconciliation for repeated runs

### Notion MCP Assumptions
- Use Notion MCP operations as the **mandatory** integration path (`search`, `fetch`, `create-pages`, `update-page`, optional comments/views).
- Start with **page-level sync MVP**; database-level sync can follow later.
- Treat MCP schema/format contracts as external dependencies that may evolve.
- Publish target is a caller-provided Notion page; default output page is `Big Brain` when no target is provided.

---

## Parallelization Strategy

After sync contracts are defined, these workstreams can proceed with limited coupling:
- Notion page mapping model
- outbound MCP publish adapter
- inbound MCP reconciliation adapter
- sync state/conflict handling
- CLI/config/docs/tests

---

## Scope Boundaries

### In scope
- Notion MCP page mapping contracts
- outbound page publishing via MCP
- inbound page re-ingest/reconciliation via MCP
- sync metadata/state tracking
- conflict detection and retry strategy
- CLI/config integration
- publish to a specific Notion page with default fallback (`Big Brain`)

### Out of scope
- generic multi-target sync
- full Notion database sync (defer to follow-up phase)
- UI sync dashboards

---

## Phase 5 Carry-Over Issues / Preconditions

- [ ] compiled summary outputs are stable
- [ ] summary provenance is preserved in compiled artifacts
- [ ] config can already store provider/integration settings
- [ ] Notion MCP access/auth setup is available in target environments

### Minimum preflight acceptance criteria
- Phase 5 outputs can be selected deterministically for publish/reconcile
- Notion credentials/config can be loaded safely
- one MCP-backed connectivity check can succeed before sync execution

---

## Recommended Implementation Order

0. Close summary artifact and config blockers
1. Define Notion MCP sync contracts and mapping rules
2. Implement outbound MCP publish flow
3. Implement inbound MCP pull/re-ingest flow
4. Implement sync state and conflict handling
5. Wire CLI and reporting
6. Add fixtures/docs/tests + risk hardening

---

## Workstream A - Sync Contracts and Mapping

### Tasks
- [ ] Define Notion page sync models
- [ ] Define mapping from compiled summary artifact -> Notion page
- [ ] Define remote ID, sync cursor, and timestamp fields
- [ ] Define conflict states and resolution markers
- [ ] Define MCP payload adapters (BigBrain markdown/content <-> Notion page content)

### Suggested files
- `src/bigbrain/compile/notion_models.py`
- `src/bigbrain/sync/notion_mapping.py`
- `src/bigbrain/sync/notion_mcp_adapter.py`

### Acceptance criteria
- page sync inputs/outputs are stable and explicit
- sync state is represented in a reusable contract
- mapper/adapters are deterministic across repeated round-trips

---

## Workstream B - Outbound Publish

### Tasks
- [ ] Implement Notion MCP page publish client/service
- [ ] Preserve source links and metadata
- [ ] Support idempotent or update-aware publishing
- [ ] Add retry behavior for transient failures
- [ ] Add preflight MCP auth/capability check before publishing
- [ ] Add target page routing (`--page`) with default output page `Big Brain`

### Suggested files
- `src/bigbrain/compile/notion_compiler.py`
- `src/bigbrain/sync/notion_publish.py`

### Acceptance criteria
- summaries can be published to Notion pages
- repeated publishes do not create uncontrolled duplication
- publish failures are actionable and retryable
- each local artifact has stable remote page mapping after first publish
- when no explicit target is provided, publish defaults to Notion page `Big Brain`

---

## Workstream C - Inbound Pull and Reconciliation

### Tasks
- [ ] Implement Notion MCP page fetch/re-ingest flow
- [ ] Map remote page updates back into KB-compatible structures
- [ ] Preserve provenance and sync state
- [ ] Add reconciliation hooks for local/remote divergence
- [ ] Track last pulled remote revision marker for incremental pull

### Suggested files
- `src/bigbrain/sync/notion_pull.py`
- `src/bigbrain/ingest/notion_ingester.py`

### Acceptance criteria
- previously synced pages can be re-imported
- page changes are visible to the KB layer
- reconciliation flow is deterministic
- incremental pull skips unchanged remote pages safely

---

## Workstream D - Sync State and Conflict Handling

### Tasks
- [ ] Persist sync metadata/state
- [ ] Detect conflicts using timestamps/version markers/content hashes
- [ ] Define retry strategy and user-facing conflict reporting
- [ ] Add sync audit logging
- [ ] Define explicit policy for conflict resolution (`last-write-wins` or manual)

### Suggested files
- `src/bigbrain/sync/notion_state.py`
- `src/bigbrain/sync/notion_conflicts.py`

### Acceptance criteria
- sync state survives across runs
- conflicts are visible and actionable
- retries do not hide permanent failures
- conflict policy is documented and applied consistently by CLI flows

---

## Workstream E - CLI, Docs, and Validation

### Tasks
- [ ] Wire Notion sync commands/flags into CLI
- [ ] Update config example with Notion settings
- [ ] Add publish/pull/conflict fixtures or mocks
- [ ] Update README and AGENTS guidance
- [ ] Add operator commands for dry-run and status (`sync status`, `sync push`, `sync pull`, `sync reconcile`)
- [ ] Document/implement `sync push --page <page>` target override and default page behavior

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
- dry-run/reporting output is sufficient to troubleshoot failed sync runs

---

## Definition of Done for Phase 6

- [ ] Notion page mapping contracts exist
- [ ] summaries can be published to Notion pages
- [ ] previously synced pages can be re-ingested
- [ ] sync metadata and conflicts are tracked
- [ ] sync CLI flows are usable
- [ ] tests/docs cover page-level bidirectional sync
- [ ] MCP-based preflight checks and retry behavior are implemented

---

## Risks and Mitigations

- [ ] MCP auth/token/session expiry handling validated with clear recovery guidance
- [ ] MCP schema drift risk addressed via adapter layer and contract tests
- [ ] rate limiting/backoff policy validated for publish and pull loops
- [ ] markdown/block round-trip loss characterized with known limitations documented
- [ ] duplicate mapping race conditions covered by idempotent upsert rules

---

## Recommended First Commit Slice

### Slice 0
- close Phase 5 output/config blockers

### Slice 1
- sync contracts
- mapping rules
- MCP adapters

### Slice 2
- outbound MCP publish + preflight

### Slice 3
- inbound MCP reconciliation
- sync state/conflicts

### Slice 4
- CLI/docs/tests
- risk hardening and recovery docs

