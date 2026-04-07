# BigBrain Phase 4 Implementation Task List
<!-- PLAN:TEMPLATE v1 -->
<!-- PLAN:SOURCE .github/plan/_phase-task-template.md -->


## Goal

Implement the **distillation pipeline** that transforms stored raw documents into reusable knowledge units, with summaries as the first polished user-facing artifact.

## Validation Snapshot (2026-04-08)

- Status key: `[x] done`, `[ ] pending/partial`
- Validation basis: code + tests in `src/bigbrain/distill/`, `src/bigbrain/cli.py`, `src/bigbrain/kb/store.py`, and `tests/test_distill.py`
- Overall: Phase 4 is largely implemented and usable end-to-end; remaining gaps are mostly around explicit normalization and summary-mode/quality controls.

---

## Parallelization Strategy

After shared distillation contracts are defined, the following can proceed in parallel:
- chunking and normalization
- extractive summarization
- abstractive summarization orchestration
- entity extraction
- relationship building
- pipeline assembly/evaluation

---

## Scope Boundaries

### In scope
- distillation contracts and outputs
- chunking and normalization
- summary-first processing
- entity extraction
- relationship building
- provider-aware pipeline execution
- evaluation fixtures and quality checks

### Out of scope
- final summary rendering/Markdown compilation
- Notion sync
- advanced UI

---

## Phase 2–3 Carry-Over Issues / Preconditions

- [x] KB store APIs exist for reading source documents and writing distilled artifacts later
- [x] provider layer exists and is invocable through one routing path
- [x] provenance metadata is available from upstream phases

### Minimum preflight acceptance criteria
- stored documents can be fetched reliably for distillation
- one provider-backed invocation path exists for summary-capable tasks

---

## Recommended Implementation Order

0. Close Phase 2–3 blockers
1. Define distillation contracts and artifact shapes
2. Implement chunking and normalization
3. Implement extractive summarization
4. Implement abstractive summarization orchestration
5. Implement entity extraction and relationship building
6. Assemble the pipeline and evaluation harness
7. Add docs and fixture validation

---

## Workstream A - Distillation Contracts

### Tasks
- [x] Define models for chunks, summaries, entities, and relationships
- [x] Define provenance fields linking outputs back to source docs/chunks
- [x] Define confidence metadata and quality markers
- [x] Define pipeline configuration contract

### Suggested files
- `src/bigbrain/distill/models.py`
- `src/bigbrain/distill/config_models.py`

### Acceptance criteria
- all distillation outputs follow stable contracts
- later compilation can consume outputs without reinterpreting raw provider responses

---

## Workstream B - Chunking and Normalization

### Tasks
- [x] Implement chunking strategies
- [x] Implement overlap rules
- [ ] Implement normalization rules for text cleanup *(no dedicated `normalizer.py` yet)*
- [x] Preserve source offsets or section references

### Suggested files
- `src/bigbrain/distill/chunker.py`
- `src/bigbrain/distill/normalizer.py`

### Acceptance criteria
- chunks are deterministic for the same input and config
- normalized text remains traceable to original source positions

---

## Workstream C - Summary Generation

### Tasks
- [ ] Implement extractive summary generation *(provider summary exists; no standalone extractive algorithm yet)*
- [x] Implement abstractive summary orchestration via Phase 3 provider layer
- [ ] Support `extractive`, `abstractive`, and `both` modes
- [ ] Add quality heuristics or validation checks

### Suggested files
- `src/bigbrain/distill/summarizer.py`
- `src/bigbrain/distill/pipeline.py`

### Acceptance criteria
- summaries are generated in the configured mode
- output remains linked to source chunks
- summary generation can run through the provider layer predictably

---

## Workstream D - Entity Extraction and Relationships

### Tasks
- [x] Implement entity extraction rules/provider-assisted flow
- [x] Implement relationship-building logic
- [ ] Define confidence thresholds *(relationship confidence field exists; thresholding policy/config not defined)*
- [x] Add deduping/normalization for repeated entities

### Suggested files
- `src/bigbrain/distill/entity_extractor.py`
- `src/bigbrain/distill/relationship_builder.py`

### Acceptance criteria
- entities and relationships are structured and attached to distilled outputs
- confidence metadata exists for extracted items

---

## Workstream E - Pipeline Orchestration and Evaluation

### Tasks
- [x] Assemble the distillation pipeline over stored documents
- [x] Add pipeline-level reporting and counts
- [ ] Add evaluation fixtures and golden outputs where practical *(broad pytest coverage exists; golden fixtures are still pending)*
- [x] Add CLI integration for `distill`

### Suggested files
- `src/bigbrain/distill/pipeline.py`
- `src/bigbrain/cli.py`
- `tests/distill/`

### Acceptance criteria
- the pipeline can process stored documents end-to-end
- CLI execution produces useful summaries and metadata
- evaluation fixtures catch regressions in chunking/summaries/entities

---

## Definition of Done for Phase 4

- [x] stable distillation models exist
- [ ] chunking and normalization work *(normalization module still pending)*
- [ ] summary-first output is generated in configured modes *(mode switching not yet implemented)*
- [x] entities and relationships are extracted with metadata
- [x] outputs preserve provenance to source chunks
- [x] `distill` CLI execution is usable
- [x] fixtures/tests cover major paths

---

## Additional Achieved Tasks (Beyond Original Checklist)

- [x] Incremental distillation with chunk hash comparison (`KBStore.get_chunk_hashes` + `DistillPipeline` skip logic)
- [x] Parallel execution within document processing (summary and entity extraction in parallel)
- [x] Parallel execution across documents with configurable worker pool (`distill --workers`)
- [x] Partial-step execution support (`distill --step summarize|entities|relationships`)
- [x] Distillation inspection and maintenance CLI commands:
  - `distill-show` for persisted summaries/entities/relationships
  - `entities` for filtering/listing entity inventory
  - `compact` for KB entity deduplication

---

## Recommended First Commit Slice

### Slice 0
- close Phase 2–3 blockers

### Slice 1
- distillation models
- config contracts

### Slice 2
- chunking
- normalization

### Slice 3
- extractive summary flow
- abstractive orchestration

### Slice 4
- entity extraction
- relationship building
- pipeline/CLI/tests

