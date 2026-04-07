"""Shared HTTP client with connection pooling."""

from __future__ import annotations

import httpx

_client: httpx.Client | None = None


def get_http_client(timeout: float = 30.0) -> httpx.Client:
    """Get or create a shared httpx Client with connection pooling.

    Reuses connections across requests for better performance.
    """
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            limits=httpx.Limits(
                max_connections=20,
                max_keepalive_connections=10,
                keepalive_expiry=30,
            ),
            headers={"User-Agent": "BigBrain/1.0"},
        )
    return _client


def close_http_client() -> None:
    """Close the shared HTTP client."""
    global _client
    if _client is not None and not _client.is_closed:
        _client.close()
    _client = None
