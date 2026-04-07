"""Base provider ABC and shared types for AI provider integration."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProviderResponse:
    """Response from an AI provider."""

    text: str
    model: str = ""
    provider: str = ""
    usage: dict[str, int] = field(default_factory=dict)  # tokens_in, tokens_out
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseProvider(ABC):
    """Abstract base class for AI providers.

    Each provider must implement these methods. The registry
    will call them with fallback between providers.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name (e.g., 'ollama', 'lm_studio')."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is reachable and ready.

        Should be a quick connectivity check (not a full inference call).
        Return False on connection errors, timeouts, or missing config.
        """
        ...

    @abstractmethod
    def complete(
        self, prompt: str, *, model: str = "", **kwargs: Any
    ) -> ProviderResponse:
        """Send a completion/generation request.

        Parameters:
            prompt: The text prompt to send
            model: Override the default model (provider-specific)
            **kwargs: Provider-specific options (temperature, max_tokens, etc.)

        Returns:
            ProviderResponse with the generated text

        Raises:
            ProviderError: On API errors, timeouts, or invalid responses
        """
        ...

    @abstractmethod
    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str = "",
        **kwargs: Any,
    ) -> ProviderResponse:
        """Send a chat completion request.

        Parameters:
            messages: List of {"role": "system"|"user"|"assistant", "content": "..."}
            model: Override the default model
            **kwargs: Provider-specific options

        Returns:
            ProviderResponse with the assistant's reply

        Raises:
            ProviderError: On API errors, timeouts, or invalid responses
        """
        ...

    def summarize(
        self, text: str, *, model: str = "", max_length: int = 500
    ) -> ProviderResponse:
        """Summarize text using a standard prompt template.

        Default implementation calls complete() with a summarization prompt.
        Providers can override for specialized behavior.
        """
        prompt = (
            f"Summarize the following text concisely in at most {max_length} words. "
            f"Focus on key concepts, definitions, and important details.\n\n"
            f"Text:\n{text}\n\nSummary:"
        )
        return self.complete(prompt, model=model)

    def extract_entities(self, text: str, *, model: str = "") -> ProviderResponse:
        """Extract key entities and concepts from text.

        Default implementation calls complete() with an extraction prompt.
        """
        prompt = (
            "Extract the key entities, concepts, and terms from the following text. "
            "Return them as a JSON array of objects with 'name', 'type', and "
            "'description' fields.\n\n"
            f"Text:\n{text}\n\nEntities (JSON):"
        )
        return self.complete(prompt, model=model)
