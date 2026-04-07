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
class ProviderConfig:
    """Top-level provider configuration."""

    ollama: OllamaConfig = field(default_factory=OllamaConfig)
    lm_studio: LMStudioConfig = field(default_factory=LMStudioConfig)
