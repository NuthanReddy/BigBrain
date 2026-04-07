#!/usr/bin/env python3
"""BigBrain – development entry point.

Run from the repo root with:

    python main.py [OPTIONS]

This script exists for local development so you can run BigBrain directly
from a checkout without installing the package.  The installed distribution
uses the console_scripts entry point defined in pyproject.toml instead.
"""

import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Make `import bigbrain` work from the repo root by placing src/ on sys.path.
# This is only needed when running via `python main.py`; an installed package
# already has its modules on the path.
# ---------------------------------------------------------------------------
_src_dir = str(Path(__file__).resolve().parent / "src")
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)


def _run() -> int:
    """Import and run the CLI, returning the process exit code."""
    from bigbrain.cli import main as cli_main  # noqa: E402 – deferred import

    return cli_main() or 0


if __name__ == "__main__":
    try:
        sys.exit(_run())

    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(130)

    except Exception as exc:
        # Import UserError late so a broken logging_config doesn't mask the
        # real error with an ImportError.
        from bigbrain.errors import UserError

        if isinstance(exc, UserError):
            # Expected, user-facing errors – no traceback needed.
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

        # Unexpected errors – show traceback only when debugging.
        print(f"Internal error: {exc}", file=sys.stderr)
        print("Run with --help for usage information.", file=sys.stderr)
        if os.environ.get("BIGBRAIN_DEBUG"):
            import traceback
            traceback.print_exc()
        sys.exit(1)
