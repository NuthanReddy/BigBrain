"""Ollama provider – local LLM inference via the Ollama REST API.

Ollama API docs: https://github.com/ollama/ollama/blob/main/docs/api.md

Key endpoints:
- POST /api/generate  — text completion
- POST /api/chat      — chat completion
- GET  /api/tags      — list available models
- GET  /               — health check (returns "Ollama is running")
"""

from __future__ import annotations

from typing import Any

import httpx

from bigbrain.errors import ProviderError
from bigbrain.logging_config import get_logger
from bigbrain.providers.base import BaseProvider, ProviderResponse
from bigbrain.providers.config import OllamaConfig

logger = get_logger(__name__)


class OllamaProvider(BaseProvider):
    """Ollama local LLM provider."""

    def __init__(self, config: OllamaConfig) -> None:
        self._config = config
        self._base_url = config.base_url.rstrip("/")
        self._timeout = config.timeout

    @property
    def name(self) -> str:
        return "ollama"

    def is_available(self) -> bool:
        """Check if Ollama is running by hitting the root endpoint."""
        try:
            resp = httpx.get(
                self._base_url,
                timeout=5.0,
            )
            return resp.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException, OSError):
            return False

    def list_models(self) -> list[str]:
        """Return list of available model names from Ollama."""
        try:
            resp = httpx.get(
                f"{self._base_url}/api/tags",
                timeout=10.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return [m["name"] for m in data.get("models", [])]
        except Exception as exc:
            logger.warning("Failed to list Ollama models: %s", exc)
            return []

    def complete(
        self, prompt: str, *, model: str = "", **kwargs: Any
    ) -> ProviderResponse:
        """Send a generation request to Ollama POST /api/generate."""
        model = model or self._config.default_model
        if not model:
            raise ProviderError(
                "ollama", "No model specified and no default_model configured"
            )

        payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
        if "temperature" in kwargs:
            payload.setdefault("options", {})["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            payload.setdefault("options", {})["num_predict"] = kwargs["max_tokens"]

        try:
            resp = httpx.post(
                f"{self._base_url}/api/generate",
                json=payload,
                timeout=self._timeout,
            )
            resp.raise_for_status()
            data = resp.json()
        except httpx.TimeoutException:
            raise ProviderError(
                "ollama", f"Request timed out after {self._timeout}s"
            )
        except httpx.HTTPStatusError as exc:
            raise ProviderError(
                "ollama",
                f"HTTP {exc.response.status_code}: {exc.response.text[:200]}",
            )
        except httpx.ConnectError:
            raise ProviderError(
                "ollama", f"Cannot connect to {self._base_url}"
            )
        except Exception as exc:
            raise ProviderError("ollama", str(exc))

        return ProviderResponse(
            text=data.get("response", ""),
            model=data.get("model", model),
            provider="ollama",
            usage={
                "prompt_tokens": data.get("prompt_eval_count", 0),
                "completion_tokens": data.get("eval_count", 0),
            },
            metadata={
                "total_duration": data.get("total_duration"),
                "eval_duration": data.get("eval_duration"),
            },
        )

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str = "",
        **kwargs: Any,
    ) -> ProviderResponse:
        """Send a chat request to Ollama POST /api/chat."""
        model = model or self._config.default_model
        if not model:
            raise ProviderError(
                "ollama", "No model specified and no default_model configured"
            )

        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
        }
        if "temperature" in kwargs:
            payload.setdefault("options", {})["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            payload.setdefault("options", {})["num_predict"] = kwargs["max_tokens"]

        try:
            resp = httpx.post(
                f"{self._base_url}/api/chat",
                json=payload,
                timeout=self._timeout,
            )
            resp.raise_for_status()
            data = resp.json()
        except httpx.TimeoutException:
            raise ProviderError(
                "ollama", f"Request timed out after {self._timeout}s"
            )
        except httpx.HTTPStatusError as exc:
            raise ProviderError(
                "ollama",
                f"HTTP {exc.response.status_code}: {exc.response.text[:200]}",
            )
        except httpx.ConnectError:
            raise ProviderError(
                "ollama", f"Cannot connect to {self._base_url}"
            )
        except Exception as exc:
            raise ProviderError("ollama", str(exc))

        message = data.get("message", {})
        return ProviderResponse(
            text=message.get("content", ""),
            model=data.get("model", model),
            provider="ollama",
            usage={
                "prompt_tokens": data.get("prompt_eval_count", 0),
                "completion_tokens": data.get("eval_count", 0),
            },
        )
