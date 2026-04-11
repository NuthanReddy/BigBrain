# BigBrain Implementation Backlog — BB-01 … BB-10

> Generated 2026-04-11 · Based on codebase audit of current `master`

---

## Week 1 — Foundations & Quick Wins

| ID | Task | Owner | Est | Deps | Status |
|----|------|-------|-----|------|--------|
| **BB-08** | **Secret / config hygiene** | Security / Backend | **S** | — | ⬜ |
| **BB-05** | **Shared HTTP client in providers** | Backend Dev | **S** | — | ⬜ |
| **BB-07** | **KBStore N+1 optimization** | Backend Dev | **S** | — | ⬜ |
| **BB-04** | **Pipeline lifecycle hardening** | Backend Dev | **S** | — | ⬜ |
| **BB-10** | **CONTRIBUTING + pre-commit + dev docs** | Tech Lead / Docs | **S** | — | ⬜ |
| **BB-01** | **Modularize CLI** | Backend Dev | **L** | — | ⬜ |

### Week 1 rationale
Four **S** tasks land quick, visible improvements with no cross-dependencies.  
BB-10 unblocks BB-02 (CI needs lint/test config to validate).  
BB-01 starts early because it's the longest lead item and unblocks BB-03.

---

## Week 2 — Quality Gates & Depth

| ID | Task | Owner | Est | Deps | Status |
|----|------|-------|-----|------|--------|
| **BB-02** | **CI quality gates** | DevOps / Platform | **M** | BB-10 | ⬜ |
| **BB-03** | **CLI & digest builder tests** | QA / Backend Dev | **L** | BB-01 | ⬜ |
| **BB-06** | **Structured run observability** | Backend Dev | **M** | BB-04 | ⬜ |
| **BB-09** | **Plugin trust / allowlist** | Backend Dev | **M** | — | ⬜ |

### Week 2 rationale
BB-02 and BB-03 depend on Week 1 deliverables (dev docs, modular CLI).  
BB-06 layers observability on top of the hardened pipelines from BB-04.  
BB-09 is independent but lower priority — scheduled after core stability work.

---

## Task Details

### BB-01 · Modularize `cli.py` → command modules · **L**
| Field | Value |
|-------|-------|
| **Current state** | 2 750 lines, 19 subcommands, all `_handle_*` in one file |
| **Owner** | Backend Dev |
| **Plan** | Split into `src/bigbrain/cli/` package: `__init__.py` (build_parser + main), `ingest.py`, `digest.py`, `wiki.py`, `notion.py`, `providers.py`, `kb.py`, `auth.py`, `plugins.py`, `orchestrator.py` |
| **Acceptance** | `cli.py` → `cli/__init__.py` < 200 lines · each module owns its `_add_*_parser` + `_handle_*` · all 642 tests pass · `bigbrain --help` unchanged |

### BB-02 · CI quality gates · **M**
| Field | Value |
|-------|-------|
| **Current state** | No `.github/workflows/`, no tool config in `pyproject.toml` |
| **Owner** | DevOps / Platform |
| **Deps** | BB-10 (pre-commit + tool config must exist first) |
| **Plan** | `.github/workflows/ci.yml`: matrix Python 3.10/3.12, steps: `pip install -e .[dev]`, `ruff check`, `mypy src/`, `pytest --cov`, `pip-audit`. Add `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]` to `pyproject.toml`. |
| **Acceptance** | CI green on PR · ruff + mypy zero errors · coverage report uploaded · pip-audit runs (informational) |

### BB-03 · Expand CLI & digest builder tests · **L**
| Field | Value |
|-------|-------|
| **Current state** | 0 CLI tests, 0 digest builder tests (29 test files elsewhere) |
| **Owner** | QA / Backend Dev |
| **Deps** | BB-01 (modular CLI is easier to unit-test) |
| **Plan** | `tests/test_cli.py`: subcommand dispatch, `--help` smoke, arg validation, `UserError` display, `--doc-id` prefix resolution. `tests/digest/test_builder.py`: chapter detection from TOC, font-based heading, SVG extraction mock, `--no-ai` full path, incremental hash skip. |
| **Acceptance** | 50+ new tests · 80%+ line coverage for `cli/` and `digest/builder.py` · CI green |

### BB-04 · Harden pipeline lifecycle / resource cleanup · **S**
| Field | Value |
|-------|-------|
| **Current state** | `Orchestrator` and `DistillPipeline` have `close()` / `__enter__/__exit__` but inner steps lack `try/finally` |
| **Owner** | Backend Dev |
| **Plan** | Wrap `run()`, `_run_ingest()`, `_run_distill()`, `_run_compile()` in `try/finally`. Ensure `ThreadPoolExecutor.shutdown(wait=False)` on interrupt. Add `atexit.register(close_http_client)`. |
| **Acceptance** | Ctrl+C during `bigbrain update` releases all DB/HTTP/thread resources · no leaked threads on exception |

### BB-05 · Shared pooled HTTP client in providers · **S**
| Field | Value |
|-------|-------|
| **Current state** | `bigbrain.http` has singleton client but providers call `httpx.get/post` directly |
| **Owner** | Backend Dev |
| **Plan** | Replace `httpx.get()`/`httpx.post()` in `ollama.py`, `lm_studio.py`, `github_copilot.py` with `get_http_client().get()`/`.post()`. Add `limits=httpx.Limits(max_connections=20)` to shared client. |
| **Acceptance** | All provider HTTP goes through shared client · connection reuse confirmed via `httpx` debug logs · all tests pass |

### BB-06 · Structured run observability · **M**
| Field | Value |
|-------|-------|
| **Current state** | `JsonFormatter` exists in logging_config but no run-scoped timing/counters/correlation |
| **Owner** | Backend Dev |
| **Deps** | BB-04 (cleanup must be solid before adding instrumentation) |
| **Plan** | Add `RunContext` dataclass (run_id, step_name, start_time, counters). Emit structured JSON log events: `pipeline.step.start`, `pipeline.step.end`, `provider.fallback`, `provider.error`. Add `--run-id` CLI flag for external correlation. |
| **Acceptance** | `bigbrain update` emits start/end/error JSON events per step with elapsed_ms · fallback events include from/to provider · `--run-id` appears in all log lines |

### BB-07 · KBStore list/search N+1 fix · **S**
| Field | Value |
|-------|-------|
| **Current state** | `_row_to_document()` runs 1 `SELECT sections` per document → N+1 on every list/search |
| **Owner** | Backend Dev |
| **Plan** | Add `_batch_load_sections(doc_ids)` with single `WHERE document_id IN (...)` query. Add `include_sections=False` param to `list_documents()`/`search_documents()` for metadata-only paths (status, kb-search preview). |
| **Acceptance** | `list_documents(100)` drops from ~101 queries to 2 · `status` command measurably faster on 500+ doc KB |

### BB-08 · Secret / config hygiene · **S**
| Field | Value |
|-------|-------|
| **Current state** | `example.yaml` has `bigbrain123` password · `data/kb/` not in `.gitignore` · config display shows secrets in cleartext |
| **Owner** | Security / Backend Dev |
| **Plan** | Replace password in `example.yaml` with `${BIGBRAIN_POSTGRES_URL}` placeholder. Add `data/` and `*.db` to `.gitignore`. Mask `*_token`, `*_password`, `*_api_key` fields in `status --config` output. Support `BIGBRAIN_POSTGRES_URL` env var. |
| **Acceptance** | `git grep -i password` returns only placeholders · `.gitignore` covers `data/` · `bigbrain status` masks secrets with `***` |

### BB-09 · Plugin trust / allowlist · **M**
| Field | Value |
|-------|-------|
| **Current state** | `discovery.py` runs `exec_module()` on any `.py` in plugins dir; only enable/disable filter exists |
| **Owner** | Backend Dev |
| **Plan** | Add `plugins.trusted_paths` (list of allowed directories) and `plugins.trusted_entry_points` (allowed prefixes) to config. Log `WARNING` + skip on untrusted source. Add `--trust-unsigned` CLI flag to override. Validate `PluginInfo` fields (name, version non-empty). |
| **Acceptance** | Plugin from untrusted dir → warning + skip · `--trust-unsigned` loads it · `PluginInfo` validation rejects empty name/version |

### BB-10 · CONTRIBUTING + pre-commit + dev docs · **S**
| Field | Value |
|-------|-------|
| **Current state** | No `CONTRIBUTING.md`, no `.pre-commit-config.yaml`, README has CLI docs only |
| **Owner** | Tech Lead / Docs |
| **Plan** | Create `CONTRIBUTING.md` (clone, venv, `pip install -e .[dev]`, `pytest`, `ruff check`, commit message format). Create `.pre-commit-config.yaml` (ruff, ruff-format, trailing-whitespace, end-of-file-fixer). Add "Development" section to `README.md`. |
| **Acceptance** | New contributor can set up + test + lint in < 5 min following CONTRIBUTING · `pre-commit run --all-files` passes · README links to CONTRIBUTING |

---

## Dependency Graph

```
BB-10 ──→ BB-02
BB-01 ──→ BB-03
BB-04 ──→ BB-06

BB-05, BB-07, BB-08, BB-09  (independent)
```

## Estimates Key
| Size | Effort | Typical |
|------|--------|---------|
| **S** | ½–1 day | Single file or config change |
| **M** | 2–3 days | Multi-file, moderate testing |
| **L** | 4–5 days | Major refactor or 50+ new tests |
