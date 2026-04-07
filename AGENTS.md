# AGENTS Guide

## Project Snapshot
- This repo is currently a minimal single-file Python app.
- Runtime entry point is `main.py`.
- Packaging metadata lives in `pyproject.toml` (`[project]` with Python `>=3.10`).
- No framework, test suite, or external runtime dependencies are defined yet.

## Architecture and Flow
- Execution starts at the `if __name__ == '__main__':` block in `main.py`.
- Current call flow is linear: `__main__` -> `print_hi('PyCharm')` -> `print(...)`.
- `print_hi(name)` is the only business function today; it prints a greeting.
- There are no service boundaries, persistence layers, or inter-module APIs yet.

## Developer Workflows (Current)
- Run locally from repo root:
```powershell
python .\main.py
```
- Expected output pattern from current code: `Hi, PyCharm`.
- There is no discovered test command in the repo (no `tests/`, no test config).
- There is no discovered lint/format config in `pyproject.toml`.

## Project-Specific Coding Conventions
- Keep changes simple and script-friendly unless you also introduce structure files.
- Preserve a clear runnable entry point in `main.py` (or document a new one explicitly).
- If you add dependencies, record them under `dependencies` in `pyproject.toml`.
- Prefer adding small pure functions (like `print_hi`) and calling them from `__main__`.

## Integration Points and Dependencies
- External integrations: none discovered.
- Third-party Python dependencies: none declared (`dependencies = []`).
- Tooling assumptions from code comments indicate PyCharm-centric execution/debug flow.

## When Expanding the Codebase
- If introducing modules, keep `main.py` as a thin orchestrator and move logic out.
- Add a `README.md` and test commands once multiple behaviors exist.
- Update this file when architecture grows beyond single-file flow.

