"""LM Studio provider – local LLM via OpenAI-compatible API.

LM Studio serves an OpenAI-compatible REST API at the configured base URL.
Default: http://localhost:1234
"""

from __future__ import annotations

from typing import Any

import httpx

from bigbrain.errors import ProviderError
from bigbrain.logging_config import get_logger
from bigbrain.providers.base import BaseProvider, ProviderResponse
from bigbrain.providers.config import LMStudioConfig

logger = get_logger(__name__)


class LMStudioProvider(BaseProvider):
    """LM Studio provider using OpenAI-compatible API."""

    def __init__(self, config: LMStudioConfig) -> None:
        self._config = config
        self._base_url = config.base_url.rstrip("/")
        self._timeout = config.timeout

    @property
    def name(self) -> str:
        return "lm_studio"

    def is_available(self) -> bool:
        """Check if LM Studio is running by listing models."""
        try:
            resp = httpx.get(
                f"{self._base_url}/v1/models",
                timeout=5.0,
            )
            return resp.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException, OSError):
            return False

    def list_models(self) -> list[str]:
        """Return list of available models from LM Studio."""
        try:
            resp = httpx.get(
                f"{self._base_url}/v1/models",
                timeout=10.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return [m["id"] for m in data.get("data", [])]
        except Exception as exc:
            logger.warning("Failed to list LM Studio models: %s", exc)
            return []

    def complete(
        self, prompt: str, *, model: str = "", **kwargs: Any
    ) -> ProviderResponse:
        """Text completion via POST /v1/completions."""
        model = model or self._config.default_model

        payload: dict[str, Any] = {
            "prompt": prompt,
            "stream": False,
        }
        if model:
            payload["model"] = model
        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]

        try:
            resp = httpx.post(
                f"{self._base_url}/v1/completions",
                json=payload,
                timeout=self._timeout,
            )
            resp.raise_for_status()
            data = resp.json()
        except httpx.TimeoutException:
            raise ProviderError(
                "lm_studio", f"Request timed out after {self._timeout}s"
            )
        except httpx.HTTPStatusError as exc:
            raise ProviderError(
                "lm_studio",
                f"HTTP {exc.response.status_code}: {exc.response.text[:200]}",
            )
        except httpx.ConnectError:
            raise ProviderError(
                "lm_studio", f"Cannot connect to {self._base_url}"
            )
        except Exception as exc:
            raise ProviderError("lm_studio", str(exc))

        choices = data.get("choices", [])
        text = choices[0].get("text", "") if choices else ""
        usage = data.get("usage", {})

        return ProviderResponse(
            text=text,
            model=data.get("model", model or ""),
            provider="lm_studio",
            usage={
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
            },
        )

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str = "",
        **kwargs: Any,
    ) -> ProviderResponse:
        """Chat completion via POST /v1/chat/completions."""
        model = model or self._config.default_model

        payload: dict[str, Any] = {
            "messages": messages,
            "stream": False,
        }
        if model:
            payload["model"] = model
        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]

        try:
            resp = httpx.post(
                f"{self._base_url}/v1/chat/completions",
                json=payload,
                timeout=self._timeout,
            )
            resp.raise_for_status()
            data = resp.json()
        except httpx.TimeoutException:
            raise ProviderError(
                "lm_studio", f"Request timed out after {self._timeout}s"
            )
        except httpx.HTTPStatusError as exc:
            raise ProviderError(
                "lm_studio",
                f"HTTP {exc.response.status_code}: {exc.response.text[:200]}",
            )
        except httpx.ConnectError:
            raise ProviderError(
                "lm_studio", f"Cannot connect to {self._base_url}"
            )
        except Exception as exc:
            raise ProviderError("lm_studio", str(exc))

        choices = data.get("choices", [])
        text = ""
        if choices:
            msg = choices[0].get("message", {})
            text = msg.get("content", "")
        usage = data.get("usage", {})

        return ProviderResponse(
            text=text,
            model=data.get("model", model or ""),
            provider="lm_studio",
            usage={
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
            },
        )
