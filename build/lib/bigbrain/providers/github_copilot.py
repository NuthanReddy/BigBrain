"""GitHub Copilot provider – cloud LLM via GitHub's Copilot API.

Uses the GitHub Copilot chat completions API with token-based authentication.
Supports retry logic and rate limit handling.
"""

from __future__ import annotations

import time
from typing import Any

import httpx

from bigbrain.errors import ProviderError
from bigbrain.logging_config import get_logger
from bigbrain.providers.base import BaseProvider, ProviderResponse
from bigbrain.providers.config import GitHubCopilotConfig
from bigbrain.providers.github_auth import resolve_github_token, validate_token

logger = get_logger(__name__)


class GitHubCopilotProvider(BaseProvider):
    """GitHub Copilot provider with token auth and retry logic."""

    def __init__(self, config: GitHubCopilotConfig) -> None:
        self._config = config
        self._base_url = config.base_url.rstrip("/")
        self._timeout = config.timeout
        self._max_retries = config.max_retries
        self._retry_delay = config.retry_delay
        self._token = resolve_github_token(config.api_token)

    @property
    def name(self) -> str:
        return "github_copilot"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def is_available(self) -> bool:
        """Check if token is valid and API is reachable."""
        if not validate_token(self._token):
            logger.debug("GitHub Copilot: no valid token configured")
            return False
        try:
            resp = httpx.get(
                f"{self._base_url}/models",
                headers=self._headers(),
                timeout=10.0,
            )
            return resp.status_code in (200, 401)  # 401 = reachable but bad token
        except (httpx.ConnectError, httpx.TimeoutException, OSError):
            return False

    def list_models(self) -> list[str]:
        """List available models from the API."""
        if not validate_token(self._token):
            return []
        try:
            resp = httpx.get(
                f"{self._base_url}/models",
                headers=self._headers(),
                timeout=10.0,
            )
            resp.raise_for_status()
            data = resp.json()
            return [m["id"] for m in data.get("data", [])]
        except Exception as exc:
            logger.warning("Failed to list GitHub Copilot models: %s", exc)
            return []

    def complete(
        self, prompt: str, *, model: str = "", **kwargs: Any
    ) -> ProviderResponse:
        """Text completion via chat completions endpoint (prompt as user message)."""
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, model=model, **kwargs)

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str = "",
        **kwargs: Any,
    ) -> ProviderResponse:
        """Chat completion with retry logic and rate limit handling."""
        if not validate_token(self._token):
            raise ProviderError(
                "github_copilot",
                "No valid API token configured. "
                "Set GITHUB_TOKEN env var or providers.github_copilot.api_token in config.",
            )

        model = model or self._config.default_model

        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
        }
        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]

        last_exc: Exception | None = None
        for attempt in range(1, self._max_retries + 1):
            try:
                resp = httpx.post(
                    f"{self._base_url}/chat/completions",
                    json=payload,
                    headers=self._headers(),
                    timeout=self._timeout,
                )

                # Rate limit handling
                if resp.status_code == 429:
                    retry_after = float(
                        resp.headers.get("Retry-After", self._retry_delay)
                    )
                    logger.warning(
                        "GitHub Copilot rate limited, retry after %.1fs (attempt %d/%d)",
                        retry_after,
                        attempt,
                        self._max_retries,
                    )
                    if attempt < self._max_retries:
                        time.sleep(retry_after)
                        continue
                    raise ProviderError(
                        "github_copilot", "Rate limited after all retries"
                    )

                resp.raise_for_status()
                data = resp.json()

                choices = data.get("choices", [])
                text = ""
                if choices:
                    msg = choices[0].get("message", {})
                    text = msg.get("content", "")

                usage = data.get("usage", {})
                return ProviderResponse(
                    text=text,
                    model=data.get("model", model),
                    provider="github_copilot",
                    usage={
                        "prompt_tokens": usage.get("prompt_tokens", 0),
                        "completion_tokens": usage.get("completion_tokens", 0),
                    },
                )

            except httpx.TimeoutException:
                last_exc = ProviderError(
                    "github_copilot",
                    f"Request timed out after {self._timeout}s "
                    f"(attempt {attempt}/{self._max_retries})",
                )
                if attempt < self._max_retries:
                    logger.warning(
                        "GitHub Copilot timeout, retrying (attempt %d/%d)",
                        attempt,
                        self._max_retries,
                    )
                    time.sleep(self._retry_delay)
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 401:
                    raise ProviderError(
                        "github_copilot",
                        "Authentication failed. Check your GITHUB_TOKEN.",
                    )
                last_exc = ProviderError(
                    "github_copilot",
                    f"HTTP {exc.response.status_code}: {exc.response.text[:200]}",
                )
                if attempt < self._max_retries:
                    time.sleep(self._retry_delay)
            except httpx.ConnectError:
                raise ProviderError(
                    "github_copilot", f"Cannot connect to {self._base_url}"
                )
            except ProviderError:
                raise
            except Exception as exc:
                last_exc = ProviderError("github_copilot", str(exc))
                if attempt < self._max_retries:
                    time.sleep(self._retry_delay)

        raise last_exc or ProviderError("github_copilot", "All retries exhausted")
