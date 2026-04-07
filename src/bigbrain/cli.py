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
    from bigbrain.logging_config import get_logger

    logger = get_logger(__name__)

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

    # Persist to KB unless --no-store
    if not args.no_store:
        from bigbrain.kb.store import KBStore
        from bigbrain.config import load_config

        cfg = load_config()
        stored_count = 0
        with KBStore(cfg.kb_db_path) as store:
            for doc in result.documents:
                try:
                    store.save_document(doc)
                    stored_count += 1
                except Exception as exc:
                    logger.warning("Failed to store document %s: %s", doc.title, exc)

            store.save_ingestion_run(result, source_path=source)

        print(f"  💾 Stored:    {stored_count} document(s) in knowledge base")

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
    """Show knowledge base status and statistics."""
    from bigbrain.config import load_config
    from pathlib import Path

    cfg = load_config()
    db_path = cfg.kb_db_path

    # Check if DB exists
    if not Path(db_path).exists():
        print("Knowledge base is empty (no database found).")
        print(f"  Expected location: {db_path}")
        print("  Run 'bigbrain ingest --source <path>' to populate it.")
        return 0

    from bigbrain.kb.store import KBStore

    with KBStore(db_path) as store:
        stats = store.get_stats()

    print("BigBrain Knowledge Base Status")
    print("=" * 40)
    print(f"  Documents:  {stats['total_documents']}")
    print(f"  Sections:   {stats['total_sections']}")

    # Format size
    size = stats['total_size_bytes']
    if size >= 1_048_576:
        print(f"  Total size: {size / 1_048_576:.1f} MB")
    elif size >= 1024:
        print(f"  Total size: {size / 1024:.1f} KB")
    else:
        print(f"  Total size: {size} bytes")

    # By type breakdown
    if stats['by_type']:
        print()
        print("By Type:")
        for stype, count in sorted(stats['by_type'].items()):
            print(f"  .{stype}: {count} document(s)")

    # Last runs
    if stats.get('last_successful_run'):
        run = stats['last_successful_run']
        print()
        print(f"Last successful ingestion: {run.get('finished_at', 'unknown')}")
        print(f"  Processed: {run.get('processed', 0)}, Skipped: {run.get('skipped', 0)}, Failed: {run.get('failed', 0)}")

    if stats.get('last_failed_run'):
        run = stats['last_failed_run']
        print()
        print(f"Last failed ingestion: {run.get('finished_at', 'unknown')}")
        print(f"  Processed: {run.get('processed', 0)}, Failed: {run.get('failed', 0)}")

    if not stats.get('last_successful_run') and not stats.get('last_failed_run'):
        print()
        print("No ingestion runs recorded yet.")

    print()
    print(f"Database: {db_path}")

    return 0


def _handle_kb_search(args: argparse.Namespace) -> int:
    """Search the knowledge base using full-text search."""
    from bigbrain.config import load_config
    from pathlib import Path

    cfg = load_config()
    db_path = cfg.kb_db_path

    if not Path(db_path).exists():
        print("Knowledge base is empty (no database found).")
        print("  Run 'bigbrain ingest --source <path>' to populate it.")
        return 1

    from bigbrain.kb.store import KBStore

    query = args.query
    limit = args.limit if hasattr(args, 'limit') else 20

    with KBStore(db_path) as store:
        results = store.search_documents(query, limit=limit)

    if not results:
        print(f"No results found for: {query}")
        return 0

    print(f"Found {len(results)} result(s) for: {query}")
    print()

    for i, doc in enumerate(results, 1):
        source_info = ""
        if doc.source:
            source_info = f" [{doc.source.source_type}]"
        print(f"  {i}. {doc.title}{source_info}")
        if doc.source:
            print(f"     {doc.source.file_path}")

        # Show a content snippet (first 150 chars, single line)
        snippet = doc.content[:150].replace("\n", " ").strip()
        if len(doc.content) > 150:
            snippet += "..."
        if snippet:
            print(f"     {snippet}")
        print()

    return 0


def _handle_providers(args: argparse.Namespace) -> int:
    """Show AI provider status and availability."""
    from bigbrain.providers.registry import ProviderRegistry

    registry = ProviderRegistry.from_app_config()

    if not registry.has_providers():
        print("No AI providers are enabled.")
        print("  Enable providers in config/example.yaml under 'providers:'")
        return 0

    print("AI Provider Status")
    print("=" * 40)

    if registry.preferred:
        print(f"  Preferred: {registry.preferred}")
    print()

    health = registry.health_check()
    for name, available in health.items():
        status = "✓ available" if available else "✗ unavailable"
        preferred_tag = " (preferred)" if name == registry.preferred else ""
        print(f"  {name}{preferred_tag}: {status}")

    # List models for available providers
    available = registry.get_available_providers()
    if available and args.models:
        print()
        for provider in available:
            if hasattr(provider, 'list_models'):
                models = provider.list_models()
                if models:
                    print(f"  {provider.name} models:")
                    for m in models[:10]:
                        print(f"    • {m}")

    return 0


def _handle_ask(args: argparse.Namespace) -> int:
    """Answer a question using KB context + AI provider (RAG)."""
    from bigbrain.config import load_config
    from pathlib import Path

    cfg = load_config()
    db_path = cfg.kb_db_path

    if not Path(db_path).exists():
        print("Knowledge base is empty (no database found).")
        print("  Run 'bigbrain ingest --source <path>' to populate it.")
        return 1

    from bigbrain.rag.pipeline import RAGPipeline
    from bigbrain.errors import NoProviderAvailableError

    try:
        with RAGPipeline.from_config() as pipeline:
            if not pipeline._registry.has_providers():
                print("No AI providers are enabled.")
                print("  Enable a provider in config/example.yaml (e.g., ollama, lm_studio, github_copilot)")
                print("  Check status with: bigbrain providers")
                return 1

            mode = getattr(args, 'mode', 'ask')

            print(f"Searching knowledge base...")

            if mode == 'explain':
                response = pipeline.explain(
                    args.question,
                    max_docs=args.context_docs,
                    model=args.model,
                )
            else:
                response = pipeline.ask(
                    args.question,
                    max_docs=args.context_docs,
                    model=args.model,
                )

            if response.chunks_used == 0:
                print("No relevant documents found in the knowledge base.")
                print("  Try ingesting more content first.")
                return 1

            print(f"Found {response.chunks_used} relevant chunk(s) from {len(response.sources)} source(s)")
            print()
            print(response.answer)

            # Attribution footer
            print()
            if response.provider and response.model:
                print(f"— {response.provider}/{response.model}")
            if response.sources:
                print(f"— Sources: {len(response.sources)} document(s)")

    except NoProviderAvailableError:
        print("No AI provider is available. Check with: bigbrain providers")
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


def _handle_kb_export(args: argparse.Namespace) -> int:
    """Export knowledge base to JSONL file."""
    from bigbrain.kb.store import KBStore
    from bigbrain.config import load_config
    from pathlib import Path

    cfg = load_config()
    if not Path(cfg.kb_db_path).exists():
        print("Knowledge base is empty (no database found).")
        return 1

    output = args.output
    with KBStore(cfg.kb_db_path) as store:
        count = store.export_jsonl(output)

    print(f"Exported {count} document(s) to {output}")
    return 0


def _handle_kb_import(args: argparse.Namespace) -> int:
    """Import documents from JSONL file."""
    from bigbrain.kb.store import KBStore
    from bigbrain.config import load_config
    from pathlib import Path

    cfg = load_config()
    input_path = args.input

    if not Path(input_path).exists():
        from bigbrain.errors import UserError
        raise UserError(f"File not found: {input_path}")

    with KBStore(cfg.kb_db_path) as store:
        imported, skipped = store.import_jsonl(input_path)

    print(f"Imported {imported} document(s), skipped {skipped}")
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
    p.add_argument(
        "--no-store",
        action="store_true",
        default=False,
        help="Skip saving documents to the knowledge base",
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
        description="Search the knowledge base using full-text search.",
    )
    p.add_argument("query", type=str, help="Search query string")
    p.add_argument("--limit", type=int, default=20,
                   help="Maximum number of results (default: 20)")
    p.set_defaults(func=_handle_kb_search)
    return p


def _add_kb_export_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``kb-export`` subcommand."""
    p = subparsers.add_parser(
        "kb-export",
        help="Export knowledge base to JSONL",
        description="Export all documents in the knowledge base to a JSONL file.",
    )
    p.add_argument(
        "--output", "-o",
        type=str,
        default="kb-export.jsonl",
        help="Output file path (default: kb-export.jsonl)",
    )
    p.set_defaults(func=_handle_kb_export)
    return p


def _add_kb_import_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``kb-import`` subcommand."""
    p = subparsers.add_parser(
        "kb-import",
        help="Import documents from JSONL",
        description="Import documents from a JSONL file into the knowledge base.",
    )
    p.add_argument(
        "input",
        type=str,
        help="Path to JSONL file to import",
    )
    p.set_defaults(func=_handle_kb_import)
    return p


def _add_providers_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``providers`` subcommand."""
    p = subparsers.add_parser(
        "providers",
        help="Show AI provider status and availability",
        description="Show registered AI providers, health status, and available models.",
    )
    p.add_argument(
        "--models",
        action="store_true",
        default=False,
        help="Also list available models for each provider",
    )
    p.set_defaults(func=_handle_providers)
    return p


def _add_ask_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``ask`` subcommand."""
    p = subparsers.add_parser(
        "ask",
        help="Ask a question using KB context + AI (RAG)",
        description=(
            "Search the knowledge base for relevant context, then use an AI "
            "provider to generate a well-formed answer."
        ),
    )
    p.add_argument("question", type=str, help="The question to answer")
    p.add_argument(
        "--context-docs", type=int, default=5,
        help="Number of KB documents to use as context (default: 5)",
    )
    p.add_argument(
        "--model", type=str, default="",
        help="Override the AI model to use",
    )
    p.add_argument(
        "--mode", choices=["ask", "explain"], default="ask",
        help="Answer mode: 'ask' for Q&A, 'explain' for concept explanation (default: ask)",
    )
    p.set_defaults(func=_handle_ask)
    return p


def _handle_auth(args: argparse.Namespace) -> int:
    """Manage GitHub authentication."""
    from bigbrain.providers.github_auth import (
        device_flow_login,
        clear_cached_token,
        resolve_github_token,
        validate_token,
        AuthError,
        _TOKEN_CACHE_PATH,
    )

    action = args.action

    if action == "login":
        try:
            token = device_flow_login()
            print(f"Authenticated successfully. Token cached at {_TOKEN_CACHE_PATH}")
            return 0
        except AuthError as exc:
            print(f"Authentication failed: {exc}", file=sys.stderr)
            return 1

    elif action == "logout":
        if clear_cached_token():
            print("GitHub token removed.")
        else:
            print("No cached token found.")
        return 0

    elif action == "status":
        token = resolve_github_token()
        if validate_token(token):
            # Mask the token for display
            masked = token[:8] + "..." + token[-4:] if len(token) > 16 else "***"
            print(f"GitHub token: {masked}")
            if _TOKEN_CACHE_PATH.exists():
                print(f"  Cached at: {_TOKEN_CACHE_PATH}")
        else:
            print("No valid GitHub token found.")
            print("  Run 'bigbrain auth login' to authenticate.")
        return 0

    return 0


def _add_auth_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``auth`` subcommand."""
    p = subparsers.add_parser(
        "auth",
        help="Manage GitHub authentication for Copilot",
        description="Login, logout, or check GitHub Copilot authentication status.",
    )
    p.add_argument(
        "action",
        choices=["login", "logout", "status"],
        help="Authentication action: login (device flow), logout (clear token), status (check token)",
    )
    p.set_defaults(func=_handle_auth)
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
    _add_kb_export_parser(subparsers)
    _add_kb_import_parser(subparsers)
    _add_providers_parser(subparsers)
    _add_ask_parser(subparsers)
    _add_auth_parser(subparsers)

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
