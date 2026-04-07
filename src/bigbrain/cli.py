"""BigBrain CLI – command-line interface built on argparse.

Provides the ``bigbrain`` entry-point with subcommands for every pipeline
stage.  Each subcommand is wired to a stub handler that will be replaced by
real implementations in later phases.
"""

from __future__ import annotations

import argparse
import sys
from typing import Sequence


# ---------------------------------------------------------------------------
# Stub handlers – one per subcommand
# ---------------------------------------------------------------------------

def _handle_ingest(args: argparse.Namespace) -> int:
    """Run the ingestion pipeline on the specified path."""
    from bigbrain.ingest.service import ingest_path
    from bigbrain.errors import UserError

    source = args.source
    if not source:
        raise UserError("--source is required. Specify a file or directory to ingest.")

    print(f"Ingesting from: {source}")
    print(f"  recursive: {args.recursive}")
    print(f"  type filter: {args.type}")
    print()

    try:
        result = ingest_path(
            source,
            recursive=args.recursive,
            file_type=args.type,
            skip_hidden=not args.include_hidden,
        )
    except UserError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    # Print summary
    print(f"Ingestion complete:")
    print(f"  ✓ Processed: {result.processed} file(s)")
    if result.skipped > 0:
        print(f"  ⊘ Skipped:   {result.skipped} file(s)")
    if result.failed > 0:
        print(f"  ✗ Failed:    {result.failed} file(s)")

    # Show processed documents
    if result.documents:
        print()
        print("Documents:")
        for doc in result.documents:
            size_info = ""
            if doc.source:
                size_info = f" ({doc.source.size_bytes:,} bytes)"
            print(f"  • {doc.title}{size_info}")
            if doc.sections:
                print(f"    sections: {len(doc.sections)}")

    # Show warnings
    if result.warnings:
        print()
        print(f"Warnings ({len(result.warnings)}):")
        for w in result.warnings[:10]:  # Cap at 10
            print(f"  ⚠ {w}")
        if len(result.warnings) > 10:
            print(f"  ... and {len(result.warnings) - 10} more")

    # Show errors
    if result.errors:
        print()
        print(f"Errors ({len(result.errors)}):")
        for e in result.errors[:10]:
            print(f"  ✗ {e}")
        if len(result.errors) > 10:
            print(f"  ... and {len(result.errors) - 10} more")

    return 1 if result.failed > 0 else 0


def _handle_distill(args: argparse.Namespace) -> int:
    print("⚠ 'distill' is not implemented yet. This command will be available in Phase 2.")
    return 0


def _handle_compile(args: argparse.Namespace) -> int:
    print("⚠ 'compile' is not implemented yet. This command will be available in Phase 3.")
    return 0


def _handle_update(args: argparse.Namespace) -> int:
    print("⚠ 'update' is not implemented yet. This command will be available in a future phase.")
    return 0


def _handle_status(args: argparse.Namespace) -> int:
    print("⚠ 'status' is not implemented yet. This command will be available in a future phase.")
    return 0


def _handle_kb_search(args: argparse.Namespace) -> int:
    print("⚠ 'kb-search' is not implemented yet. This command will be available in a future phase.")
    return 0


# ---------------------------------------------------------------------------
# Parser construction – kept modular so future phases can extend subparsers
# ---------------------------------------------------------------------------

def _add_ingest_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``ingest`` subcommand."""
    p = subparsers.add_parser(
        "ingest",
        help="Ingest content from local files or external sources",
        description="Ingest content from local files or external sources.",
    )
    p.add_argument(
        "--source",
        type=str,
        help="Path to the file or directory to ingest from",
    )
    p.add_argument(
        "--type",
        choices=["txt", "md", "pdf", "py", "auto"],
        default="auto",
        help="Source file type (default: auto)",
    )
    p.add_argument(
        "--recursive",
        action="store_true",
        default=True,
        help="Recursively traverse directories (default: true)",
    )
    p.add_argument(
        "--no-recursive",
        action="store_false",
        dest="recursive",
        help="Do not recurse into subdirectories",
    )
    p.add_argument(
        "--include-hidden",
        action="store_true",
        default=False,
        help="Include hidden files and directories (default: false)",
    )
    p.set_defaults(func=_handle_ingest)
    return p


def _add_distill_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``distill`` subcommand."""
    p = subparsers.add_parser(
        "distill",
        help="Distill ingested content into summaries, entities, and relationships",
        description="Distill ingested content into summaries, entities, and relationships.",
    )
    p.add_argument(
        "--target",
        type=str,
        help="Identifier of the content to distill",
    )
    p.set_defaults(func=_handle_distill)
    return p


def _add_compile_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``compile`` subcommand."""
    p = subparsers.add_parser(
        "compile",
        help="Compile knowledge base into output formats",
        description="Compile knowledge base into output formats.",
    )
    p.add_argument(
        "--format",
        choices=["markdown", "cheatsheet", "flashcard", "qa"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    p.set_defaults(func=_handle_compile)
    return p


def _add_update_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``update`` subcommand."""
    p = subparsers.add_parser(
        "update",
        help="Run incremental update pipeline on changed sources",
        description="Run incremental update pipeline on changed sources.",
    )
    p.add_argument(
        "--source",
        type=str,
        default=None,
        help="Optional path filter to limit the update scope",
    )
    p.set_defaults(func=_handle_update)
    return p


def _add_status_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``status`` subcommand."""
    p = subparsers.add_parser(
        "status",
        help="Show current knowledge base status and statistics",
        description="Show current knowledge base status and statistics.",
    )
    p.set_defaults(func=_handle_status)
    return p


def _add_kb_search_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``kb-search`` subcommand."""
    p = subparsers.add_parser(
        "kb-search",
        help="Search the knowledge base",
        description="Search the knowledge base.",
    )
    p.add_argument(
        "query",
        type=str,
        help="Search query string",
    )
    p.set_defaults(func=_handle_kb_search)
    return p


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser.

    Exposed as a standalone function so tests and documentation tools can
    introspect the CLI surface without invoking ``main()``.
    """
    parser = argparse.ArgumentParser(
        prog="bigbrain",
        description=(
            "BigBrain \u2013 a knowledge compiler that ingests, distills, "
            "and compiles knowledge."
        ),
    )

    subparsers = parser.add_subparsers(dest="command", title="commands")

    _add_ingest_parser(subparsers)
    _add_distill_parser(subparsers)
    _add_compile_parser(subparsers)
    _add_update_parser(subparsers)
    _add_status_parser(subparsers)
    _add_kb_search_parser(subparsers)

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point.

    Parameters
    ----------
    argv:
        Command-line arguments (defaults to ``sys.argv[1:]``).

    Returns
    -------
    int
        Exit code – 0 on success, 1 on error.
    """
    # Best-effort logging bootstrap; the module may not exist yet.
    try:
        from bigbrain.logging_config import setup_logging
        setup_logging()
    except ImportError:
        pass

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 1

    try:
        return args.func(args)
    except Exception as exc:  # noqa: BLE001
        from bigbrain.errors import UserError
        if isinstance(exc, UserError):
            print(f"Error: {exc}", file=sys.stderr)
        else:
            print(f"Internal error: {exc}", file=sys.stderr)
            import logging
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                import traceback
                traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
