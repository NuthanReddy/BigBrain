"""End-to-end pipeline orchestrator with incremental processing."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from bigbrain.config import BigBrainConfig, load_config
from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger
from bigbrain.orchestrator.change_detector import ChangeDetector
from bigbrain.progress import progress_bar

logger = get_logger(__name__)


@dataclass
class OrchestratorResult:
    """Result of an end-to-end pipeline run."""
    ingested: int = 0
    skipped_unchanged: int = 0
    distilled: int = 0
    compiled: int = 0
    deleted: int = 0
    errors: list[str] = field(default_factory=list)
    steps_run: list[str] = field(default_factory=list)


class Orchestrator:
    """End-to-end pipeline: detect changes → ingest → distill → compile.

    Usage::
        orch = Orchestrator.from_config()
        result = orch.run(source="path/to/docs/")
        orch.close()
    """

    def __init__(self, store: KBStore, config: BigBrainConfig) -> None:
        self._store = store
        self._config = config
        self._detector = ChangeDetector(store)

    @classmethod
    def from_config(cls, config: BigBrainConfig | None = None) -> Orchestrator:
        if config is None:
            config = load_config()
        store = KBStore(config.kb_db_path)
        return cls(store=store, config=config)

    def close(self) -> None:
        self._store.close()

    def __enter__(self) -> Orchestrator:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def run(
        self,
        source: str | Path,
        *,
        force: bool = False,
        steps: set[str] | None = None,
        model: str = "",
        compile_format: str = "",
    ) -> OrchestratorResult:
        """Run the end-to-end pipeline.

        Args:
            source: Path to file or directory to process
            force: Skip change detection, reprocess everything
            steps: Which steps to run {"ingest", "distill", "compile"} (default: all)
            model: Override AI model for distill/compile
            compile_format: Output format for compile step
        """
        steps = steps or {"ingest", "distill", "compile"}
        result = OrchestratorResult()

        source_path = Path(source).resolve()

        # Step 1: Ingest (with change detection)
        if "ingest" in steps:
            result.steps_run.append("ingest")
            self._run_ingest(source_path, force=force, result=result)

        # Step 2: Distill
        if "distill" in steps:
            result.steps_run.append("distill")
            self._run_distill(force=force, model=model, result=result)

        # Step 3: Compile
        if "compile" in steps:
            result.steps_run.append("compile")
            self._run_compile(model=model, compile_format=compile_format, result=result)

        return result

    def _run_ingest(self, source_path: Path, *, force: bool, result: OrchestratorResult) -> None:
        """Ingest with incremental change detection."""
        from bigbrain.ingest.discovery import discover_files
        from bigbrain.ingest.registry import get_ingester, _init_default_ingesters

        _init_default_ingesters()

        # Discover files
        discovery = discover_files(
            source_path,
            supported_extensions=self._config.ingestion.supported_extensions,
            recursive=self._config.ingestion.recursive,
            skip_hidden=self._config.ingestion.skip_hidden,
            max_file_size_mb=self._config.ingestion.max_file_size_mb,
        )

        if not force:
            # Change detection
            changes = self._detector.scan(
                discovery.files,
                supported_extensions=self._config.ingestion.supported_extensions,
            )
            files_to_ingest = changes.changed_files
            result.skipped_unchanged = len(changes.unchanged_files)

            # Handle deletions
            for deleted_path in changes.deleted_paths:
                doc = self._store.get_document_by_source_path(deleted_path)
                if doc:
                    self._store.delete_document(doc.id)
                    self._detector.remove_file_record(deleted_path)
                    result.deleted += 1

            if not files_to_ingest:
                logger.info("No changes detected — skipping ingestion")
                return

            logger.info("Change detection: %d new, %d modified, %d unchanged, %d deleted",
                        len(changes.new_files), len(changes.modified_files),
                        len(changes.unchanged_files), len(changes.deleted_paths))
        else:
            files_to_ingest = discovery.files

        # Ingest changed files
        with progress_bar(len(files_to_ingest), "Ingesting") as update:
            for file_path in files_to_ingest:
                ext = file_path.suffix.lower()
                ingester = get_ingester(ext)
                if ingester is None:
                    update(1)
                    continue
                try:
                    doc = ingester.ingest(file_path)
                    self._store.save_document(doc)
                    self._detector.save_file_record(file_path)
                    result.ingested += 1
                    logger.info("Ingested: %s", file_path)
                except Exception as exc:
                    result.errors.append(f"ingest {file_path}: {exc}")
                    logger.error("Failed to ingest %s: %s", file_path, exc)
                update(1)

    def _run_distill(self, *, force: bool, model: str, result: OrchestratorResult) -> None:
        """Run distillation on KB documents."""
        from bigbrain.distill.pipeline import DistillPipeline
        from bigbrain.providers.registry import ProviderRegistry
        from bigbrain.stores.factory import create_entity_store

        registry = ProviderRegistry.from_config(self._config.providers)
        if not registry.has_providers():
            logger.warning("No AI providers available — skipping distillation")
            return

        entity_backend = create_entity_store(self._config.entity_store, self._store)
        pipeline = DistillPipeline(
            store=self._store, registry=registry, config=self._config.distillation,
            entity_store=entity_backend,
        )

        docs = self._store.list_documents(limit=9999)
        for doc in docs:
            try:
                pipeline.distill_document(doc, model=model, force=force)
                result.distilled += 1
            except Exception as exc:
                result.errors.append(f"distill {doc.title}: {exc}")
                logger.error("Distill failed for %s: %s", doc.title, exc)

    def _run_compile(self, *, model: str, compile_format: str, result: OrchestratorResult) -> None:
        """Run compilation on KB documents."""
        from bigbrain.compile.pipeline import CompilePipeline
        from bigbrain.providers.registry import ProviderRegistry

        registry = ProviderRegistry.from_config(self._config.providers)
        fmt = compile_format or self._config.compile.default_format

        pipeline = CompilePipeline(
            store=self._store, registry=registry, config=self._config.compile,
        )

        docs = self._store.list_documents(limit=9999)
        for doc in docs:
            try:
                pipeline.compile_document(doc.id, format=fmt, model=model)
                result.compiled += 1
            except Exception as exc:
                result.errors.append(f"compile {doc.title}: {exc}")
                logger.error("Compile failed for %s: %s", doc.title, exc)
