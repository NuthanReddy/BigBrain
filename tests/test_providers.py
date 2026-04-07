"""Comprehensive tests for Phase 3 AI provider integration.

All HTTP calls are mocked – no real LLM server needed.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx
import pytest

from bigbrain.errors import (
    NoProviderAvailableError,
    ProviderError,
    UserError,
)
from bigbrain.providers.base import BaseProvider, ProviderResponse
from bigbrain.providers.config import (
    GitHubCopilotConfig,
    LMStudioConfig,
    OllamaConfig,
    ProviderConfig,
)
from bigbrain.providers.github_auth import resolve_github_token, validate_token
from bigbrain.providers.github_copilot import GitHubCopilotProvider
from bigbrain.providers.lm_studio import LMStudioProvider
from bigbrain.providers.ollama import OllamaProvider
from bigbrain.providers.registry import ProviderRegistry


# ── helpers ──────────────────────────────────────────────────────────


def _mock_response(status_code: int = 200, json_data: dict | None = None) -> MagicMock:
    """Build a fake httpx.Response with the given status code and JSON body."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_data or {}
    resp.text = ""
    resp.raise_for_status = MagicMock()
    if status_code >= 400:
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "error", request=MagicMock(), response=resp,
        )
    return resp


class MockProvider(BaseProvider):
    """Lightweight mock provider for registry tests (no HTTP)."""

    def __init__(
        self,
        name: str,
        available: bool = True,
        fail_on_call: bool = False,
    ) -> None:
        self._name = name
        self._available = available
        self._fail = fail_on_call

    @property
    def name(self) -> str:
        return self._name

    def is_available(self) -> bool:
        return self._available

    def complete(self, prompt: str, *, model: str = "", **kwargs) -> ProviderResponse:
        if self._fail:
            raise ProviderError(self._name, "mock failure")
        return ProviderResponse(text=f"response from {self._name}", provider=self._name)

    def chat(self, messages, *, model: str = "", **kwargs) -> ProviderResponse:
        if self._fail:
            raise ProviderError(self._name, "mock failure")
        return ProviderResponse(text=f"chat from {self._name}", provider=self._name)


# =====================================================================
# 1. ProviderResponse
# =====================================================================


class TestProviderResponse:
    def test_default_values(self):
        r = ProviderResponse(text="hello")
        assert r.text == "hello"
        assert r.model == ""
        assert r.provider == ""
        assert r.usage == {}
        assert r.metadata == {}

    def test_custom_usage_and_metadata(self):
        r = ProviderResponse(
            text="ok",
            model="m1",
            provider="p1",
            usage={"prompt_tokens": 10, "completion_tokens": 20},
            metadata={"latency_ms": 123},
        )
        assert r.usage["prompt_tokens"] == 10
        assert r.usage["completion_tokens"] == 20
        assert r.metadata["latency_ms"] == 123
        assert r.model == "m1"
        assert r.provider == "p1"


# =====================================================================
# 2. ProviderConfig
# =====================================================================


class TestProviderConfig:
    def test_default_ollama_config(self):
        c = OllamaConfig()
        assert c.enabled is False
        assert c.base_url == "http://localhost:11434"
        assert c.default_model == "llama3.2"
        assert c.timeout == 120

    def test_default_lm_studio_config(self):
        c = LMStudioConfig()
        assert c.enabled is False
        assert c.base_url == "http://localhost:1234"
        assert c.default_model == ""
        assert c.timeout == 120

    def test_provider_config_constructs_nested_defaults(self):
        pc = ProviderConfig()
        assert isinstance(pc.ollama, OllamaConfig)
        assert isinstance(pc.lm_studio, LMStudioConfig)
        assert pc.ollama.enabled is False
        assert pc.lm_studio.enabled is False

    def test_config_with_custom_values(self):
        c = OllamaConfig(enabled=True, base_url="http://gpu:11434", default_model="mistral", timeout=60)
        assert c.enabled is True
        assert c.base_url == "http://gpu:11434"
        assert c.default_model == "mistral"
        assert c.timeout == 60


# =====================================================================
# 3. ProviderErrors
# =====================================================================


class TestProviderErrors:
    def test_provider_error_is_user_error(self):
        assert issubclass(ProviderError, UserError)

    def test_no_provider_available_error_is_provider_error(self):
        assert issubclass(NoProviderAvailableError, ProviderError)

    def test_provider_error_message_format(self):
        e = ProviderError("ollama", "connection refused")
        assert "ollama" in str(e)
        assert "connection refused" in str(e)

    def test_provider_error_message_without_reason(self):
        e = ProviderError("lm_studio")
        assert "lm_studio" in str(e)

    def test_no_provider_available_error_message_with_tried(self):
        e = NoProviderAvailableError(tried=["ollama", "lm_studio"])
        assert "ollama" in str(e)
        assert "lm_studio" in str(e)

    def test_no_provider_available_error_message_none_tried(self):
        e = NoProviderAvailableError(tried=[])
        assert "none configured" in str(e)


# =====================================================================
# 4. OllamaProvider (mocked HTTP)
# =====================================================================


class TestOllamaProvider:
    def _make_provider(self, **overrides) -> OllamaProvider:
        defaults = {"enabled": True, "base_url": "http://localhost:11434", "default_model": "llama3.2", "timeout": 30}
        defaults.update(overrides)
        return OllamaProvider(OllamaConfig(**defaults))

    # -- is_available ---------------------------------------------------

    @patch("httpx.get")
    def test_is_available_true(self, mock_get):
        mock_get.return_value = _mock_response(200)
        p = self._make_provider()
        assert p.is_available() is True

    @patch("httpx.get")
    def test_is_available_false_on_connect_error(self, mock_get):
        mock_get.side_effect = httpx.ConnectError("refused")
        p = self._make_provider()
        assert p.is_available() is False

    @patch("httpx.get")
    def test_is_available_false_on_timeout(self, mock_get):
        mock_get.side_effect = httpx.TimeoutException("timed out")
        p = self._make_provider()
        assert p.is_available() is False

    # -- complete -------------------------------------------------------

    @patch("httpx.post")
    def test_complete_returns_provider_response(self, mock_post):
        mock_post.return_value = _mock_response(200, {
            "response": "The answer is 42",
            "model": "llama3.2",
            "prompt_eval_count": 10,
            "eval_count": 5,
            "total_duration": 1_000_000,
            "eval_duration": 500_000,
        })
        p = self._make_provider()
        r = p.complete("What is the answer?")

        assert r.text == "The answer is 42"
        assert r.model == "llama3.2"
        assert r.provider == "ollama"
        assert r.usage["prompt_tokens"] == 10
        assert r.usage["completion_tokens"] == 5
        assert r.metadata["total_duration"] == 1_000_000

    @patch("httpx.post")
    def test_complete_raises_on_http_error(self, mock_post):
        mock_post.return_value = _mock_response(500, {})
        p = self._make_provider()
        with pytest.raises(ProviderError, match="ollama"):
            p.complete("fail")

    @patch("httpx.post")
    def test_complete_raises_on_timeout(self, mock_post):
        mock_post.side_effect = httpx.TimeoutException("timed out")
        p = self._make_provider()
        with pytest.raises(ProviderError, match="timed out"):
            p.complete("timeout")

    @patch("httpx.post")
    def test_complete_raises_on_connect_error(self, mock_post):
        mock_post.side_effect = httpx.ConnectError("refused")
        p = self._make_provider()
        with pytest.raises(ProviderError, match="Cannot connect"):
            p.complete("fail")

    def test_complete_raises_when_no_model(self):
        p = self._make_provider(default_model="")
        with pytest.raises(ProviderError, match="No model specified"):
            p.complete("prompt")

    # -- chat -----------------------------------------------------------

    @patch("httpx.post")
    def test_chat_returns_provider_response(self, mock_post):
        mock_post.return_value = _mock_response(200, {
            "message": {"role": "assistant", "content": "Hello!"},
            "model": "llama3.2",
            "prompt_eval_count": 8,
            "eval_count": 3,
        })
        p = self._make_provider()
        msgs = [{"role": "user", "content": "Hi"}]
        r = p.chat(msgs)

        assert r.text == "Hello!"
        assert r.model == "llama3.2"
        assert r.provider == "ollama"
        assert r.usage["prompt_tokens"] == 8
        assert r.usage["completion_tokens"] == 3

    @patch("httpx.post")
    def test_chat_raises_on_connect_error(self, mock_post):
        mock_post.side_effect = httpx.ConnectError("refused")
        p = self._make_provider()
        with pytest.raises(ProviderError, match="Cannot connect"):
            p.chat([{"role": "user", "content": "Hi"}])

    def test_chat_raises_when_no_model(self):
        p = self._make_provider(default_model="")
        with pytest.raises(ProviderError, match="No model specified"):
            p.chat([{"role": "user", "content": "Hi"}])

    # -- list_models ----------------------------------------------------

    @patch("httpx.get")
    def test_list_models_returns_names(self, mock_get):
        mock_get.return_value = _mock_response(200, {
            "models": [{"name": "llama3.2"}, {"name": "mistral"}],
        })
        p = self._make_provider()
        assert p.list_models() == ["llama3.2", "mistral"]

    @patch("httpx.get")
    def test_list_models_returns_empty_on_error(self, mock_get):
        mock_get.side_effect = httpx.ConnectError("refused")
        p = self._make_provider()
        assert p.list_models() == []

    # -- summarize (inherited default implementation) -------------------

    @patch("httpx.post")
    def test_summarize_calls_complete_with_prompt(self, mock_post):
        mock_post.return_value = _mock_response(200, {
            "response": "Short summary.",
            "model": "llama3.2",
        })
        p = self._make_provider()
        r = p.summarize("A very long text about many things.")
        assert r.text == "Short summary."
        # Verify the prompt included summarization instructions
        call_payload = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1]["json"]
        assert "Summarize" in call_payload["prompt"]

    # -- kwargs forwarding ----------------------------------------------

    @patch("httpx.post")
    def test_complete_forwards_temperature_and_max_tokens(self, mock_post):
        mock_post.return_value = _mock_response(200, {"response": "ok", "model": "llama3.2"})
        p = self._make_provider()
        p.complete("test", temperature=0.5, max_tokens=100)
        payload = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1]["json"]
        assert payload["options"]["temperature"] == 0.5
        assert payload["options"]["num_predict"] == 100


# =====================================================================
# 5. LMStudioProvider (mocked HTTP)
# =====================================================================


class TestLMStudioProvider:
    def _make_provider(self, **overrides) -> LMStudioProvider:
        defaults = {"enabled": True, "base_url": "http://localhost:1234", "default_model": "local-model", "timeout": 30}
        defaults.update(overrides)
        return LMStudioProvider(LMStudioConfig(**defaults))

    # -- is_available ---------------------------------------------------

    @patch("httpx.get")
    def test_is_available_true(self, mock_get):
        mock_get.return_value = _mock_response(200)
        p = self._make_provider()
        assert p.is_available() is True

    @patch("httpx.get")
    def test_is_available_false_on_connect_error(self, mock_get):
        mock_get.side_effect = httpx.ConnectError("refused")
        p = self._make_provider()
        assert p.is_available() is False

    @patch("httpx.get")
    def test_is_available_false_on_timeout(self, mock_get):
        mock_get.side_effect = httpx.TimeoutException("timed out")
        p = self._make_provider()
        assert p.is_available() is False

    # -- complete -------------------------------------------------------

    @patch("httpx.post")
    def test_complete_returns_provider_response(self, mock_post):
        mock_post.return_value = _mock_response(200, {
            "choices": [{"text": "result"}],
            "model": "local-model",
            "usage": {"prompt_tokens": 5, "completion_tokens": 10},
        })
        p = self._make_provider()
        r = p.complete("Generate something")

        assert r.text == "result"
        assert r.model == "local-model"
        assert r.provider == "lm_studio"
        assert r.usage["prompt_tokens"] == 5
        assert r.usage["completion_tokens"] == 10

    @patch("httpx.post")
    def test_complete_raises_on_http_error(self, mock_post):
        mock_post.return_value = _mock_response(500)
        p = self._make_provider()
        with pytest.raises(ProviderError, match="lm_studio"):
            p.complete("fail")

    @patch("httpx.post")
    def test_complete_raises_on_timeout(self, mock_post):
        mock_post.side_effect = httpx.TimeoutException("timed out")
        p = self._make_provider()
        with pytest.raises(ProviderError, match="timed out"):
            p.complete("timeout")

    @patch("httpx.post")
    def test_complete_raises_on_connect_error(self, mock_post):
        mock_post.side_effect = httpx.ConnectError("refused")
        p = self._make_provider()
        with pytest.raises(ProviderError, match="Cannot connect"):
            p.complete("fail")

    # -- chat -----------------------------------------------------------

    @patch("httpx.post")
    def test_chat_returns_provider_response(self, mock_post):
        mock_post.return_value = _mock_response(200, {
            "choices": [{"message": {"content": "Hi"}}],
            "model": "local-model",
            "usage": {"prompt_tokens": 3, "completion_tokens": 7},
        })
        p = self._make_provider()
        r = p.chat([{"role": "user", "content": "Hello"}])

        assert r.text == "Hi"
        assert r.model == "local-model"
        assert r.provider == "lm_studio"
        assert r.usage["prompt_tokens"] == 3
        assert r.usage["completion_tokens"] == 7

    @patch("httpx.post")
    def test_chat_raises_on_connect_error(self, mock_post):
        mock_post.side_effect = httpx.ConnectError("refused")
        p = self._make_provider()
        with pytest.raises(ProviderError, match="Cannot connect"):
            p.chat([{"role": "user", "content": "Hi"}])

    @patch("httpx.post")
    def test_chat_raises_on_timeout(self, mock_post):
        mock_post.side_effect = httpx.TimeoutException("timed out")
        p = self._make_provider()
        with pytest.raises(ProviderError, match="timed out"):
            p.chat([{"role": "user", "content": "Hi"}])

    # -- list_models ----------------------------------------------------

    @patch("httpx.get")
    def test_list_models_returns_ids(self, mock_get):
        mock_get.return_value = _mock_response(200, {
            "data": [{"id": "model-1"}, {"id": "model-2"}],
        })
        p = self._make_provider()
        assert p.list_models() == ["model-1", "model-2"]

    @patch("httpx.get")
    def test_list_models_returns_empty_on_error(self, mock_get):
        mock_get.side_effect = httpx.ConnectError("refused")
        p = self._make_provider()
        assert p.list_models() == []

    # -- kwargs forwarding ----------------------------------------------

    @patch("httpx.post")
    def test_complete_forwards_temperature_and_max_tokens(self, mock_post):
        mock_post.return_value = _mock_response(200, {
            "choices": [{"text": "ok"}],
            "model": "local-model",
            "usage": {},
        })
        p = self._make_provider()
        p.complete("test", temperature=0.7, max_tokens=200)
        payload = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1]["json"]
        assert payload["temperature"] == 0.7
        assert payload["max_tokens"] == 200

    # -- complete with empty choices ------------------------------------

    @patch("httpx.post")
    def test_complete_empty_choices_returns_empty_text(self, mock_post):
        mock_post.return_value = _mock_response(200, {"choices": [], "model": "m", "usage": {}})
        p = self._make_provider()
        r = p.complete("test")
        assert r.text == ""

    @patch("httpx.post")
    def test_chat_empty_choices_returns_empty_text(self, mock_post):
        mock_post.return_value = _mock_response(200, {"choices": [], "model": "m", "usage": {}})
        p = self._make_provider()
        r = p.chat([{"role": "user", "content": "Hi"}])
        assert r.text == ""


# =====================================================================
# 6. ProviderRegistry (mock providers, no HTTP)
# =====================================================================


class TestProviderRegistry:
    # -- basic state ----------------------------------------------------

    def test_has_providers_false_when_empty(self):
        reg = ProviderRegistry()
        assert reg.has_providers() is False

    def test_has_providers_true_after_register(self):
        reg = ProviderRegistry()
        reg.register(MockProvider("mock"))
        assert reg.has_providers() is True

    def test_list_providers_returns_registered_names(self):
        reg = ProviderRegistry()
        reg.register(MockProvider("alpha"))
        reg.register(MockProvider("beta"))
        assert reg.list_providers() == ["alpha", "beta"]

    # -- from_config ----------------------------------------------------

    def test_from_config_no_providers_enabled(self):
        cfg = ProviderConfig()  # both disabled by default
        reg = ProviderRegistry.from_config(cfg)
        assert reg.has_providers() is False

    def test_from_config_ollama_enabled(self):
        cfg = ProviderConfig(ollama=OllamaConfig(enabled=True))
        reg = ProviderRegistry.from_config(cfg)
        assert reg.has_providers() is True
        assert "ollama" in reg.list_providers()

    def test_from_config_lm_studio_enabled(self):
        cfg = ProviderConfig(lm_studio=LMStudioConfig(enabled=True))
        reg = ProviderRegistry.from_config(cfg)
        assert "lm_studio" in reg.list_providers()

    def test_from_config_both_enabled(self):
        cfg = ProviderConfig(
            ollama=OllamaConfig(enabled=True),
            lm_studio=LMStudioConfig(enabled=True),
        )
        reg = ProviderRegistry.from_config(cfg)
        assert len(reg.list_providers()) == 2

    # -- get_provider ---------------------------------------------------

    def test_get_provider_raises_when_empty(self):
        reg = ProviderRegistry()
        with pytest.raises(NoProviderAvailableError):
            reg.get_provider()

    def test_get_provider_returns_first_available(self):
        reg = ProviderRegistry()
        reg.register(MockProvider("first"))
        reg.register(MockProvider("second"))
        p = reg.get_provider()
        assert p.name == "first"

    def test_get_provider_skips_unavailable(self):
        reg = ProviderRegistry()
        reg.register(MockProvider("down", available=False))
        reg.register(MockProvider("up", available=True))
        p = reg.get_provider()
        assert p.name == "up"

    def test_get_provider_raises_when_all_unavailable(self):
        reg = ProviderRegistry()
        reg.register(MockProvider("a", available=False))
        reg.register(MockProvider("b", available=False))
        with pytest.raises(NoProviderAvailableError):
            reg.get_provider()

    # -- health_check ---------------------------------------------------

    def test_health_check_returns_dict(self):
        reg = ProviderRegistry()
        reg.register(MockProvider("up", available=True))
        reg.register(MockProvider("down", available=False))
        result = reg.health_check()
        assert result == {"up": True, "down": False}

    # -- fallback: complete ---------------------------------------------

    def test_complete_uses_first_provider(self):
        reg = ProviderRegistry()
        reg.register(MockProvider("first"))
        reg.register(MockProvider("second"))
        r = reg.complete("test")
        assert r.provider == "first"
        assert "response from first" in r.text

    def test_complete_falls_back_on_failure(self):
        reg = ProviderRegistry()
        reg.register(MockProvider("failing", fail_on_call=True))
        reg.register(MockProvider("working"))
        r = reg.complete("test")
        assert r.provider == "working"

    def test_complete_raises_when_all_fail(self):
        reg = ProviderRegistry()
        reg.register(MockProvider("a", fail_on_call=True))
        reg.register(MockProvider("b", fail_on_call=True))
        with pytest.raises(NoProviderAvailableError):
            reg.complete("test")

    def test_complete_raises_when_no_providers(self):
        reg = ProviderRegistry()
        with pytest.raises(NoProviderAvailableError):
            reg.complete("test")

    # -- fallback: chat -------------------------------------------------

    def test_chat_uses_first_provider(self):
        reg = ProviderRegistry()
        reg.register(MockProvider("first"))
        msgs = [{"role": "user", "content": "Hi"}]
        r = reg.chat(msgs)
        assert "chat from first" in r.text

    def test_chat_falls_back_on_failure(self):
        reg = ProviderRegistry()
        reg.register(MockProvider("failing", fail_on_call=True))
        reg.register(MockProvider("backup"))
        r = reg.chat([{"role": "user", "content": "Hi"}])
        assert r.provider == "backup"

    def test_chat_raises_when_all_fail(self):
        reg = ProviderRegistry()
        reg.register(MockProvider("x", fail_on_call=True))
        with pytest.raises(NoProviderAvailableError):
            reg.chat([{"role": "user", "content": "Hi"}])

    # -- get_available_providers ----------------------------------------

    def test_get_available_providers(self):
        reg = ProviderRegistry()
        reg.register(MockProvider("up1", available=True))
        reg.register(MockProvider("down", available=False))
        reg.register(MockProvider("up2", available=True))
        avail = reg.get_available_providers()
        names = [p.name for p in avail]
        assert names == ["up1", "up2"]


# =====================================================================
# 7. GitHubAuth (github_auth.py)
# =====================================================================


class TestGitHubAuth:
    def test_resolve_token_from_config(self):
        """Config value takes priority over environment."""
        token = resolve_github_token(config_token="ghp_config_token_12345")
        assert token == "ghp_config_token_12345"

    @patch.dict("os.environ", {"GITHUB_TOKEN": "ghp_env_token_67890"})
    def test_resolve_token_from_env(self):
        """Falls back to GITHUB_TOKEN env var when config is empty."""
        token = resolve_github_token(config_token="")
        assert token == "ghp_env_token_67890"

    @patch.dict("os.environ", {}, clear=True)
    def test_resolve_token_empty(self):
        """Returns empty string when nothing is set."""
        # Remove GITHUB_TOKEN if present
        import os
        os.environ.pop("GITHUB_TOKEN", None)
        token = resolve_github_token(config_token="")
        assert token == ""

    def test_validate_token_valid(self):
        """Accepts tokens >= 10 chars."""
        assert validate_token("ghp_1234567890") is True
        assert validate_token("a" * 10) is True

    def test_validate_token_empty(self):
        """Rejects empty/short tokens."""
        assert validate_token("") is False
        assert validate_token("   ") is False
        assert validate_token("short") is False


# =====================================================================
# 8. GitHubCopilotProvider (mocked HTTP)
# =====================================================================


class TestGitHubCopilotProvider:
    def _make_provider(self, **overrides) -> GitHubCopilotProvider:
        defaults = {
            "enabled": True,
            "api_token": "ghp_test_token_1234567890",
            "base_url": "https://api.githubcopilot.com",
            "default_model": "gpt-4o",
            "timeout": 30,
            "max_retries": 3,
            "retry_delay": 0.01,
        }
        defaults.update(overrides)
        return GitHubCopilotProvider(GitHubCopilotConfig(**defaults))

    # -- is_available ---------------------------------------------------

    def test_is_available_no_token(self):
        """Returns False when no valid token is configured."""
        p = self._make_provider(api_token="")
        # Clear env to ensure no fallback
        with patch.dict("os.environ", {}, clear=True):
            import os
            os.environ.pop("GITHUB_TOKEN", None)
            assert p.is_available() is False

    @patch("httpx.get")
    def test_is_available_with_token(self, mock_get):
        """Returns True when API responds successfully."""
        mock_get.return_value = _mock_response(200, {"data": []})
        p = self._make_provider()
        assert p.is_available() is True

    # -- complete delegates to chat -------------------------------------

    @patch("httpx.post")
    def test_complete_delegates_to_chat(self, mock_post):
        """Verify complete() calls chat() under the hood."""
        mock_post.return_value = _mock_response(200, {
            "choices": [{"message": {"content": "delegated"}}],
            "model": "gpt-4o",
            "usage": {"prompt_tokens": 5, "completion_tokens": 3},
        })
        p = self._make_provider()
        r = p.complete("test prompt")
        assert r.text == "delegated"
        # Verify the POST payload wraps prompt in a user message
        payload = mock_post.call_args.kwargs.get("json") or mock_post.call_args[1]["json"]
        assert payload["messages"] == [{"role": "user", "content": "test prompt"}]

    # -- chat success ---------------------------------------------------

    @patch("httpx.post")
    def test_chat_success(self, mock_post):
        """Mock POST returning OpenAI-format response."""
        mock_post.return_value = _mock_response(200, {
            "choices": [{"message": {"content": "Hello from Copilot!"}}],
            "model": "gpt-4o",
            "usage": {"prompt_tokens": 10, "completion_tokens": 8},
        })
        p = self._make_provider()
        msgs = [{"role": "user", "content": "Hi"}]
        r = p.chat(msgs)

        assert r.text == "Hello from Copilot!"
        assert r.model == "gpt-4o"
        assert r.provider == "github_copilot"
        assert r.usage["prompt_tokens"] == 10
        assert r.usage["completion_tokens"] == 8

    # -- auth failure ---------------------------------------------------

    @patch("httpx.post")
    def test_chat_auth_failure(self, mock_post):
        """401 raises ProviderError with auth message."""
        mock_post.return_value = _mock_response(401, {})
        p = self._make_provider()
        with pytest.raises(ProviderError, match="Authentication failed"):
            p.chat([{"role": "user", "content": "Hi"}])

    # -- rate limiting --------------------------------------------------

    @patch("httpx.post")
    def test_chat_rate_limited_then_success(self, mock_post):
        """First call returns 429, retry succeeds."""
        rate_resp = _mock_response(429, {})
        rate_resp.headers = {"Retry-After": "0.01"}
        ok_resp = _mock_response(200, {
            "choices": [{"message": {"content": "ok"}}],
            "model": "gpt-4o",
            "usage": {},
        })
        mock_post.side_effect = [rate_resp, ok_resp]
        p = self._make_provider(retry_delay=0.01)
        r = p.chat([{"role": "user", "content": "Hi"}])
        assert r.text == "ok"
        assert mock_post.call_count == 2

    # -- no token raises ------------------------------------------------

    def test_chat_no_token_raises(self):
        """Raises ProviderError about missing token."""
        with patch.dict("os.environ", {}, clear=True):
            import os
            os.environ.pop("GITHUB_TOKEN", None)
            p = self._make_provider(api_token="")
            with pytest.raises(ProviderError, match="No valid API token"):
                p.chat([{"role": "user", "content": "Hi"}])

    # -- timeout retries ------------------------------------------------

    @patch("httpx.post")
    def test_chat_timeout_retries(self, mock_post):
        """httpx.TimeoutException triggers retry."""
        ok_resp = _mock_response(200, {
            "choices": [{"message": {"content": "recovered"}}],
            "model": "gpt-4o",
            "usage": {},
        })
        mock_post.side_effect = [
            httpx.TimeoutException("timed out"),
            ok_resp,
        ]
        p = self._make_provider(retry_delay=0.01)
        r = p.chat([{"role": "user", "content": "Hi"}])
        assert r.text == "recovered"
        assert mock_post.call_count == 2

    # -- list_models ----------------------------------------------------

    @patch("httpx.get")
    def test_list_models(self, mock_get):
        """Mock GET /models response."""
        mock_get.return_value = _mock_response(200, {
            "data": [{"id": "gpt-4o"}, {"id": "gpt-4o-mini"}],
        })
        p = self._make_provider()
        models = p.list_models()
        assert models == ["gpt-4o", "gpt-4o-mini"]


# =====================================================================
# 9. PreferredProvider (registry preferred routing)
# =====================================================================


class TestPreferredProvider:
    def test_preferred_provider_tried_first(self):
        """Register A, B with preferred=B; verify B is called first."""
        reg = ProviderRegistry(preferred="beta")
        reg.register(MockProvider("alpha"))
        reg.register(MockProvider("beta"))
        r = reg.complete("test")
        assert r.provider == "beta"

    def test_preferred_unavailable_falls_back(self):
        """Preferred provider fails, next provider succeeds."""
        reg = ProviderRegistry(preferred="failing")
        reg.register(MockProvider("failing", fail_on_call=True))
        reg.register(MockProvider("backup"))
        r = reg.complete("test")
        assert r.provider == "backup"

    def test_preferred_empty_uses_registration_order(self):
        """No preferred set, uses normal registration order."""
        reg = ProviderRegistry(preferred="")
        reg.register(MockProvider("first"))
        reg.register(MockProvider("second"))
        r = reg.complete("test")
        assert r.provider == "first"

    def test_preferred_property(self):
        """registry.preferred returns the configured value."""
        reg = ProviderRegistry(preferred="ollama")
        assert reg.preferred == "ollama"
        reg2 = ProviderRegistry()
        assert reg2.preferred == ""

    def test_from_config_passes_preferred(self):
        """from_config reads preferred_provider field."""
        cfg = ProviderConfig(
            preferred_provider="ollama",
            ollama=OllamaConfig(enabled=True),
        )
        reg = ProviderRegistry.from_config(cfg)
        assert reg.preferred == "ollama"
