"""Tests for bigbrain.errors."""

from bigbrain.errors import (
    UserError,
    IngestionError,
    UnsupportedFormatError,
    FileAccessError,
    ConfigError,
)


class TestErrorHierarchy:
    """Tests for the error class hierarchy."""

    def test_user_error_is_base(self):
        assert issubclass(UserError, Exception)

    def test_ingestion_error_is_user_error(self):
        assert issubclass(IngestionError, UserError)

    def test_unsupported_format_is_ingestion_error(self):
        assert issubclass(UnsupportedFormatError, IngestionError)

    def test_file_access_error_is_ingestion_error(self):
        assert issubclass(FileAccessError, IngestionError)

    def test_config_error_is_user_error(self):
        assert issubclass(ConfigError, UserError)


class TestErrorMessages:
    """Tests for error message formatting."""

    def test_unsupported_format_message(self):
        err = UnsupportedFormatError(".xyz")
        assert ".xyz" in str(err)
        assert "Unsupported file format" in str(err)

    def test_unsupported_format_message_with_path(self):
        err = UnsupportedFormatError(".xyz", path="/some/file.xyz")
        msg = str(err)
        assert ".xyz" in msg
        assert "/some/file.xyz" in msg

    def test_file_access_error_message(self):
        err = FileAccessError("/some/file.txt", reason="not found")
        msg = str(err)
        assert "/some/file.txt" in msg
        assert "not found" in msg

    def test_file_access_error_without_reason(self):
        err = FileAccessError("/some/file.txt")
        msg = str(err)
        assert "/some/file.txt" in msg

    def test_error_attributes(self):
        err = UnsupportedFormatError(".xyz", path="/a/b.xyz")
        assert err.extension == ".xyz"
        assert err.path == "/a/b.xyz"

        err2 = FileAccessError("/a/b.txt", reason="denied")
        assert err2.path == "/a/b.txt"
        assert err2.reason == "denied"
