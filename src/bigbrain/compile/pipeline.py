"""Compilation pipeline — orchestrates rendering distilled content into output formats."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from bigbrain.compile.cheatsheet import CheatsheetCompiler
from bigbrain.compile.flashcard import FlashcardCompiler
from bigbrain.compile.markdown import MarkdownCompiler
from bigbrain.compile.models import CompileOutput, CompileResult, OutputFormat
from bigbrain.compile.qa_generator import QAGenerator
from bigbrain.compile.study_guide import StudyGuideCompiler
from bigbrain.config import BigBrainConfig, CompileConfig, load_config
from bigbrain.kb.store import KBStore
from bigbrain.logging_config import get_logger
from bigbrain.providers.registry import ProviderRegistry

logger = get_logger(__name__)


class CompilePipeline:
    """Orchestrates compilation of distilled content into output formats.

    Usage::

        pipeline = CompilePipeline.from_config()
        output = pipeline.compile_document(doc_id, format="flashcard")
        pipeline.close()
    """

    def __init__(
        self,
        store: KBStore,
        registry: ProviderRegistry | None = None,
        config: CompileConfig | None = None,
    ) -> None:
        self._store = store
        self._registry = registry or ProviderRegistry()
        self._config = config or CompileConfig()

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def from_config(cls, config: BigBrainConfig | None = None) -> CompilePipeline:
        """Build a pipeline from the application config."""
        if config is None:
            config = load_config()
        store = KBStore(config.kb_db_path)
        registry = ProviderRegistry.from_config(config.providers)
        return cls(store=store, registry=registry, config=config.compile)

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Release resources held by the pipeline."""
        self._store.close()

    def __enter__(self) -> CompilePipeline:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def compile_document(
        self,
        doc_id: str,
        *,
        format: str = "",
        model: str = "",
        output_path: str = "",
    ) -> CompileOutput | None:
        """Compile a single document into the specified format.

        Parameters
        ----------
        doc_id:
            Knowledge-base document identifier.
        format:
            Output format name (``markdown``, ``flashcard``, ``cheatsheet``,
            ``qa``, ``study_guide``).  Falls back to ``CompileConfig.default_format``.
        model:
            Optional model override passed to AI-backed compilers.
        output_path:
            Explicit file path for the rendered output.  When empty the
            pipeline auto-generates a path under ``CompileConfig.output_dir``.
        """
        fmt = format or self._config.default_format

        doc = self._store.get_document(doc_id)
        if doc is None:
            logger.warning("Document not found: %s", doc_id)
            return None

        summaries = self._store.get_summaries(doc_id)
        entities = (
            self._store.get_entities(doc_id) if self._config.include_entities else []
        )
        relationships = (
            self._store.get_relationships(doc_id)
            if self._config.include_relationships
            else []
        )

        logger.info(
            "Compiling %s as %s (%d summaries, %d entities, %d relationships)",
            doc.title,
            fmt,
            len(summaries),
            len(entities),
            len(relationships),
        )

        output = self._dispatch(
            fmt, doc, summaries, entities, relationships, model=model
        )

        if output and output_path:
            self._write_output(output, output_path)
        elif output and not output_path:
            auto_path = self._auto_output_path(doc.title, fmt)
            self._write_output(output, str(auto_path))
            output.metadata["output_path"] = str(auto_path)

        return output

    def compile_all(
        self,
        *,
        format: str = "",
        model: str = "",
        source_type: str | None = None,
    ) -> CompileResult:
        """Compile every document in the knowledge base.

        Parameters
        ----------
        format:
            Output format (defaults to config).
        model:
            Optional model override for AI compilers.
        source_type:
            If provided, only documents of this type are compiled.
        """
        fmt = format or self._config.default_format
        docs = self._store.list_documents(source_type=source_type, limit=9999)

        result = CompileResult(total_documents=len(docs))

        for doc in docs:
            try:
                output = self.compile_document(doc.id, format=fmt, model=model)
                if output:
                    result.outputs.append(output)
            except Exception as exc:
                logger.error("Failed to compile %s: %s", doc.title, exc)
                result.errors.append(f"{doc.title}: {exc}")

        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _dispatch(self, fmt, doc, summaries, entities, relationships, *, model):
        """Dispatch to the appropriate compiler based on *fmt*."""
        if fmt == OutputFormat.MARKDOWN.value:
            return MarkdownCompiler().compile(doc, summaries, entities, relationships)

        if fmt == OutputFormat.FLASHCARD.value:
            return FlashcardCompiler(self._registry).compile(
                doc,
                summaries,
                entities,
                max_cards=self._config.flashcard_count,
                model=model,
            )

        if fmt == OutputFormat.CHEATSHEET.value:
            return CheatsheetCompiler().compile(doc, entities, relationships)

        if fmt == OutputFormat.QA.value:
            return QAGenerator(self._registry).compile(
                doc,
                summaries,
                entities,
                max_pairs=self._config.qa_count,
                model=model,
            )

        if fmt == OutputFormat.STUDY_GUIDE.value:
            return StudyGuideCompiler(self._registry).compile(
                doc, summaries, entities, relationships, model=model
            )

        logger.warning("Unknown format '%s', falling back to markdown", fmt)
        return MarkdownCompiler().compile(doc, summaries, entities, relationships)

    def _auto_output_path(self, title: str, fmt: str) -> Path:
        """Derive an output file path from the document title and format."""
        out_dir = Path(self._config.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        safe = (
            "".join(c if c.isalnum() or c in "-_ " else "" for c in title)[:60]
            .strip()
            .replace(" ", "-")
            .lower()
        )
        return out_dir / f"{safe}-{fmt}.md"

    @staticmethod
    def _write_output(output: CompileOutput, path: str) -> None:
        """Write compiled output to a file."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(output.content, encoding="utf-8")
        logger.info("Wrote compiled output to %s", p)
