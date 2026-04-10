"""Provider configuration dataclasses."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class OllamaConfig:
    """Configuration for the Ollama provider."""

    enabled: bool = False
    base_url: str = "http://localhost:11434"
    default_model: str = "llama3.2"
    timeout: int = 120  # seconds


@dataclass
class LMStudioConfig:
    """Configuration for the LM Studio provider."""

    enabled: bool = False
    base_url: str = "http://localhost:1234"
    default_model: str = ""  # LM Studio uses whatever model is loaded
    timeout: int = 120


@dataclass
class GitHubCopilotConfig:
    """Configuration for the GitHub Copilot provider."""

    enabled: bool = False
    api_token: str = ""
    base_url: str = "https://api.githubcopilot.com"
    default_model: str = "gpt-4o"
    timeout: int = 120
    max_retries: int = 5
    retry_delay: float = 2.0  # base seconds between retries (exponential backoff)
    request_delay: float = 1.0  # seconds to wait between every request (throttle)


@dataclass
class ProviderConfig:
    """Top-level provider configuration."""

    preferred_provider: str = ""  # e.g. "ollama", "lm_studio"; empty = use registration order
    ollama: OllamaConfig = field(default_factory=OllamaConfig)
    lm_studio: LMStudioConfig = field(default_factory=LMStudioConfig)
    github_copilot: GitHubCopilotConfig = field(default_factory=GitHubCopilotConfig)
