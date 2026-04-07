# BigBrain Phase 9 Implementation Task List
<!-- PLAN:TEMPLATE v1 -->
<!-- PLAN:SOURCE .github/plan/_phase-task-template.md -->


## Goal

Implement **audio and rich UX** features:
- podcast script generation
- optional podcast audio generation
- UI/visualization surfaces for browsing and operating the knowledge base

---

## Parallelization Strategy

After shared presentation contracts are defined, these streams can progress largely in parallel:
- podcast script generation
- text-to-speech/audio generation
- UI backend/read models
- UI frontend shell and graph views
- docs and validation assets

---

## Scope Boundaries

### In scope
- podcast script generation
- optional TTS/audio generation
- UI read models/endpoints as needed
- UI browsing and provenance visualization

### Out of scope
- release automation
- advanced enterprise auth/hosting for UI
- unrelated cloud deployment work

---

## Phase 4–8 Carry-Over Issues / Preconditions

- [ ] stable compiled outputs exist for scripts/UX views
- [ ] search/status APIs exist for UI read models
- [ ] study output/summary artifacts are stable enough to present

### Minimum preflight acceptance criteria
- there is enough structured data to drive scripts and UI browsing
- audio generation can be optional without blocking script generation

---

## Recommended Implementation Order

0. Close read-model/output blockers
1. Define script/audio/UI presentation contracts
2. Implement script generation
3. Implement optional TTS/audio flow
4. Implement UI read models and shell
5. Add visualization/provenance views
6. Add docs and validation assets

---

## Workstream A - Podcast Script Generation

### Tasks
- [ ] define podcast script artifact contract
- [ ] implement script generation from compiled knowledge
- [ ] include duration estimates and speaker markers
- [ ] support script-only CLI flow

### Suggested files
- `src/bigbrain/compile/podcast_script_compiler.py`

### Acceptance criteria
- scripts are conversational and structurally predictable
- script generation works without requiring audio generation

---

## Workstream B - Audio / TTS Generation

### Tasks
- [ ] define audio generation contract
- [ ] add optional TTS dependency/integration
- [ ] support WAV/MP3 or chosen output format
- [ ] expose voice/config settings
- [ ] keep failures optional/non-blocking

### Suggested files
- `src/bigbrain/compile/podcast_audio.py`

### Acceptance criteria
- audio generation is optional and modular
- script generation remains usable if audio generation is unavailable

---

## Workstream C - UI Read Models and Backend Surface

### Tasks
- [ ] define read models for documents/chunks/entities/relationships/artifacts
- [ ] add backend service endpoints or local APIs as needed
- [ ] expose search/status/provenance views

### Suggested files
- `src/bigbrain/ui/read_models.py`
- `src/bigbrain/ui/service.py`

### Acceptance criteria
- UI can browse existing knowledge artifacts without redefining backend contracts
- provenance/search/status data is accessible for visualization

---

## Workstream D - UI Shell and Visualization

### Tasks
- [ ] implement browsing shell
- [ ] add document/chunk/entity views
- [ ] add graph/provenance visualizations
- [ ] add pipeline trigger/status surfaces if appropriate

### Suggested files
- `ui/` or chosen frontend location

### Acceptance criteria
- UI makes KB contents easier to browse than raw files alone
- key knowledge structures are visible and navigable

---

## Workstream E - Docs, Fixtures, and UX Validation

### Tasks
- [ ] add script fixtures and expected outputs
- [ ] add audio smoke validation where possible
- [ ] document optional dependency behavior
- [ ] document UI usage and limitations

### Acceptance criteria
- optional features are clearly documented
- script/audio/UI behaviors are validated enough to iterate safely

---

## Definition of Done for Phase 9

- [ ] podcast script generation works
- [ ] audio generation is optional and functional when enabled
- [ ] UI can browse core knowledge artifacts
- [ ] provenance/search/status are visible in UX surfaces
- [ ] docs and validation assets exist for the new user-facing features

---

## Recommended First Commit Slice

### Slice 0
- close artifact/read-model blockers

### Slice 1
- script contracts and generation

### Slice 2
- optional audio generation

### Slice 3
- UI read models/backend
- UI shell/visualization

### Slice 4
- docs/tests/smoke validation

