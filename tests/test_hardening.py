"""Tests for Phase 10 production hardening: progress, retry, http, validation, logging."""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path

import pytest

from bigbrain.errors import ProviderError, UserError

# ---------------------------------------------------------------------------
# Progress
# ---------------------------------------------------------------------------


class TestProgressBar:
    """Tests for bigbrain.progress helpers."""

    def test_progress_bar_fallback(self, monkeypatch):
        """Non-interactive stderr yields a simple callable update."""
        import io
        from bigbrain.progress import progress_bar

        monkeypatch.setattr("sys.stderr", io.StringIO())
        with progress_bar(5, "Test") as update:
            assert callable(update)

    def test_progress_bar_completes(self, monkeypatch, capsys):
        """Running through all items prints progress output."""
        import io
        from bigbrain.progress import progress_bar

        monkeypatch.setattr("sys.stderr", io.StringIO())
        with progress_bar(10, "Items") as update:
            for _ in range(10):
                update(1)
        out = capsys.readouterr().out
        assert "Items" in out
        assert "10/10" in out


# ---------------------------------------------------------------------------
# Retry
# ---------------------------------------------------------------------------


class TestRetry:
    """Tests for with_retry decorator and CircuitBreaker."""

    def test_with_retry_succeeds_first_try(self):
        from bigbrain.retry import with_retry

        @with_retry(max_attempts=3, retry_on=(ValueError,), backoff_base=0.01, max_delay=0.1)
        def ok():
            return 42

        assert ok() == 42

    def test_with_retry_succeeds_after_failure(self):
        from bigbrain.retry import with_retry

        calls = [0]

        @with_retry(max_attempts=3, retry_on=(ValueError,), backoff_base=0.01, max_delay=0.1)
        def flaky():
            calls[0] += 1
            if calls[0] < 2:
                raise ValueError("fail")
            return "ok"

        assert flaky() == "ok"
        assert calls[0] == 2

    def test_with_retry_exhausts_retries(self):
        from bigbrain.retry import with_retry

        @with_retry(max_attempts=2, retry_on=(ValueError,), backoff_base=0.01, max_delay=0.1)
        def always_fails():
            raise ValueError("boom")

        with pytest.raises(ValueError, match="boom"):
            always_fails()

    def test_circuit_breaker_closed_by_default(self):
        from bigbrain.retry import CircuitBreaker

        cb = CircuitBreaker(failure_threshold=3)
        assert cb.is_open() is False
        assert cb.failure_count == 0

    def test_circuit_breaker_opens_after_threshold(self):
        from bigbrain.retry import CircuitBreaker

        cb = CircuitBreaker(failure_threshold=3, recovery_timeout=60)
        for _ in range(3):
            cb.record_failure()
        assert cb.is_open() is True

    def test_circuit_breaker_resets_on_success(self):
        from bigbrain.retry import CircuitBreaker

        cb = CircuitBreaker(failure_threshold=3)
        cb.record_failure()
        cb.record_failure()
        assert cb.failure_count == 2
        cb.record_success()
        assert cb.failure_count == 0
        assert cb.is_open() is False

    def test_circuit_breaker_recovers_after_timeout(self):
        from bigbrain.retry import CircuitBreaker

        cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.01)
        cb.record_failure()
        cb.record_failure()
        assert cb.is_open() is True
        time.sleep(0.02)
        assert cb.is_open() is False  # half-open after timeout
        assert cb.failure_count == 0


# ---------------------------------------------------------------------------
# HTTP client
# ---------------------------------------------------------------------------


class TestHttpClient:
    """Tests for the shared httpx client helpers."""

    def teardown_method(self):
        """Reset global client after each test."""
        import bigbrain.http as _mod
        if _mod._client is not None and not _mod._client.is_closed:
            _mod._client.close()
        _mod._client = None

    def test_get_http_client_returns_client(self):
        import httpx
        from bigbrain.http import get_http_client

        client = get_http_client()
        assert isinstance(client, httpx.Client)

    def test_get_http_client_reuses_same(self):
        from bigbrain.http import get_http_client

        c1 = get_http_client()
        c2 = get_http_client()
        assert c1 is c2

    def test_close_http_client(self):
        import bigbrain.http as _mod
        from bigbrain.http import close_http_client, get_http_client

        client = get_http_client()
        assert not client.is_closed
        close_http_client()
        assert _mod._client is None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestValidation:
    """Tests for input validation helpers."""

    def test_validate_url_valid(self):
        from bigbrain.validation import validate_url

        assert validate_url("https://example.com") == "https://example.com"
        assert validate_url("http://localhost:8080/v1") == "http://localhost:8080/v1"

    def test_validate_url_empty_raises(self):
        from bigbrain.validation import validate_url

        with pytest.raises(UserError, match="empty"):
            validate_url("")

    def test_validate_url_bad_scheme_raises(self):
        from bigbrain.validation import validate_url

        with pytest.raises(UserError, match="scheme"):
            validate_url("ftp://example.com")

    def test_validate_url_too_long_raises(self):
        from bigbrain.validation import validate_url

        with pytest.raises(UserError, match="too long"):
            validate_url("https://example.com/" + "a" * 2100)

    def test_validate_path_valid(self):
        from bigbrain.validation import validate_path

        result = validate_path(".")
        assert isinstance(result, Path)
        assert result.is_absolute()

    def test_validate_path_empty_raises(self):
        from bigbrain.validation import validate_path

        with pytest.raises(UserError, match="empty"):
            validate_path("")

    def test_validate_doc_id_valid(self):
        from bigbrain.validation import validate_doc_id

        assert validate_doc_id("abc123def456") == "abc123def456"

    def test_validate_doc_id_invalid_raises(self):
        from bigbrain.validation import validate_doc_id

        with pytest.raises(UserError, match="Invalid document ID"):
            validate_doc_id("not-hex!")

    def test_validate_notion_page_id_valid(self):
        from bigbrain.validation import validate_notion_page_id

        uuid = "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4"
        assert validate_notion_page_id(uuid) == uuid

    def test_validate_notion_page_id_invalid_raises(self):
        from bigbrain.validation import validate_notion_page_id

        with pytest.raises(UserError, match="Invalid Notion page ID"):
            validate_notion_page_id("not-a-uuid")

    def test_sanitize_text_truncates(self):
        from bigbrain.validation import sanitize_text

        long = "x" * 200
        result = sanitize_text(long, max_length=50)
        assert len(result) == 50

    def test_validate_model_name_valid(self):
        from bigbrain.validation import validate_model_name

        assert validate_model_name("gpt-4o") == "gpt-4o"
        assert validate_model_name("ollama/llama3:latest") == "ollama/llama3:latest"

    def test_validate_model_name_invalid_raises(self):
        from bigbrain.validation import validate_model_name

        with pytest.raises(UserError, match="Invalid model name"):
            validate_model_name("model name with spaces")


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


class TestLogging:
    """Tests for logging_config helpers."""

    def teardown_method(self):
        from bigbrain.logging_config import reset_logging
        reset_logging()

    def test_json_formatter_output(self):
        from bigbrain.logging_config import JsonFormatter

        fmt = JsonFormatter()
        record = logging.LogRecord(
            name="test.logger",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="hello %s",
            args=("world",),
            exc_info=None,
        )
        output = fmt.format(record)
        data = json.loads(output)
        assert data["level"] == "INFO"
        assert data["logger"] == "test.logger"
        assert data["message"] == "hello world"
        assert "timestamp" in data

    def test_setup_logging_quiet(self):
        from bigbrain.logging_config import setup_logging

        root = logging.getLogger()
        before = len(root.handlers)
        setup_logging(level="INFO", quiet=True)
        # quiet mode should NOT add a console handler
        assert len(root.handlers) == before

    def test_setup_logging_file(self, tmp_path):
        from bigbrain.logging_config import setup_logging

        log_file = tmp_path / "test.log"
        setup_logging(level="DEBUG", log_file=str(log_file))
        logging.getLogger().info("file test")
        # flush handlers
        for h in logging.getLogger().handlers:
            h.flush()
        assert log_file.exists()
        assert "file test" in log_file.read_text(encoding="utf-8")

    def test_reset_logging(self):
        from bigbrain.logging_config import reset_logging, setup_logging

        setup_logging(level="INFO")
        root = logging.getLogger()
        assert len(root.handlers) > 0
        reset_logging()
        assert len(root.handlers) == 0
        # After reset, setup_logging should work again (idempotency guard cleared)
        setup_logging(level="WARNING")
        assert len(root.handlers) > 0
