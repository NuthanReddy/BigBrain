"""Tests for bigbrain.ingest.discovery."""

import os
import tempfile
from pathlib import Path

import pytest

from bigbrain.ingest.discovery import discover_files, DiscoveryResult
from bigbrain.errors import FileAccessError

from tests.conftest import FIXTURES_DIR


class TestDiscoverFiles:
    """Tests for discover_files()."""

    def test_discovers_files_in_directory(self):
        result = discover_files(FIXTURES_DIR, supported_extensions=[".txt", ".md", ".pdf", ".py"])
        assert isinstance(result, DiscoveryResult)
        assert len(result.files) > 0

    def test_respects_supported_extensions_filter(self):
        result = discover_files(FIXTURES_DIR, supported_extensions=[".txt"])
        extensions = {f.suffix.lower() for f in result.files}
        assert extensions <= {".txt"}
        # Should have skipped .md, .py, .pdf files
        assert len(result.skipped) > 0

    def test_recursive_traversal_finds_nested(self):
        result = discover_files(FIXTURES_DIR, recursive=True, supported_extensions=[".txt"])
        file_names = {f.name for f in result.files}
        assert "deep.txt" in file_names, "Recursive should find nested/deep.txt"

    def test_non_recursive_skips_nested(self):
        result = discover_files(FIXTURES_DIR, recursive=False, supported_extensions=[".txt"])
        file_names = {f.name for f in result.files}
        assert "deep.txt" not in file_names, "Non-recursive should not find nested/deep.txt"

    def test_skips_hidden_files_by_default(self, tmp_path):
        # Create a hidden file
        hidden_dir = tmp_path / ".hidden"
        hidden_dir.mkdir()
        hidden_file = hidden_dir / "secret.txt"
        hidden_file.write_text("hidden content")
        visible = tmp_path / "visible.txt"
        visible.write_text("visible content")

        result = discover_files(tmp_path, skip_hidden=True, supported_extensions=[".txt"])
        file_names = {f.name for f in result.files}
        assert "visible.txt" in file_names
        assert "secret.txt" not in file_names
        assert any("hidden" in s for s in result.skipped)

    def test_includes_hidden_files_when_skip_hidden_false(self, tmp_path):
        hidden_dir = tmp_path / ".hidden"
        hidden_dir.mkdir()
        hidden_file = hidden_dir / "secret.txt"
        hidden_file.write_text("hidden content")
        visible = tmp_path / "visible.txt"
        visible.write_text("visible content")

        result = discover_files(tmp_path, skip_hidden=False, supported_extensions=[".txt"])
        file_names = {f.name for f in result.files}
        assert "visible.txt" in file_names
        assert "secret.txt" in file_names

    def test_raises_file_access_error_for_nonexistent_path(self):
        with pytest.raises(FileAccessError):
            discover_files("/nonexistent/path/that/does/not/exist")

    def test_skips_files_over_max_file_size(self, tmp_path):
        large_file = tmp_path / "large.txt"
        # Write a file just over 1 MB
        large_file.write_text("x" * (1024 * 1024 + 1))
        small_file = tmp_path / "small.txt"
        small_file.write_text("small")

        result = discover_files(
            tmp_path,
            supported_extensions=[".txt"],
            max_file_size_mb=1,
        )
        file_names = {f.name for f in result.files}
        assert "small.txt" in file_names
        assert "large.txt" not in file_names
        assert any("too large" in s for s in result.skipped)

    def test_single_file_input(self):
        single = FIXTURES_DIR / "sample.txt"
        result = discover_files(single, supported_extensions=[".txt"])
        assert len(result.files) == 1
        assert result.files[0].name == "sample.txt"

    def test_single_file_unsupported_extension_returns_empty(self):
        unsupported = FIXTURES_DIR / "unsupported.xyz"
        result = discover_files(unsupported, supported_extensions=[".txt", ".md", ".py", ".pdf"])
        assert len(result.files) == 0
        assert len(result.skipped) > 0
