"""Python source file ingester with optional AST-based symbol extraction."""

from __future__ import annotations

import ast
from datetime import datetime
from pathlib import Path
from typing import Any

from bigbrain.ingest.registry import BaseIngester
from bigbrain.kb.models import Document, DocumentSection, SourceMetadata
from bigbrain.errors import FileAccessError
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


class PythonIngester(BaseIngester):
    """Ingests Python (.py) files, preserving source and extracting symbols."""

    def supported_extensions(self) -> list[str]:
        return [".py"]

    def ingest(self, path: Path) -> Document:
        path = Path(path).resolve()

        if not path.is_file():
            raise FileAccessError(str(path), "file not found")

        content = self._read_file(path)
        stat = path.stat()

        # AST analysis (best-effort, don't fail the whole ingest on syntax errors)
        module_docstring = ""
        symbols: list[dict[str, Any]] = []
        sections: list[DocumentSection] = []

        try:
            tree = ast.parse(content, filename=str(path))
            module_docstring = ast.get_docstring(tree) or ""
            symbols = self._extract_symbols(tree)
            sections = self._build_sections(tree, content)
        except SyntaxError as exc:
            logger.warning("Syntax error parsing %s: %s (line %s)", path, exc.msg, exc.lineno)

        # Title from module docstring first line, or filename
        title = ""
        if module_docstring:
            first_line = module_docstring.split("\n")[0].strip()
            if first_line:
                title = first_line
        if not title:
            title = path.stem.replace("_", " ").replace("-", " ").title()

        source = SourceMetadata(
            file_path=str(path),
            file_extension=".py",
            source_type="py",
            modified_at=datetime.fromtimestamp(stat.st_mtime),
            size_bytes=stat.st_size,
        )

        return Document(
            title=title,
            content=content,
            source=source,
            language="python",
            sections=sections,
            metadata={
                "module_docstring": module_docstring,
                "symbols": symbols,
                "symbol_count": len(symbols),
                "line_count": content.count("\n") + 1 if content else 0,
            },
        )

    def _extract_symbols(self, tree: ast.Module) -> list[dict[str, Any]]:
        """Extract top-level classes and functions."""
        symbols = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                symbols.append({
                    "type": "function",
                    "name": node.name,
                    "lineno": node.lineno,
                    "docstring": ast.get_docstring(node) or "",
                    "args": [arg.arg for arg in node.args.args],
                    "decorators": [
                        self._decorator_name(d) for d in node.decorator_list
                    ],
                })
            elif isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef):
                        methods.append(item.name)
                symbols.append({
                    "type": "class",
                    "name": node.name,
                    "lineno": node.lineno,
                    "docstring": ast.get_docstring(node) or "",
                    "methods": methods,
                    "bases": [self._node_name(b) for b in node.bases],
                    "decorators": [
                        self._decorator_name(d) for d in node.decorator_list
                    ],
                })
        return symbols

    def _build_sections(self, tree: ast.Module, content: str) -> list[DocumentSection]:
        """Build sections from top-level classes and functions."""
        lines = content.split("\n")
        sections: list[DocumentSection] = []

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
                kind = "class" if isinstance(node, ast.ClassDef) else "function"
                end_lineno = getattr(node, "end_lineno", node.lineno)
                section_lines = lines[node.lineno - 1 : end_lineno]
                sections.append(DocumentSection(
                    title=f"{kind}: {node.name}",
                    content="\n".join(section_lines),
                    level=1,
                    metadata={"kind": kind, "lineno": node.lineno},
                ))

        return sections

    @staticmethod
    def _decorator_name(node: ast.expr) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return ast.dump(node)
        if isinstance(node, ast.Call):
            return PythonIngester._decorator_name(node.func)
        return ast.dump(node)

    @staticmethod
    def _node_name(node: ast.expr) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{PythonIngester._node_name(node.value)}.{node.attr}"
        return ast.dump(node)

    def _read_file(self, path: Path) -> str:
        """Read Python source file."""
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            logger.warning("UTF-8 decode failed for %s, trying latin-1", path)
            try:
                return path.read_text(encoding="latin-1")
            except Exception as exc:
                raise FileAccessError(str(path), f"encoding error: {exc}") from exc
        except OSError as exc:
            raise FileAccessError(str(path), str(exc)) from exc
