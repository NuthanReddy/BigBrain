# BigBrain Phase 0 Implementation Task List
<!-- PLAN:TEMPLATE v1 -->
<!-- PLAN:SOURCE .github/plan/_phase-task-template.md -->


## Goal

Turn the current single-file prototype into a structured, installable, runnable CLI foundation without implementing Phase 1+ features yet.

Phase 0 is complete when the repository has:
- a stable `src/` package layout
- a thin `main.py` entry point
- a scaffolded CLI with discoverable commands
- config loading conventions
- shared logging setup
- packaging metadata for `src` layout
- starter docs that match reality

---

## Scope Boundaries

### In scope
- project/package structure
- CLI scaffolding
- config scaffolding
- logging scaffolding
- packaging updates
- docs updates
- placeholder modules for later phases

### Out of scope
- real ingestion behavior
- KB persistence logic
- provider runtime logic
- summary generation
- Notion sync
- search/indexing implementation

---

## Recommended Implementation Order

1. Create the package structure
2. Move entry orchestration into a CLI module
3. Add command scaffolding and `--help`
4. Add config loading and sample config
5. Add centralized logging and CLI error handling
6. Update packaging metadata in `pyproject.toml`
7. Add README + update `AGENTS.md`
8. Smoke-test the CLI surface

---

## Workstream A - Foundation and Repository Layout

### Tasks
- [ ] Keep `main.py` as the executable entry point only
- [ ] Create `src/bigbrain/` as the package root
- [ ] Add package placeholders:
  - [ ] `src/bigbrain/orchestrator/__init__.py`
  - [ ] `src/bigbrain/ingest/__init__.py`
  - [ ] `src/bigbrain/kb/__init__.py`
  - [ ] `src/bigbrain/distill/__init__.py`
  - [ ] `src/bigbrain/compile/__init__.py`
- [ ] Add core Phase 0 modules:
  - [ ] `src/bigbrain/__init__.py`
  - [ ] `src/bigbrain/cli.py`
  - [ ] `src/bigbrain/config.py`
  - [ ] `src/bigbrain/logging_config.py`
- [ ] Add `config/` directory for sample settings
- [ ] Add `docs/` directory for future architecture notes if needed

### Acceptance criteria
- Imports resolve from `src` layout cleanly
- `main.py` no longer contains business logic
- Future phase folders exist and match the roadmap

---

## Workstream B - CLI Foundation

### Tasks
- [ ] Define one CLI entry function in `src/bigbrain/cli.py`
- [ ] Add root command help text
- [ ] Add scaffolded command groups:
  - [ ] `ingest`
  - [ ] `distill`
  - [ ] `compile`
  - [ ] `update`
  - [ ] `status`
  - [ ] `kb-search`
- [ ] Add baseline arguments where appropriate
- [ ] Return friendly “not implemented yet” messages for stubbed commands
- [ ] Ensure command structure can be extended without replacing parser logic later

### Suggested command scaffold
```text
bigbrain
├── ingest
├── distill
├── compile
├── update
├── status
└── kb-search
```

### Acceptance criteria
- `python main.py --help` works
- subcommands are visible in help output
- stubbed commands fail gracefully without stack traces
- CLI surface matches the roadmap terminology

---

## Workstream C - Config and Environment Conventions

### Tasks
- [ ] Define a Phase 0 settings model in `src/bigbrain/config.py`
- [ ] Support config loading from YAML
- [ ] Support environment variable overrides
- [ ] Establish env naming convention, e.g. `BIGBRAIN_*`
- [ ] Create `config/example.yaml`
- [ ] Reserve config sections for later phases:
  - [ ] `app`
  - [ ] `logging`
  - [ ] `paths`
  - [ ] `providers`
  - [ ] `ingestion`
  - [ ] `distillation`
  - [ ] `kb`
- [ ] Add placeholder provider config keys for:
  - [ ] GitHub Copilot Enterprise
  - [ ] Ollama
  - [ ] LM Studio

### Acceptance criteria
- config load order is documented and deterministic
- missing optional config falls back to sane defaults
- provider structure is reserved without implementing provider logic yet

### Suggested precedence
1. built-in defaults
2. YAML config file
3. environment variables
4. CLI flags, if added later

---

## Workstream D - Logging and Error Handling

### Tasks
- [ ] Add centralized logging setup in `src/bigbrain/logging_config.py`
- [ ] Define a default console log format
- [ ] Define default log levels
- [ ] Initialize logging once at CLI startup
- [ ] Add top-level exception handling around CLI execution
- [ ] Distinguish user-facing errors from unexpected internal errors
- [ ] Reserve extension points for file/structured logging later

### Acceptance criteria
- every module can obtain a logger through one shared pattern
- startup configures logging exactly once
- user-facing failures are concise and predictable
- stack traces are not shown for normal command misuse

---

## Workstream E - Packaging and Entry Points

### Tasks
- [ ] Update `pyproject.toml` description to match the project
- [ ] Configure package discovery for `src` layout
- [ ] Add only minimal Phase 0 dependencies
- [ ] Add a console script entry point such as `bigbrain`
- [ ] Keep `main.py` runnable directly for local development
- [ ] Avoid adding Phase 1+ dependencies in Phase 0 unless required for scaffolding

### Acceptance criteria
- package metadata matches the current implementation state
- the app can be invoked through a canonical CLI entry point
- dependencies remain minimal and Phase-0-scoped

---

## Workstream F - Documentation and Contributor Guidance

### Tasks
- [ ] Create `README.md`
- [ ] Document what Phase 0 includes vs what is deferred
- [ ] Document how to run the CLI
- [ ] Document config discovery and override behavior
- [ ] Document current scaffolded commands
- [ ] Update `AGENTS.md` to reflect the new structure and workflows
- [ ] Add a short architecture note showing where later phases will land

### Acceptance criteria
- a new contributor can run the CLI from the repo root
- docs match the actual file structure and command surface
- `AGENTS.md` is no longer describing a single-file-only app

---

## Suggested Phase 0 File Structure

```text
BigBrain/
├── .github/
│   └── plan/
│       ├── idea and phases.md
│       └── phase-0-implementation-task-list.md
├── config/
│   └── example.yaml
├── docs/
├── src/
│   └── bigbrain/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── logging_config.py
│       ├── orchestrator/
│       │   └── __init__.py
│       ├── ingest/
│       │   └── __init__.py
│       ├── kb/
│       │   └── __init__.py
│       ├── distill/
│       │   └── __init__.py
│       └── compile/
│           └── __init__.py
├── AGENTS.md
├── README.md
├── main.py
└── pyproject.toml
```

---

## Definition of Done for Phase 0

Phase 0 is done when all of the following are true:
- [ ] `python main.py --help` succeeds
- [ ] all planned top-level subcommands exist as CLI scaffolds
- [ ] `src/bigbrain/` is the stable package root
- [ ] config loading exists with example configuration
- [ ] centralized logging is initialized from the CLI path
- [ ] packaging metadata supports the `src` layout
- [ ] `README.md` exists and is accurate
- [ ] `AGENTS.md` reflects the new architecture
- [ ] no Phase 1+ implementation details are required for the foundation to run

---

## Suggested Validation Commands

```powershell
python .\main.py --help
python .\main.py ingest --help
python .\main.py distill --help
python .\main.py compile --help
python .\main.py status
```

---

## Recommended First Commit Slice

If you want to implement Phase 0 incrementally, use this order:

### Slice 1
- package structure
- thin `main.py`
- `cli.py` root parser

### Slice 2
- command scaffolding
- help text
- graceful not-implemented paths

### Slice 3
- config loading
- sample config
- env override pattern

### Slice 4
- logging setup
- top-level error handling

### Slice 5
- packaging updates
- README
- `AGENTS.md`

---

## Notes for Phase 1 Handoff

Phase 1 should build on this foundation by attaching real handlers to the existing `ingest` command group instead of redesigning the CLI.

Specifically, the first Phase 1 implementations should plug into:
- `src/bigbrain/cli.py` for command wiring
- `src/bigbrain/config.py` for path/provider/config access
- `src/bigbrain/logging_config.py` for logger setup
- `src/bigbrain/ingest/` for TXT/Markdown/PDF/Python ingestion logic

