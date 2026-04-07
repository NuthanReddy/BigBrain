"""Retry helpers with configurable backoff for AI and network operations."""

from __future__ import annotations

import functools
from typing import Any, Callable, TypeVar

from bigbrain.errors import ProviderError
from bigbrain.logging_config import get_logger

logger = get_logger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def with_retry(
    max_attempts: int = 3,
    retry_on: tuple[type[Exception], ...] = (ProviderError,),
    backoff_base: float = 2.0,
    max_delay: float = 30.0,
) -> Callable[[F], F]:
    """Decorator for retrying functions with exponential backoff.

    Usage::
        @with_retry(max_attempts=3, retry_on=(ProviderError,))
        def call_ai(prompt):
            return registry.complete(prompt)
    """
    try:
        from tenacity import (
            before_sleep_log,
            retry,
            retry_if_exception_type,
            stop_after_attempt,
            wait_exponential,
        )
        import logging

        def decorator(func: F) -> F:
            @retry(
                stop=stop_after_attempt(max_attempts),
                wait=wait_exponential(multiplier=backoff_base, max=max_delay),
                retry=retry_if_exception_type(retry_on),
                before_sleep=before_sleep_log(logger, logging.WARNING),
                reraise=True,
            )
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return func(*args, **kwargs)
            return wrapper  # type: ignore
        return decorator  # type: ignore
    except ImportError:
        # Fallback: simple retry without tenacity
        def decorator(func: F) -> F:  # type: ignore[no-redef]
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                import time
                last_exc = None
                for attempt in range(1, max_attempts + 1):
                    try:
                        return func(*args, **kwargs)
                    except retry_on as exc:
                        last_exc = exc
                        if attempt < max_attempts:
                            delay = min(backoff_base ** attempt, max_delay)
                            logger.warning(
                                "Retry %d/%d after %.1fs: %s",
                                attempt, max_attempts, delay, exc,
                            )
                            time.sleep(delay)
                raise last_exc  # type: ignore
            return wrapper  # type: ignore
        return decorator  # type: ignore


class CircuitBreaker:
    """Simple circuit breaker for repeated failures.

    After ``failure_threshold`` consecutive failures the circuit opens
    and rejects calls for ``recovery_timeout`` seconds.

    Usage::
        breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)
        if breaker.is_open():
            return fallback_result
        try:
            result = make_call()
            breaker.record_success()
        except Exception:
            breaker.record_failure()
    """

    def __init__(
        self, failure_threshold: int = 5, recovery_timeout: float = 60.0
    ) -> None:
        self._threshold = failure_threshold
        self._timeout = recovery_timeout
        self._failures = 0
        self._opened_at: float | None = None

    def is_open(self) -> bool:
        if self._opened_at is None:
            return False
        import time
        if time.time() - self._opened_at > self._timeout:
            # Half-open: allow one attempt
            self._opened_at = None
            self._failures = 0
            return False
        return True

    def record_success(self) -> None:
        self._failures = 0
        self._opened_at = None

    def record_failure(self) -> None:
        self._failures += 1
        if self._failures >= self._threshold:
            import time
            self._opened_at = time.time()
            logger.warning(
                "Circuit breaker opened after %d failures", self._failures
            )

    @property
    def failure_count(self) -> int:
        return self._failures
