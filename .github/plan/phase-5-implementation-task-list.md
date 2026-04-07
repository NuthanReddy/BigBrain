# BigBrain Phase 5 Implementation Task List

## Goal

Implement the **summary compilation MVP** so distilled outputs become readable, structured, reusable summary documents, primarily in Markdown.

---

## Parallelization Strategy

After output contracts are defined, these can proceed mostly independently:
- output models and grouping rules
- Markdown rendering/templates
- source attribution/provenance formatting
- CLI/reporting integration
- fixtures/snapshot validation

---

## Scope Boundaries

### In scope
- summary output contracts
- topic grouping and merge rules
- Markdown compilation
- source attribution and timestamps
- compilation reporting and CLI wiring
- snapshot-style validation

### Out of scope
- Notion sync
- study outputs like flashcards/Q&A
- audio generation

---

## Phase 4 Carry-Over Issues / Preconditions

- [ ] distilled outputs are stable and queryable
- [ ] provenance metadata exists
- [ ] summary artifacts have enough structure for grouping/rendering

### Minimum preflight acceptance criteria
- Phase 4 produces summaries and metadata consistently
- the compiler can read distilled outputs without re-calling providers

---

## Recommended Implementation Order

0. Close Phase 4 output-shape blockers
1. Define compilation contracts
2. Implement grouping/merge strategy
3. Implement Markdown rendering
4. Implement attribution and source contribution sections
5. Wire `compile` CLI flow
6. Add snapshot validation and docs

---

## Workstream A - Compilation Contracts

### Tasks
- [ ] Define compiled summary artifact models
- [ ] Define topic grouping and hierarchy fields
- [ ] Define merge/ordering rules
- [ ] Define artifact metadata (timestamps, source counts, etc.)

### Suggested files
- `src/bigbrain/compile/models.py`

### Acceptance criteria
- compiled outputs have stable structure and metadata
- merge/grouping rules are deterministic

---

## Workstream B - Topic Grouping and Merge Logic

### Tasks
- [ ] Group summaries by topic/source rules
- [ ] Define ordering rules within compiled outputs
- [ ] Avoid duplicate topic output paths
- [ ] Preserve source contribution visibility

### Suggested files
- `src/bigbrain/compile/grouping.py`
- `src/bigbrain/compile/summary_service.py`

### Acceptance criteria
- topic grouping is predictable
- duplicate output paths/topics are handled cleanly
- multi-source merged summaries retain source visibility

---

## Workstream C - Markdown Rendering

### Tasks
- [ ] Implement Markdown renderer for summaries
- [ ] Preserve code blocks and technical formatting
- [ ] Render attribution inline or in footnotes
- [ ] Add timestamps and contributing-source sections

### Suggested files
- `src/bigbrain/compile/markdown_compiler.py`
- `src/bigbrain/compile/renderers.py`

### Acceptance criteria
- Markdown output is readable without inspecting raw sources
- technical content formats correctly
- attribution and timestamps are present

---

## Workstream D - CLI, Reporting, and Output Paths

### Tasks
- [ ] Wire summary compilation into the `compile` CLI group
- [ ] Add output path handling
- [ ] Print concise compile summaries
- [ ] Handle empty/distillation-missing input cases cleanly

### Suggested files
- `src/bigbrain/cli.py`
- `src/bigbrain/compile/summary_service.py`

### Acceptance criteria
- `compile` CLI can produce real Markdown output
- output paths and reports are understandable
- missing prerequisites fail with actionable errors

---

## Workstream E - Snapshot Validation and Docs

### Tasks
- [ ] Add snapshot-style tests for Markdown output
- [ ] Add multi-source merge fixtures
- [ ] Update docs with compile usage
- [ ] Update `AGENTS.md` if compile architecture becomes more concrete

### Suggested files
- `tests/compile/`
- `tests/fixtures/compile/`
- `README.md`
- `AGENTS.md`

### Acceptance criteria
- output regressions are catchable by tests
- docs reflect the real compile surface

---

## Definition of Done for Phase 5

- [ ] compiled summary artifact contracts exist
- [ ] topic grouping and merge logic work
- [ ] Markdown output is readable and attributed
- [ ] compile CLI is usable
- [ ] snapshot/fixture validation exists
- [ ] docs describe the summary compilation MVP accurately

---

## Recommended First Commit Slice

### Slice 0
- close Phase 4 output blockers

### Slice 1
- compile models
- grouping rules

### Slice 2
- Markdown renderer
- attribution/timestamps

### Slice 3
- CLI/output path handling
- fixtures/snapshots/docs

