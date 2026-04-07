"""GitHub authentication helpers for the Copilot provider."""

from __future__ import annotations

import os

from bigbrain.logging_config import get_logger

logger = get_logger(__name__)


def resolve_github_token(config_token: str = "") -> str:
    """Resolve the GitHub token from config or environment.

    Priority: config value → GITHUB_TOKEN env var → empty string
    """
    if config_token:
        return config_token
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        logger.debug("Using GITHUB_TOKEN from environment")
    return token


def validate_token(token: str) -> bool:
    """Validate that a token is non-empty and has reasonable format.

    Does NOT make a network call — just basic format validation.
    Tokens are typically 'ghp_*', 'gho_*', 'github_pat_*', or 'ghu_*'.
    """
    if not token or not token.strip():
        return False
    # Accept any non-empty token (don't be overly strict on format)
    return len(token) >= 10


class AuthError(Exception):
    """Raised when GitHub authentication fails."""
