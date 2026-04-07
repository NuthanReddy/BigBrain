# BigBrain Phase 3 Implementation Task List
<!-- PLAN:TEMPLATE v1 -->
<!-- PLAN:SOURCE .github/plan/_phase-task-template.md -->


## Goal

Implement the **AI provider layer** that supports:
- GitHub Copilot Enterprise as the primary provider
- Ollama as a required local provider
- LM Studio as a required local provider
- optional configured default/override plus automatic fallback

This phase should deliver provider abstractions and routing, but should not own the summary logic itself.

---

## Parallelization Strategy

After provider contracts are finalized, the work splits well into parallel streams:
- GitHub auth/bootstrap
- GitHub provider adapter
- Ollama adapter
- LM Studio adapter
- routing/fallback/telemetry
- CLI/config integration and fixture validation

---

## Scope Boundaries

### In scope
- provider abstraction/interfaces
- request/response contracts
- provider configuration
- first-run GitHub authentication bootstrap
- provider adapters
- fallback policy and routing
- provider metadata and observability

### Out of scope
- distillation algorithms
- prompt design for every future task type
- Notion sync
- UI

---

## Phase 2 Carry-Over Issues / Preconditions

- [ ] KB/document contracts used by later phases are stable enough for provider consumers
- [ ] config system supports provider sections
- [ ] logging and `UserError` patterns are stable
- [ ] CLI has a consistent place for provider-related options or status

### Minimum preflight acceptance criteria
- Phase 0 and 2 config/logging/CLI conventions are reusable
- provider configuration can be loaded without special-case hacks

---

## Recommended Implementation Order

0. Close Phase 0/2 config and contract blockers
1. Finalize provider contracts
2. Implement GitHub auth/bootstrap
3. Implement provider adapters in parallel
4. Implement routing/fallback policy
5. Add CLI/config/status integration
6. Add provider-level tests, mocks, and docs

---

## Workstream A - Provider Contracts

### Tasks
- [ ] Define provider interface(s)
- [ ] Define request/response contracts
- [ ] Define provider capability metadata
- [ ] Define error categories and retryability metadata
- [ ] Define provenance fields to record provider/model usage

### Suggested files
- `src/bigbrain/providers/base.py`
- `src/bigbrain/providers/models.py`

### Acceptance criteria
- every provider adapter implements the same contract
- provider outputs can be consumed uniformly by later phases
- error and capability metadata are explicit

---

## Workstream B - GitHub Authentication and Bootstrap

### Tasks
- [ ] Define first-run GitHub authentication flow
- [ ] Define storage/loading of auth state or tokens per config rules
- [ ] Add startup validation for authenticated setup
- [ ] Add user-facing remediation for failed auth
- [ ] Keep auth isolated from future prompt logic

### Suggested files
- `src/bigbrain/providers/github_auth.py`
- `src/bigbrain/config.py`
- `src/bigbrain/cli.py`

### Acceptance criteria
- first-run auth is enforced as designed
- auth failures are actionable and clean
- the auth layer is separable from provider invocation logic

---

## Workstream C - GitHub Copilot Enterprise Adapter

### Tasks
- [ ] Implement provider adapter for GitHub-backed runtime usage
- [ ] Map provider-specific settings into the shared contract
- [ ] Handle rate limits, transient failures, and capability reporting
- [ ] Emit provenance and logging data

### Suggested files
- `src/bigbrain/providers/github_provider.py`

### Acceptance criteria
- the adapter satisfies the provider contract
- failures are surfaced through shared error handling
- provider usage is observable in logs/metadata

---

## Workstream D - Ollama Adapter

### Tasks
- [ ] Implement local endpoint client
- [ ] Support capability probing and health checks
- [ ] Map local settings into the shared contract
- [ ] Emit provenance and logging data

### Suggested files
- `src/bigbrain/providers/ollama_provider.py`

### Acceptance criteria
- local Ollama execution works through the shared interface
- capability/availability checks are exposed to the router

---

## Workstream E - LM Studio Adapter

### Tasks
- [ ] Implement local endpoint client
- [ ] Support capability probing and health checks
- [ ] Map LM Studio settings into the shared contract
- [ ] Emit provenance and logging data

### Suggested files
- `src/bigbrain/providers/lmstudio_provider.py`

### Acceptance criteria
- LM Studio works through the shared interface
- capability/availability checks are exposed to the router

---

## Workstream F - Routing, Fallback, and Observability

### Tasks
- [ ] Implement optional configured default/override behavior
- [ ] Implement automatic fallback based on capability and availability
- [ ] Define deterministic routing order
- [ ] Add provider selection telemetry/logging
- [ ] Add status helpers for provider readiness
- [ ] Confirm MVP has no forced local-only routing rules

### Suggested files
- `src/bigbrain/providers/router.py`
- `src/bigbrain/providers/health.py`

### Acceptance criteria
- provider preference is honored when possible
- fallback occurs automatically when needed
- routed provider is visible in logs and metadata
- routing remains provider-agnostic for later phases

---

## Workstream G - CLI, Docs, and Validation

### Tasks
- [ ] Add provider-related CLI/status commands or flags as needed
- [ ] Update config examples for providers
- [ ] Add provider mocks/fakes for tests
- [ ] Update `README.md` and `AGENTS.md`

### Suggested files
- `src/bigbrain/cli.py`
- `config/example.yaml`
- `README.md`
- `AGENTS.md`
- `tests/providers/`

### Acceptance criteria
- provider configuration and readiness can be inspected
- docs describe auth, local providers, and fallback behavior
- tests cover router behavior and adapter contract conformance

---

## Definition of Done for Phase 3

- [ ] provider contracts are stable
- [ ] first-run GitHub auth exists
- [ ] GitHub Copilot Enterprise adapter works
- [ ] Ollama adapter works
- [ ] LM Studio adapter works
- [ ] configured default/override plus automatic fallback works
- [ ] provider provenance is recorded
- [ ] docs and tests cover the provider layer

---

## Recommended First Commit Slice

### Slice 0
- close config/auth/logging blockers

### Slice 1
- provider contracts
- shared models

### Slice 2
- GitHub auth/bootstrap
- GitHub adapter

### Slice 3
- Ollama adapter
- LM Studio adapter

### Slice 4
- router/fallback/health
- CLI/docs/tests

