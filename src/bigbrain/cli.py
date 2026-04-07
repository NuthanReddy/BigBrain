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

    # URL ingestion mode
    if args.url:
        from bigbrain.ingest.url_ingester import UrlIngester
        print(f"Ingesting URL: {args.url}")
        try:
            ingester = UrlIngester()
            doc = ingester.ingest(args.url)
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        print(f"  Title: {doc.title}")
        print(f"  Size: {doc.source.size_bytes:,} bytes")
        if doc.sections:
            print(f"  Sections: {len(doc.sections)}")

        if not args.no_store:
            from bigbrain.kb.store import KBStore
            from bigbrain.config import load_config
            cfg = load_config()
            with KBStore(cfg.kb_db_path) as store:
                store.save_document(doc)
            print(f"  💾 Stored in knowledge base")

        return 0

    # API ingestion mode
    if args.api:
        from bigbrain.ingest.api_ingester import ApiIngester
        print(f"Ingesting API: {args.api}")
        try:
            ingester = ApiIngester(auth_token=args.auth_token)
            doc = ingester.ingest(args.api, json_path=args.json_path)
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1

        print(f"  Title: {doc.title}")
        print(f"  Size: {doc.source.size_bytes:,} bytes")
        if doc.sections:
            print(f"  Sections: {len(doc.sections)}")

        if not args.no_store:
            from bigbrain.kb.store import KBStore
            from bigbrain.config import load_config
            cfg = load_config()
            with KBStore(cfg.kb_db_path) as store:
                store.save_document(doc)
            print(f"  💾 Stored in knowledge base")

        return 0

    source = args.source
    if not source:
        raise UserError("--source, --url, or --api is required. Specify a file, directory, URL, or API endpoint.")

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
    """Run the distillation pipeline on stored documents."""
    from bigbrain.config import load_config
    from pathlib import Path

    cfg = load_config()
    db_path = cfg.kb_db_path

    if not Path(db_path).exists():
        print("Knowledge base is empty (no database found).")
        print("  Run 'bigbrain ingest --source <path>' first.")
        return 1

    from bigbrain.distill.pipeline import DistillPipeline
    from bigbrain.errors import NoProviderAvailableError

    workers = getattr(args, 'workers', 3)

    try:
        with DistillPipeline.from_config(cfg) as pipeline:
            pipeline._workers = workers
            if not pipeline._registry.has_providers():
                print("No AI providers are enabled.")
                print("  Enable a provider in config/example.yaml")
                return 1

            model = args.model if args.model else ""
            force = getattr(args, 'force', False)
            step_arg = getattr(args, 'step', '')
            steps = {step_arg} if step_arg else None

            if args.doc_id:
                print(f"Distilling document: {args.doc_id}{f' (step: {step_arg})' if step_arg else ''}")
                result = pipeline.distill_by_id(args.doc_id, model=model, force=force, steps=steps)
                if result is None:
                    print(f"Document not found: {args.doc_id}")
                    return 1
                _print_distill_result(result)
            else:
                source_type = args.type if args.type else None
                mode = "force" if force else "incremental"
                step_info = f", step: {step_arg}" if step_arg else ""
                print(f"Distilling all documents ({mode}{step_info}){f' (type: {source_type})' if source_type else ''}...")
                results = pipeline.distill_all(model=model, source_type=source_type, force=force, steps=steps)

                total_summaries = sum(len(r.summaries) for r in results)
                total_entities = sum(len(r.entities) for r in results)
                total_relationships = sum(len(r.relationships) for r in results)
                total_errors = sum(len(r.errors) for r in results)

                print()
                print(f"Distillation complete:")
                print(f"  Documents:     {len(results)}")
                print(f"  Summaries:     {total_summaries}")
                print(f"  Entities:      {total_entities}")
                print(f"  Relationships: {total_relationships}")
                if total_errors > 0:
                    print(f"  Errors:        {total_errors}")

    except NoProviderAvailableError:
        print("No AI provider is available. Check with: bigbrain providers")
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


def _print_distill_result(result):
    """Print a single distillation result."""
    print()
    print(f"Distillation complete:")
    print(f"  Chunks:        {len(result.chunks)}")
    print(f"  Summaries:     {len(result.summaries)}")
    print(f"  Entities:      {len(result.entities)}")
    print(f"  Relationships: {len(result.relationships)}")

    if result.summaries:
        print()
        print("Summary:")
        print(f"  {result.summaries[0].content[:500]}")

    if result.entities:
        print()
        print(f"Entities ({len(result.entities)}):")
        for e in result.entities[:15]:
            print(f"  • {e.name} ({e.entity_type}): {e.description[:80]}")
        if len(result.entities) > 15:
            print(f"  ... and {len(result.entities) - 15} more")

    if result.relationships:
        print()
        print(f"Relationships ({len(result.relationships)}):")
        for r in result.relationships[:10]:
            print(f"  • {r.relationship_type}: {r.description[:80]}")
        if len(result.relationships) > 10:
            print(f"  ... and {len(result.relationships) - 10} more")

    if result.errors:
        print()
        print(f"Errors ({len(result.errors)}):")
        for e in result.errors:
            print(f"  ✗ {e}")

    if result.provider:
        print()
        print(f"— {result.provider}/{result.model}")


def _handle_compile(args: argparse.Namespace) -> int:
    """Compile distilled content into output formats."""
    from bigbrain.config import load_config
    from pathlib import Path

    cfg = load_config()
    db_path = cfg.kb_db_path

    if not Path(db_path).exists():
        print("Knowledge base is empty.")
        print("  Run 'bigbrain ingest' then 'bigbrain distill' first.")
        return 1

    from bigbrain.compile.pipeline import CompilePipeline

    fmt = args.format
    model = args.model if hasattr(args, 'model') and args.model else ""
    output = getattr(args, 'output', '') or ''

    try:
        with CompilePipeline.from_config(cfg) as pipeline:
            if args.doc_id:
                print(f"Compiling {args.doc_id} as {fmt}...")
                result = pipeline.compile_document(
                    args.doc_id, format=fmt, model=model, output_path=output,
                )
                if result is None:
                    print(f"Document not found: {args.doc_id}")
                    return 1

                out_path = result.metadata.get("output_path", output or "stdout")
                print(f"✓ Compiled: {result.title}")
                print(f"  Format: {fmt}")
                print(f"  Output: {out_path}")
                if result.flashcards:
                    print(f"  Flashcards: {len(result.flashcards)}")
                if result.qa_pairs:
                    print(f"  Q&A pairs: {len(result.qa_pairs)}")
                if result.generated_by_provider:
                    print(f"  Provider: {result.generated_by_provider}/{result.generated_by_model}")
            else:
                source_type = args.type if hasattr(args, 'type') and args.type else None
                print(f"Compiling all documents as {fmt}...")
                compile_result = pipeline.compile_all(
                    format=fmt, model=model, source_type=source_type,
                )

                print()
                print(f"Compilation complete:")
                print(f"  Documents: {compile_result.total_documents}")
                print(f"  Outputs:   {len(compile_result.outputs)}")
                if compile_result.errors:
                    print(f"  Errors:    {len(compile_result.errors)}")

                if compile_result.outputs:
                    print()
                    for out in compile_result.outputs:
                        path = out.metadata.get("output_path", "")
                        print(f"  ✓ {out.title}")
                        if path:
                            print(f"    → {path}")

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


def _handle_update(args: argparse.Namespace) -> int:
    """Run incremental update pipeline on changed sources."""
    from bigbrain.config import load_config
    from bigbrain.orchestrator.pipeline import Orchestrator

    cfg = load_config()
    source = args.source
    if not source:
        from bigbrain.errors import UserError
        raise UserError("--source is required for update. Specify a file or directory.")

    force = getattr(args, 'force', False)
    model = getattr(args, 'model', '') or ''

    # Parse steps
    step_arg = getattr(args, 'steps', '')
    steps = set(step_arg.split(',')) if step_arg else None

    compile_format = getattr(args, 'format', '') or ''

    mode = "force" if force else "incremental"
    print(f"Running {mode} update from: {source}")

    with Orchestrator.from_config(cfg) as orch:
        result = orch.run(
            source, force=force, steps=steps,
            model=model, compile_format=compile_format,
        )

    print()
    print(f"Update complete ({', '.join(result.steps_run)}):")
    print(f"  Ingested:    {result.ingested}")
    if result.skipped_unchanged:
        print(f"  Unchanged:   {result.skipped_unchanged}")
    if result.deleted:
        print(f"  Deleted:     {result.deleted}")
    if result.distilled:
        print(f"  Distilled:   {result.distilled}")
    if result.compiled:
        print(f"  Compiled:    {result.compiled}")
    if result.errors:
        print(f"  Errors:      {len(result.errors)}")
        for e in result.errors[:5]:
            print(f"    ✗ {e}")

    return 1 if result.errors else 0


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
        docs = store.list_documents(limit=9999) if not args.brief else []

    print("BigBrain Knowledge Base Status")
    print("=" * 40)
    print(f"  Documents:  {stats['total_documents']}")
    print(f"  Sections:   {stats['total_sections']}")

    # Distillation stats
    if stats.get('total_chunks', 0) or stats.get('total_summaries', 0):
        print()
        print("Distilled:")
        print(f"  Chunks:        {stats.get('total_chunks', 0)}")
        print(f"  Summaries:     {stats.get('total_summaries', 0)}")
        print(f"  Entities:      {stats.get('total_entities', 0)}")
        print(f"  Relationships: {stats.get('total_relationships', 0)}")

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

    # Document listing with IDs
    if docs:
        print()
        print("Documents:")
        for doc in docs:
            stype = f" [{doc.source.source_type}]" if doc.source else ""
            print(f"  {doc.id}  {doc.title}{stype}")

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


def _handle_distill_show(args: argparse.Namespace) -> int:
    """Show distilled content for a document or all documents."""
    from bigbrain.config import load_config
    from pathlib import Path

    cfg = load_config()
    db_path = cfg.kb_db_path

    if not Path(db_path).exists():
        print("Knowledge base is empty.")
        return 1

    from bigbrain.kb.store import KBStore

    with KBStore(db_path) as store:
        if args.doc_id:
            docs = []
            doc = store.get_document(args.doc_id)
            if doc:
                docs = [doc]
            else:
                print(f"Document not found: {args.doc_id}")
                return 1
        else:
            docs = store.list_documents(limit=9999)

        if not docs:
            print("No documents in KB.")
            return 0

        for doc in docs:
            summaries = store.get_summaries(doc.id)
            entities = store.get_entities(doc.id)
            relationships = store.get_relationships(doc.id)

            if not summaries and not entities and not relationships:
                continue

            print(f"{'=' * 60}")
            source = f" [{doc.source.source_type}]" if doc.source else ""
            print(f"  {doc.title}{source}")
            print(f"{'=' * 60}")

            if summaries:
                print()
                print("📝 Summary:")
                for s in summaries:
                    print(f"  {s.content[:1000]}")
                    if s.generated_by_model:
                        print(f"  — {s.generated_by_provider}/{s.generated_by_model}")

            if entities:
                print()
                print(f"🏷️  Entities ({len(entities)}):")
                for e in entities[:30]:
                    desc = f": {e.description[:60]}" if e.description else ""
                    print(f"  • {e.name} ({e.entity_type}){desc}")
                if len(entities) > 30:
                    print(f"  ... and {len(entities) - 30} more")

            if relationships:
                # Build name lookup from entities
                ent_map = {e.id: e.name for e in entities}
                print()
                print(f"🔗 Relationships ({len(relationships)}):")
                for r in relationships[:20]:
                    src = ent_map.get(r.source_entity_id, r.source_entity_id[:8])
                    tgt = ent_map.get(r.target_entity_id, r.target_entity_id[:8])
                    print(f"  • {src} —[{r.relationship_type}]→ {tgt}")
                    if r.description:
                        print(f"    {r.description[:80]}")
                if len(relationships) > 20:
                    print(f"  ... and {len(relationships) - 20} more")

            print()

    return 0


def _handle_entities(args: argparse.Namespace) -> int:
    """List distilled entities with optional type filter."""
    from bigbrain.config import load_config
    from pathlib import Path

    cfg = load_config()
    db_path = cfg.kb_db_path

    if not Path(db_path).exists():
        print("Knowledge base is empty.")
        return 1

    from bigbrain.kb.store import KBStore

    with KBStore(db_path) as store:
        entity_type = getattr(args, 'type', '') or ''
        search = getattr(args, 'search', '') or ''

        # If --types flag, just show available types
        if getattr(args, 'types', False):
            type_counts = store.get_entity_types()
            if not type_counts:
                print("No entities found.")
                return 0
            print(f"Entity types ({sum(c for _, c in type_counts)} total):")
            for etype, count in type_counts:
                print(f"  {etype}: {count}")
            return 0

        entities = store.list_all_entities(
            entity_type=entity_type,
            search=search,
            limit=getattr(args, 'limit', 500),
        )

    if not entities:
        filter_info = f" (type={entity_type})" if entity_type else ""
        filter_info += f" (search={search})" if search else ""
        print(f"No entities found{filter_info}.")
        return 0

    # Group by type for display
    by_type: dict[str, list] = {}
    for e in entities:
        by_type.setdefault(e.entity_type, []).append(e)

    print(f"Entities: {len(entities)} found")
    print()
    for etype, ents in sorted(by_type.items()):
        print(f"  [{etype}] ({len(ents)})")
        for e in ents:
            desc = f" — {e.description[:70]}" if e.description else ""
            print(f"    • {e.name}{desc}")
        print()

    return 0


def _handle_compact(args: argparse.Namespace) -> int:
    """Compact the knowledge base: deduplicate entities, optimize storage."""
    from bigbrain.config import load_config
    from pathlib import Path

    cfg = load_config()
    db_path = cfg.kb_db_path

    if not Path(db_path).exists():
        print("Knowledge base is empty.")
        return 1

    from bigbrain.kb.store import KBStore

    with KBStore(db_path) as store:
        # Get before counts
        stats_before = store.get_stats()
        entities_before = stats_before.get("total_entities", 0)

        # Deduplicate entities
        removed = store.dedup_entities()

        # Get after counts
        stats_after = store.get_stats()
        entities_after = stats_after.get("total_entities", 0)

    print("Knowledge Base Compaction")
    print("=" * 40)
    print(f"  Entities: {entities_before} → {entities_after} ({removed} duplicates removed)")
    print()
    if removed == 0:
        print("  No duplicates found — KB is already clean.")
    else:
        print(f"  ✓ Removed {removed} duplicate entities")

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
    p.add_argument(
        "--url", type=str, default="",
        help="URL of a web page to ingest",
    )
    p.add_argument(
        "--api", type=str, default="",
        help="URL of a REST API endpoint to ingest (JSON)",
    )
    p.add_argument(
        "--json-path", type=str, default="",
        help="Dot-separated path to extract from API JSON response (e.g., 'data.content')",
    )
    p.add_argument(
        "--auth-token", type=str, default="",
        help="Bearer token for API authentication",
    )
    p.set_defaults(func=_handle_ingest)
    return p


def _add_distill_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``distill`` subcommand."""
    p = subparsers.add_parser(
        "distill",
        help="Distill ingested content into summaries, entities, and relationships",
        description="Run the distillation pipeline: chunk, summarize, extract entities, build relationships.",
    )
    p.add_argument(
        "--doc-id", type=str, default="",
        help="Distill a specific document by ID (default: distill all)",
    )
    p.add_argument(
        "--type", type=str, default="",
        help="Filter documents by source type (e.g., 'txt', 'md', 'pdf')",
    )
    p.add_argument(
        "--model", type=str, default="",
        help="Override the AI model to use",
    )
    p.add_argument(
        "--workers", type=int, default=2,
        help="Number of parallel workers for multi-document distillation (default: 2)",
    )
    p.add_argument(
        "--force", action="store_true", default=False,
        help="Re-distill all chunks even if unchanged (default: incremental)",
    )
    p.add_argument(
        "--step", type=str, default="", choices=["", "summarize", "entities", "relationships"],
        help="Run only a specific step (default: all steps)",
    )
    p.set_defaults(func=_handle_distill)
    return p


def _add_distill_show_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``distill-show`` subcommand."""
    p = subparsers.add_parser(
        "distill-show",
        help="Show distilled content (summaries, entities, relationships)",
        description="Display distillation results stored in the knowledge base.",
    )
    p.add_argument(
        "--doc-id", type=str, default="",
        help="Show distilled content for a specific document (default: all)",
    )
    p.set_defaults(func=_handle_distill_show)
    return p


def _add_entities_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``entities`` subcommand."""
    p = subparsers.add_parser(
        "entities",
        help="List distilled entities with optional filters",
        description="Display extracted entities from the knowledge base.",
    )
    p.add_argument(
        "--type", type=str, default="",
        help="Filter by entity type (e.g., algorithm, concept, data_structure, theorem, technique)",
    )
    p.add_argument(
        "--search", type=str, default="",
        help="Search entities by name or description",
    )
    p.add_argument(
        "--types", action="store_true", default=False,
        help="Show available entity types with counts",
    )
    p.add_argument(
        "--limit", type=int, default=500,
        help="Maximum entities to display (default: 500)",
    )
    p.set_defaults(func=_handle_entities)
    return p


def _add_compact_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``compact`` subcommand."""
    p = subparsers.add_parser(
        "compact",
        help="Compact the KB: deduplicate entities, optimize storage",
        description="Remove duplicate entities and optimize the knowledge base.",
    )
    p.set_defaults(func=_handle_compact)
    return p


def _add_compile_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``compile`` subcommand."""
    p = subparsers.add_parser(
        "compile",
        help="Compile knowledge base into output formats",
        description="Render distilled content as markdown, flashcards, cheatsheets, Q&A, or study guides.",
    )
    p.add_argument(
        "--format", "-f",
        choices=["markdown", "flashcard", "cheatsheet", "qa", "study_guide"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    p.add_argument(
        "--doc-id", type=str, default="",
        help="Compile a specific document by ID (default: compile all)",
    )
    p.add_argument(
        "--type", type=str, default="",
        help="Filter documents by source type",
    )
    p.add_argument(
        "--model", type=str, default="",
        help="Override the AI model (for flashcard, qa, study_guide)",
    )
    p.add_argument(
        "--output", "-o", type=str, default="",
        help="Output file path (default: auto-generate in build/ directory)",
    )
    p.set_defaults(func=_handle_compile)
    return p


def _add_update_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``update`` subcommand."""
    p = subparsers.add_parser(
        "update",
        help="Run incremental update pipeline on changed sources",
        description="Detect changes, re-ingest, distill, and compile incrementally.",
    )
    p.add_argument("--source", type=str, default=None, help="Path to file or directory")
    p.add_argument("--force", action="store_true", default=False, help="Skip change detection, reprocess everything")
    p.add_argument("--steps", type=str, default="", help="Comma-separated steps: ingest,distill,compile (default: all)")
    p.add_argument("--model", type=str, default="", help="Override AI model")
    p.add_argument("--format", type=str, default="", help="Compile format (markdown, flashcard, etc.)")
    p.set_defaults(func=_handle_update)
    return p


def _add_status_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``status`` subcommand."""
    p = subparsers.add_parser(
        "status",
        help="Show current knowledge base status and statistics",
        description="Show current knowledge base status and statistics.",
    )
    p.add_argument(
        "--brief", action="store_true", default=False,
        help="Show only counts, skip document listing",
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


# ---------------------------------------------------------------------------
# Notion integration
# ---------------------------------------------------------------------------

def _handle_notion(args: argparse.Namespace) -> int:
    """Manage Notion integration."""
    from bigbrain.config import load_config

    cfg = load_config()
    action = args.action

    if action == "status":
        from bigbrain.notion.client import NotionClient

        client = NotionClient.from_config(cfg.notion)

        available = client.is_available()
        print("Notion Integration Status")
        print("=" * 40)
        conn_status = "\u2713 yes" if available else "\u2717 no"
        print(f"  Connected: {conn_status}")
        print(f"  Direction: {cfg.notion.sync_direction}")

        if available:
            from pathlib import Path

            if Path(cfg.kb_db_path).exists():
                from bigbrain.notion.sync import SyncEngine
                from bigbrain.kb.store import KBStore

                with KBStore(cfg.kb_db_path) as store:
                    engine = SyncEngine(client=client, store=store, config=cfg.notion)
                    mappings = engine.get_sync_status()

                if mappings:
                    print()
                    print(f"Synced documents ({len(mappings)}):")
                    for m in mappings:
                        print(f"  {m['document_id'][:12]}  {m['title']}  [{m['status']}]")
                        print(f"    Notion: {m['notion_page_id'][:12]}  Last sync: {m['last_synced_at'] or 'never'}")
                else:
                    print()
                    print("No sync mappings yet. Run 'bigbrain notion sync' or 'bigbrain notion import'.")
        return 0

    elif action == "sync":
        from bigbrain.notion.sync import SyncEngine

        parent = args.parent_page_id if hasattr(args, 'parent_page_id') and args.parent_page_id else cfg.notion.default_page_id

        print("Syncing with Notion...")
        with SyncEngine.from_config(cfg) as engine:
            result = engine.sync(parent_page_id=parent)

        print()
        print("Sync complete:")
        print(f"  Imported:  {result.imported}")
        print(f"  Exported:  {result.exported}")
        print(f"  Skipped:   {result.skipped}")
        if result.conflicts:
            print(f"  Conflicts: {result.conflicts}")
        if result.errors:
            print(f"  Errors:    {len(result.errors)}")
            for e in result.errors[:5]:
                print(f"    \u2717 {e}")
        return 0

    elif action == "import":
        from bigbrain.notion.sync import SyncEngine

        query = args.query if hasattr(args, 'query') and args.query else ""
        max_pages = args.limit if hasattr(args, 'limit') else 20

        suffix = f" matching: {query}" if query else ""
        print(f"Importing Notion pages{suffix}...")
        with SyncEngine.from_config(cfg) as engine:
            result = engine.import_pages(query=query, max_pages=max_pages)

        print(f"  Imported: {result.imported}")
        if result.errors:
            print(f"  Errors:   {len(result.errors)}")
        return 0

    elif action == "export":
        from bigbrain.notion.sync import SyncEngine

        parent = args.parent_page_id if hasattr(args, 'parent_page_id') and args.parent_page_id else cfg.notion.default_page_id

        if not parent:
            print("Error: --parent-page-id is required for export (or set notion.default_page_id in config).")
            return 1

        source_type = args.type if hasattr(args, 'type') and args.type else None
        print("Exporting KB documents to Notion...")
        with SyncEngine.from_config(cfg) as engine:
            result = engine.export_documents(parent_page_id=parent, source_type=source_type)

        print(f"  Exported: {result.exported}")
        if result.errors:
            print(f"  Errors:   {len(result.errors)}")
        return 0

    else:
        print(f"Unknown action: {action}")
        return 1


def _add_notion_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``notion`` subcommand."""
    p = subparsers.add_parser(
        "notion",
        help="Manage Notion integration (sync, import, export)",
        description="Bidirectional sync between BigBrain KB and Notion workspace.",
    )
    p.add_argument(
        "action",
        choices=["sync", "import", "export", "status"],
        help="Notion action: sync (bidirectional), import (pull), export (push), status (check)",
    )
    p.add_argument(
        "--parent-page-id", type=str, default="",
        help="Notion parent page ID for exports/new pages",
    )
    p.add_argument(
        "--query", "-q", type=str, default="",
        help="Search query for Notion import (filters pages)",
    )
    p.add_argument(
        "--type", type=str, default="",
        help="Filter KB documents by source type for export",
    )
    p.add_argument(
        "--limit", type=int, default=20,
        help="Max pages to import (default: 20)",
    )
    p.set_defaults(func=_handle_notion)
    return p


def _handle_plugins(args: argparse.Namespace) -> int:
    """List discovered plugins."""
    from bigbrain.config import load_config
    from bigbrain.plugins.loader import PluginLoader

    cfg = load_config()
    loader = PluginLoader.from_config(cfg)
    count = loader.load_all()

    plugins = loader.list_plugins()

    if not plugins:
        print("No plugins discovered.")
        print(f"  Plugin directory: {cfg.plugins.plugins_dir}")
        print("  Place .py files with PluginBase subclasses in that directory.")
        return 0

    print(f"Discovered {count} plugin(s):")
    print()
    for info in plugins:
        print(f"  {info.name} v{info.version} [{info.plugin_type}]")
        if info.description:
            print(f"    {info.description}")

    loader.unload_all()
    return 0


def _add_plugins_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    """Register the ``plugins`` subcommand."""
    p = subparsers.add_parser(
        "plugins",
        help="List discovered plugins",
        description="Show installed and discovered BigBrain plugins.",
    )
    p.set_defaults(func=_handle_plugins)
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

    # Global logging options
    parser.add_argument(
        "--quiet", "-q", action="store_true", default=False,
        help="Suppress log output",
    )
    parser.add_argument(
        "--log-file", type=str, default="",
        help="Write logs to a file",
    )
    parser.add_argument(
        "--log-format", choices=["console", "json"], default="console",
        help="Log output format (default: console)",
    )

    subparsers = parser.add_subparsers(dest="command", title="commands")

    _add_ingest_parser(subparsers)
    _add_distill_parser(subparsers)
    _add_distill_show_parser(subparsers)
    _add_entities_parser(subparsers)
    _add_compact_parser(subparsers)
    _add_compile_parser(subparsers)
    _add_update_parser(subparsers)
    _add_status_parser(subparsers)
    _add_kb_search_parser(subparsers)
    _add_kb_export_parser(subparsers)
    _add_kb_import_parser(subparsers)
    _add_providers_parser(subparsers)
    _add_ask_parser(subparsers)
    _add_auth_parser(subparsers)
    _add_notion_parser(subparsers)
    _add_plugins_parser(subparsers)

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
    parser = build_parser()
    args = parser.parse_args(argv)

    # Configure logging using parsed CLI flags.
    try:
        from bigbrain.logging_config import setup_logging
        setup_logging(
            quiet=getattr(args, "quiet", False),
            log_file=getattr(args, "log_file", ""),
            log_format=getattr(args, "log_format", "console"),
        )
    except ImportError:
        pass

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
