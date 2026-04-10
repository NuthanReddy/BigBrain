"""GitHub Copilot provider – cloud LLM via GitHub's Copilot API.

Uses the GitHub Copilot chat completions API with token-based authentication.
Features adaptive rate limiting that reads X-RateLimit-* headers from every
response and auto-tunes request pacing to stay within the API's limits.
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
    """GitHub Copilot provider with adaptive rate limiting.

    Reads ``X-RateLimit-Remaining``, ``X-RateLimit-Reset``, and
    ``Retry-After`` headers from every API response.  When remaining
    requests drop below a threshold the provider automatically slows
    down; when the window resets it speeds back up.
    """

    def __init__(self, config: GitHubCopilotConfig) -> None:
        self._config = config
        self._base_url = config.base_url.rstrip("/")
        self._timeout = config.timeout
        self._max_retries = config.max_retries
        self._retry_delay = config.retry_delay
        self._request_delay = config.request_delay
        self._token = resolve_github_token(config.api_token)

        # Adaptive rate-limit state (updated from response headers)
        self._rate_limit: int = 0          # total allowed per window
        self._rate_remaining: int = -1     # requests left in window (-1 = unknown)
        self._rate_reset: float = 0.0      # unix timestamp when window resets

        # Self-tracking: timestamps of recent requests (sliding 60s window)
        self._request_timestamps: list[float] = []
        self._total_requests: int = 0
        self._total_errors: int = 0

    @property
    def name(self) -> str:
        return "github_copilot"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _update_rate_limits(self, headers: httpx.Headers) -> None:
        """Parse rate-limit headers and update internal state.

        GitHub Copilot API does not currently return X-RateLimit-* headers.
        Instead we track request counts and timing ourselves.
        """
        # Check for standard headers (in case GitHub adds them later)
        try:
            if "x-ratelimit-limit" in headers:
                self._rate_limit = int(headers["x-ratelimit-limit"])
            if "x-ratelimit-remaining" in headers:
                self._rate_remaining = int(headers["x-ratelimit-remaining"])
            if "x-ratelimit-reset" in headers:
                self._rate_reset = float(headers["x-ratelimit-reset"])
        except (ValueError, TypeError):
            pass

        # Self-tracking: count requests in a sliding 60-second window
        now = time.time()
        self._request_timestamps.append(now)
        # Prune timestamps older than 60s
        cutoff = now - 60.0
        self._request_timestamps = [t for t in self._request_timestamps if t > cutoff]

    def _adaptive_delay(self) -> float:
        """Compute how long to wait before the next request.

        If API provides rate-limit headers, use those.  Otherwise use
        self-tracked request counts in a 60-second sliding window to
        stay under an estimated ~10 requests/minute safe rate.
        """
        # If API headers are available, use them
        if self._rate_remaining >= 0 and self._rate_limit > 0:
            pct = self._rate_remaining / self._rate_limit
            if pct > 0.5:
                return self._request_delay
            elif pct > 0.2:
                return self._request_delay * 2
            elif self._rate_remaining > 0:
                time_left = max(self._rate_reset - time.time(), 1.0)
                return min(time_left / self._rate_remaining, 30.0)
            else:
                wait = max(self._rate_reset - time.time(), 10.0)
                logger.warning("Rate limit exhausted, waiting %.1fs until reset", wait)
                return min(wait, 120.0)

        # Self-tracking: if we've had recent 403/429 errors, slow down
        reqs_last_minute = len(self._request_timestamps)
        if reqs_last_minute >= 10:
            # We're sending a lot — slow down to ~6/min
            return max(self._request_delay * 3, 10.0)
        elif reqs_last_minute >= 5:
            return max(self._request_delay * 2, 5.0)

        return self._request_delay

    def rate_limit_info(self) -> dict[str, Any]:
        """Return current rate-limit state (for diagnostics)."""
        now = time.time()
        cutoff = now - 60.0
        recent = [t for t in self._request_timestamps if t > cutoff]
        return {
            "limit": self._rate_limit,
            "remaining": self._rate_remaining,
            "reset": self._rate_reset,
            "reset_in": max(self._rate_reset - now, 0),
            "requests_last_60s": len(recent),
            "total_requests": self._total_requests,
            "total_errors": self._total_errors,
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
            return resp.status_code in (200, 401)
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
        """Chat completion with adaptive rate limiting and retry logic."""
        if not validate_token(self._token):
            raise ProviderError(
                "github_copilot",
                "No valid Copilot token. Run 'bigbrain auth login' to authenticate via GitHub.",
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
                # Pre-request adaptive delay based on rate-limit state
                if attempt == 1:
                    delay = self._adaptive_delay()
                    if delay > 0:
                        time.sleep(delay)

                resp = httpx.post(
                    f"{self._base_url}/chat/completions",
                    json=payload,
                    headers=self._headers(),
                    timeout=self._timeout,
                )

                # Always update rate-limit state from headers
                self._update_rate_limits(resp.headers)

                # Handle 400 errors
                if resp.status_code == 400:
                    body = resp.text[:500]
                    if "Personal Access Token" in body:
                        raise ProviderError(
                            "github_copilot",
                            "Classic PATs are not supported. "
                            "Run 'bigbrain auth login' to authenticate via GitHub device flow.",
                        )
                    logger.warning(
                        "GitHub Copilot 400 (attempt %d/%d): %s",
                        attempt, self._max_retries, body,
                    )
                    last_exc = ProviderError("github_copilot", f"Bad request: {body}")
                    if attempt < self._max_retries:
                        delay = self._retry_delay * (2 ** (attempt - 1))
                        time.sleep(min(delay, 120))
                        continue
                    raise last_exc

                # Rate limit handling (429 or 403 quota exceeded)
                if resp.status_code in (429, 403):
                    self._total_errors += 1
                    # Prefer Retry-After header, fall back to reset timestamp
                    if "Retry-After" in resp.headers:
                        retry_after = float(resp.headers["Retry-After"])
                    elif self._rate_reset > 0:
                        retry_after = max(self._rate_reset - time.time(), 10.0)
                    else:
                        retry_after = self._retry_delay * (2 ** (attempt - 1))
                    retry_after = max(retry_after, 10)
                    retry_after = min(retry_after, 120)

                    remaining_info = ""
                    if self._rate_remaining >= 0:
                        remaining_info = f" (remaining: {self._rate_remaining}/{self._rate_limit})"

                    logger.warning(
                        "GitHub Copilot %d (attempt %d/%d), retry after %.1fs%s",
                        resp.status_code, attempt, self._max_retries,
                        retry_after, remaining_info,
                    )
                    last_exc = ProviderError(
                        "github_copilot",
                        f"Rate limited ({resp.status_code}) after {self._max_retries} retries",
                    )
                    if attempt < self._max_retries:
                        time.sleep(retry_after)
                        continue
                    raise last_exc

                resp.raise_for_status()
                data = resp.json()
                self._total_requests += 1

                choices = data.get("choices", [])
                text = ""
                if choices:
                    msg = choices[0].get("message", {})
                    text = msg.get("content", "")

                usage = data.get("usage", {})

                # Log rate-limit state periodically
                reqs_last_min = len(self._request_timestamps)
                if self._total_requests % 5 == 0:
                    logger.debug(
                        "Copilot: %d reqs total, %d in last 60s, delay=%.1fs",
                        self._total_requests, reqs_last_min,
                        self._adaptive_delay(),
                    )

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
