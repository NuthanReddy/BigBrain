# BigBrain Phase 10 Implementation Task List
<!-- PLAN:TEMPLATE v1 -->
<!-- PLAN:SOURCE .github/plan/_phase-task-template.md -->


## Goal

Implement **hardening, testing, and release readiness** so the project is reliable to evolve and publish.

---

## Parallelization Strategy

This phase is highly parallelizable by discipline:
- test coverage expansion
- lint/format/tooling
- CI automation
- packaging/release automation
- documentation cleanup
- performance/security/reliability checks

---

## Scope Boundaries

### In scope
- broader test coverage
- fixture and snapshot maintenance
- linting/formatting/type-checking if chosen
- CI workflows
- release/versioning conventions
- contributor docs and runbooks
- performance and reliability checks

### Out of scope
- net-new product features
- major architectural redesigns unrelated to release readiness

---

## Phase 0–9 Carry-Over Issues / Preconditions

- [ ] core feature phases are stable enough to test and package
- [ ] project structure and CLI surface are no longer changing daily
- [ ] docs can be updated against a mostly stable implementation surface

### Minimum preflight acceptance criteria
- the application can be run end-to-end for the implemented feature set
- there is a stable enough command surface to automate in CI

---

## Recommended Implementation Order

0. Close major instability blockers from earlier phases
1. Expand tests and fixtures
2. Add lint/format/tooling
3. Add CI workflows
4. Add packaging/versioning/release steps
5. Add docs/runbooks/contributor guidance
6. Add performance/reliability checks

---

## Workstream A - Test Coverage and Fixtures

### Tasks
- [ ] add/expand unit tests across modules
- [ ] add fixture corpora for inputs and outputs
- [ ] add snapshot tests for compiled outputs
- [ ] add integration/smoke tests for key CLI flows

### Acceptance criteria
- major happy paths and failure paths are covered
- regressions are easier to catch before release

---

## Workstream B - Tooling Quality Gates

### Tasks
- [ ] choose and configure formatter/linter/test runner conventions
- [ ] add static checks if desired
- [ ] document local developer commands

### Acceptance criteria
- contributors have one consistent quality toolchain
- code quality checks are automatable

---

## Workstream C - CI Automation

### Tasks
- [ ] add CI workflow for tests
- [ ] add CI workflow for lint/format checks
- [ ] add smoke checks for packaging/CLI invocation
- [ ] fail fast on broken docs/examples if desired

### Acceptance criteria
- the project has automated quality gates on change
- the CLI/package can be validated in automation

---

## Workstream D - Packaging and Release Readiness

### Tasks
- [ ] review `pyproject.toml` metadata completeness
- [ ] define versioning policy
- [ ] define release checklist
- [ ] add packaging validation steps
- [ ] prepare distribution artifacts/process

### Acceptance criteria
- package metadata is complete and accurate
- release steps are documented and repeatable

---

## Workstream E - Documentation and Contributor Guidance

### Tasks
- [ ] update README to match implemented capabilities
- [ ] update AGENTS guidance to current architecture reality
- [ ] add contributor onboarding steps
- [ ] add troubleshooting/runbooks for common failures

### Acceptance criteria
- docs match the real product surface
- new contributors can run and test the project without guesswork

---

## Workstream F - Reliability, Performance, and Security Checks

### Tasks
- [ ] identify slow-path benchmarks or smoke benchmarks
- [ ] review dependency health/security where applicable
- [ ] add basic resilience checks for config, storage, provider fallback, sync, and CLI misuse

### Acceptance criteria
- common operational risks are documented and tested
- performance and reliability regressions are more visible

---

## Definition of Done for Phase 10

- [ ] tests cover the implemented feature surface adequately
- [ ] quality tooling is standardized
- [ ] CI runs automated checks
- [ ] packaging and release steps are documented and validated
- [ ] docs and contributor guidance are current
- [ ] basic performance/reliability/security checks exist

---

## Recommended First Commit Slice

### Slice 0
- close instability blockers from prior phases

### Slice 1
- test/fixture expansion

### Slice 2
- tooling configuration
- CI automation

### Slice 3
- packaging/release workflow
- docs/runbooks

### Slice 4
- perf/reliability/security pass

