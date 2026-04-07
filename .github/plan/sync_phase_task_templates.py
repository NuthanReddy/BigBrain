from __future__ import annotations

import argparse
import re
from pathlib import Path

TEMPLATE_MARKERS = [
    "<!-- PLAN:TEMPLATE v1 -->",
    "<!-- PLAN:SOURCE .github/plan/_phase-task-template.md -->",
]

# Canonical heading names and common aliases to normalize.
HEADING_ALIASES = {
    "Recommended Execution Order": "Recommended Implementation Order",
}

REQUIRED_HEADINGS = [
    "Goal",
    "Scope Boundaries",
    "Recommended Implementation Order",
    "Definition of Done for Phase",
    "Recommended First Commit Slice",
]


def _phase_files(plan_dir: Path) -> list[Path]:
    phase_files = sorted(plan_dir.glob("phase-*-implementation-task-list.md"))
    polyglot = sorted(plan_dir.glob("phase-11-*.md"))
    files = {f.resolve(): f for f in [*phase_files, *polyglot]}
    return [files[k] for k in sorted(files)]


def _extract_h2_headings(text: str) -> list[str]:
    return re.findall(r"^##\s+(.+)$", text, flags=re.MULTILINE)


def _has_required_heading(headings: list[str], required: str) -> bool:
    if required == "Definition of Done for Phase":
        return any(h.startswith("Definition of Done for Phase") for h in headings)
    return required in headings


def _normalize_aliases(text: str) -> str:
    for alias, canonical in HEADING_ALIASES.items():
        text = re.sub(
            rf"^##\s+{re.escape(alias)}$",
            f"## {canonical}",
            text,
            flags=re.MULTILINE,
        )
    return text


def _ensure_markers(text: str) -> str:
    lines = text.splitlines()
    if not lines:
        return text

    # Insert template markers after H1 if missing.
    if lines[0].startswith("# "):
        marker_block = TEMPLATE_MARKERS.copy()
        existing = set(lines[1:6])
        marker_block = [m for m in marker_block if m not in existing]
        if marker_block:
            insert_at = 1
            # Keep one blank line after markers for readability.
            lines[insert_at:insert_at] = marker_block + [""]
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def _append_missing_stubs(text: str) -> str:
    headings = _extract_h2_headings(text)
    additions: list[str] = []

    for required in REQUIRED_HEADINGS:
        if not _has_required_heading(headings, required):
            if required == "Definition of Done for Phase":
                additions.extend([
                    "",
                    "---",
                    "",
                    "## Definition of Done for Phase",
                    "",
                    "- [ ] TODO",
                ])
            elif required == "Recommended First Commit Slice":
                additions.extend([
                    "",
                    "---",
                    "",
                    "## Recommended First Commit Slice",
                    "",
                    "### Slice 0",
                    "- TODO",
                ])
            else:
                additions.extend([
                    "",
                    "---",
                    "",
                    f"## {required}",
                    "",
                    "TODO",
                ])

    if additions:
        if not text.endswith("\n"):
            text += "\n"
        text += "\n".join(additions) + "\n"
    return text


def sync_file(path: Path, write: bool) -> tuple[bool, str]:
    original = path.read_text(encoding="utf-8")
    updated = _normalize_aliases(original)
    updated = _ensure_markers(updated)
    updated = _append_missing_stubs(updated)

    changed = updated != original
    if changed and write:
        path.write_text(updated, encoding="utf-8")
    return changed, path.name


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync phase task docs to the shared template structure.")
    parser.add_argument("--plan-dir", default=".github/plan", help="Directory containing phase task docs")
    parser.add_argument("--write", action="store_true", help="Write updates in place")
    args = parser.parse_args()

    plan_dir = Path(args.plan_dir).resolve()
    files = _phase_files(plan_dir)

    changed_files: list[str] = []
    for path in files:
        changed, name = sync_file(path, write=args.write)
        if changed:
            changed_files.append(name)

    if changed_files:
        mode = "updated" if args.write else "would update"
        print(f"{mode}: {', '.join(changed_files)}")
        return 0 if args.write else 1

    print("all phase task docs already synced")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

