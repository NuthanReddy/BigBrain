"""GitHub OAuth device flow authentication for the Copilot provider.

Implements the GitHub device authorization flow:
1. Request device code from GitHub
2. User visits github.com/login/device and enters the code
3. App polls for access token
4. Token is cached locally for reuse

Tokens are stored in ~/.bigbrain/github_token.json
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import httpx

from bigbrain.logging_config import get_logger

logger = get_logger(__name__)

# GitHub OAuth app client ID for Copilot integrations
# This is a public client ID — no secret needed for device flow
_GITHUB_DEVICE_CLIENT_ID = "Iv1.b507a08c87ecfe98"  # VS Code's Copilot client ID

_TOKEN_CACHE_PATH = Path.home() / ".bigbrain" / "github_token.json"
_DEVICE_CODE_URL = "https://github.com/login/device/code"
_TOKEN_URL = "https://github.com/login/oauth/access_token"


class AuthError(Exception):
    """Raised when GitHub authentication fails."""


def resolve_github_token(config_token: str = "") -> str:
    """Resolve the GitHub Copilot token.

    Priority:
    1. Explicit config token (if set)
    2. GITHUB_TOKEN env var (if it looks like an OAuth token gho_/ghu_)
    3. Cached token from previous device flow login
    4. Empty string (caller should trigger device flow)
    """
    # 1. Config value
    if config_token:
        return config_token

    # 2. Environment variable
    env_token = os.environ.get("GITHUB_TOKEN", "")
    if env_token and not env_token.startswith("ghp_"):
        # Accept OAuth tokens (gho_, ghu_, github_pat_) but not classic PATs
        logger.debug("Using GITHUB_TOKEN from environment")
        return env_token

    # 3. Cached token
    cached = _load_cached_token()
    if cached:
        logger.debug("Using cached GitHub token from %s", _TOKEN_CACHE_PATH)
        return cached

    return ""


def validate_token(token: str) -> bool:
    """Check if a token is present and not a classic PAT."""
    if not token or not token.strip():
        return False
    if token.startswith("ghp_"):
        logger.warning(
            "Classic PATs (ghp_*) are not supported for Copilot. "
            "Run 'bigbrain auth login' to authenticate."
        )
        return False
    return len(token) >= 10


def device_flow_login(client_id: str = "") -> str:
    """Run the GitHub OAuth device flow interactively.

    Prints instructions for the user, polls for the token,
    caches it, and returns it.

    Args:
        client_id: OAuth app client ID (defaults to the built-in one)

    Returns:
        The access token string

    Raises:
        AuthError: If the flow fails or is cancelled
    """
    client_id = client_id or _GITHUB_DEVICE_CLIENT_ID

    # Step 1: Request device code
    try:
        resp = httpx.post(
            _DEVICE_CODE_URL,
            data={
                "client_id": client_id,
                "scope": "copilot",
            },
            headers={"Accept": "application/json"},
            timeout=15.0,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        raise AuthError(f"Failed to start device flow: {exc}")

    device_code = data["device_code"]
    user_code = data["user_code"]
    verification_uri = data.get("verification_uri", "https://github.com/login/device")
    interval = data.get("interval", 5)
    expires_in = data.get("expires_in", 900)

    # Step 2: Prompt user
    print()
    print("=" * 50)
    print("  GitHub Copilot Authentication")
    print("=" * 50)
    print()
    print(f"  1. Open: {verification_uri}")
    print(f"  2. Enter code: {user_code}")
    print()
    print("  Waiting for authorization...", end="", flush=True)

    # Step 3: Poll for token
    deadline = time.time() + expires_in
    while time.time() < deadline:
        time.sleep(interval)
        try:
            token_resp = httpx.post(
                _TOKEN_URL,
                data={
                    "client_id": client_id,
                    "device_code": device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                },
                headers={"Accept": "application/json"},
                timeout=15.0,
            )
            token_data = token_resp.json()
        except Exception:
            print(".", end="", flush=True)
            continue

        error = token_data.get("error")
        if error == "authorization_pending":
            print(".", end="", flush=True)
            continue
        elif error == "slow_down":
            interval = token_data.get("interval", interval + 5)
            print(".", end="", flush=True)
            continue
        elif error == "expired_token":
            print()
            raise AuthError("Device code expired. Please try again.")
        elif error == "access_denied":
            print()
            raise AuthError("Authorization denied by user.")
        elif error:
            print()
            raise AuthError(
                f"OAuth error: {error} — {token_data.get('error_description', '')}"
            )

        # Success!
        access_token = token_data.get("access_token", "")
        if access_token:
            print(" done!")
            print()
            _cache_token(access_token)
            logger.info("GitHub Copilot authenticated successfully")
            return access_token

    print()
    raise AuthError("Authentication timed out. Please try again.")


def _load_cached_token() -> str:
    """Load cached token from disk."""
    try:
        if _TOKEN_CACHE_PATH.exists():
            data = json.loads(_TOKEN_CACHE_PATH.read_text(encoding="utf-8"))
            return data.get("access_token", "")
    except Exception:
        pass
    return ""


def _cache_token(token: str) -> None:
    """Save token to disk cache."""
    try:
        _TOKEN_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        _TOKEN_CACHE_PATH.write_text(
            json.dumps({"access_token": token}),
            encoding="utf-8",
        )
        # Restrict file permissions on Unix
        if sys.platform != "win32":
            _TOKEN_CACHE_PATH.chmod(0o600)
        logger.debug("Cached GitHub token to %s", _TOKEN_CACHE_PATH)
    except Exception as exc:
        logger.warning("Failed to cache GitHub token: %s", exc)


def clear_cached_token() -> bool:
    """Remove cached token. Returns True if a token was removed."""
    try:
        if _TOKEN_CACHE_PATH.exists():
            _TOKEN_CACHE_PATH.unlink()
            return True
    except Exception:
        pass
    return False
