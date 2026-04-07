"""Progress display helpers using rich (with graceful fallback)."""

from __future__ import annotations

import sys
from contextlib import contextmanager
from typing import Any, Iterator

from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


def _is_interactive() -> bool:
    return hasattr(sys.stderr, "isatty") and sys.stderr.isatty()


@contextmanager
def progress_bar(total: int, description: str = "Processing") -> Iterator[Any]:
    """Context manager for a progress bar.

    Uses rich if available and interactive, otherwise a simple counter.

    Usage::
        with progress_bar(len(items), "Ingesting") as update:
            for item in items:
                process(item)
                update(1)
    """
    if _is_interactive():
        try:
            from rich.progress import (
                BarColumn,
                Progress,
                SpinnerColumn,
                TextColumn,
                TimeRemainingColumn,
            )

            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TextColumn("{task.completed}/{task.total}"),
                TimeRemainingColumn(),
            ) as prog:
                task_id = prog.add_task(description, total=total)

                def update(advance: int = 1) -> None:
                    prog.update(task_id, advance=advance)

                yield update
                return
        except ImportError:
            pass

    # Fallback: simple counter
    completed = [0]

    def update(advance: int = 1) -> None:
        completed[0] += advance
        if completed[0] % max(1, total // 10) == 0 or completed[0] == total:
            print(f"  {description}: {completed[0]}/{total}", flush=True)

    yield update


def print_status(message: str, style: str = "") -> None:
    """Print a styled status message (uses rich if available)."""
    try:
        from rich import print as rprint

        if style:
            rprint(f"[{style}]{message}[/{style}]")
        else:
            rprint(message)
    except ImportError:
        print(message)


def print_table(headers: list[str], rows: list[list[str]], title: str = "") -> None:
    """Print a formatted table (uses rich if available)."""
    try:
        from rich.console import Console
        from rich.table import Table

        table = Table(title=title)
        for h in headers:
            table.add_column(h)
        for row in rows:
            table.add_row(*[str(c) for c in row])
        Console().print(table)
    except ImportError:
        if title:
            print(f"\n{title}")
        widths = [
            max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
            for i, h in enumerate(headers)
        ]
        header_line = "  ".join(h.ljust(w) for h, w in zip(headers, widths))
        print(header_line)
        print("-" * len(header_line))
        for row in rows:
            print("  ".join(str(c).ljust(w) for c, w in zip(row, widths)))
