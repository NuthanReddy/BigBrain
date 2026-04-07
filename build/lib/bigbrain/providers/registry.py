"""Provider registry – loads enabled providers and manages fallback."""

from __future__ import annotations

from typing import Any

from bigbrain.errors import NoProviderAvailableError, ProviderError
from bigbrain.logging_config import get_logger
from bigbrain.providers.base import BaseProvider, ProviderResponse
from bigbrain.providers.config import ProviderConfig

logger = get_logger(__name__)


class ProviderRegistry:
    """Registry that manages AI providers with automatic fallback.

    Providers are tried in order of registration. If one fails or is
    unavailable, the next is tried. Raises NoProviderAvailableError
    if all fail.

    Usage::

        registry = ProviderRegistry.from_config(config.providers)
        response = registry.complete("Summarize this text...")

    Or::

        registry = ProviderRegistry.from_app_config()
        if registry.has_providers():
            response = registry.complete("...")
    """

    def __init__(self, preferred: str = "") -> None:
        self._providers: list[BaseProvider] = []
        self._preferred = preferred

    @classmethod
    def from_config(cls, config: ProviderConfig) -> ProviderRegistry:
        """Create registry from ProviderConfig, loading only enabled providers."""
        registry = cls(preferred=config.preferred_provider)

        # Register Ollama if enabled
        if config.ollama.enabled:
            from bigbrain.providers.ollama import OllamaProvider

            registry.register(OllamaProvider(config.ollama))
            logger.debug("Registered Ollama provider")

        # Register LM Studio if enabled
        if config.lm_studio.enabled:
            from bigbrain.providers.lm_studio import LMStudioProvider

            registry.register(LMStudioProvider(config.lm_studio))
            logger.debug("Registered LM Studio provider")

        # Register GitHub Copilot if enabled
        if config.github_copilot.enabled:
            from bigbrain.providers.github_copilot import GitHubCopilotProvider

            registry.register(GitHubCopilotProvider(config.github_copilot))
            logger.debug("Registered GitHub Copilot provider")

        return registry

    @classmethod
    def from_app_config(cls) -> ProviderRegistry:
        """Create registry from the application config (loads config automatically)."""
        from bigbrain.config import load_config

        cfg = load_config()
        return cls.from_config(cfg.providers)

    def register(self, provider: BaseProvider) -> None:
        """Add a provider to the registry."""
        self._providers.append(provider)

    def has_providers(self) -> bool:
        """Return True if at least one provider is registered."""
        return len(self._providers) > 0

    def list_providers(self) -> list[str]:
        """Return names of all registered providers."""
        return [p.name for p in self._providers]

    def get_available_providers(self) -> list[BaseProvider]:
        """Return providers that pass is_available() check."""
        available = []
        for p in self._providers:
            try:
                if p.is_available():
                    available.append(p)
                else:
                    logger.debug("Provider %s is not available", p.name)
            except Exception as exc:
                logger.debug(
                    "Provider %s availability check failed: %s", p.name, exc
                )
        return available

    def get_provider(self) -> BaseProvider:
        """Return the first available provider.

        If a preferred provider is configured, it is tried first.
        Raises NoProviderAvailableError if none are available.
        """
        if not self._providers:
            raise NoProviderAvailableError(tried=[])

        # Try preferred provider first
        if self._preferred:
            for p in self._providers:
                if p.name == self._preferred:
                    try:
                        if p.is_available():
                            return p
                        logger.warning(
                            "Preferred provider '%s' is not available, falling back",
                            self._preferred,
                        )
                    except Exception:
                        logger.warning(
                            "Preferred provider '%s' check failed, falling back",
                            self._preferred,
                        )
                    break

        # Fallback to registration order
        for p in self._providers:
            try:
                if p.is_available():
                    return p
            except Exception:
                continue

        raise NoProviderAvailableError(tried=self.list_providers())

    def health_check(self) -> dict[str, bool]:
        """Check availability of all registered providers.

        Returns dict of provider_name → is_available.
        """
        results = {}
        for p in self._providers:
            try:
                results[p.name] = p.is_available()
            except Exception:
                results[p.name] = False
        return results

    # ------------------------------------------------------------------
    # Fallback-enabled operations
    # ------------------------------------------------------------------

    def complete(
        self, prompt: str, *, model: str = "", **kwargs: Any
    ) -> ProviderResponse:
        """Complete with fallback across providers.

        Tries each registered provider in order. If one fails, tries the next.
        Raises NoProviderAvailableError if all fail.
        """
        return self._with_fallback("complete", prompt=prompt, model=model, **kwargs)

    def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str = "",
        **kwargs: Any,
    ) -> ProviderResponse:
        """Chat with fallback across providers."""
        return self._with_fallback("chat", messages=messages, model=model, **kwargs)

    def summarize(
        self, text: str, *, model: str = "", max_length: int = 500
    ) -> ProviderResponse:
        """Summarize with fallback across providers."""
        return self._with_fallback(
            "summarize", text=text, model=model, max_length=max_length
        )

    def extract_entities(self, text: str, *, model: str = "") -> ProviderResponse:
        """Extract entities with fallback across providers."""
        return self._with_fallback("extract_entities", text=text, model=model)

    @property
    def preferred(self) -> str:
        """Return the preferred provider name, or empty string."""
        return self._preferred

    def _with_fallback(self, method_name: str, **kwargs: Any) -> ProviderResponse:
        """Try calling method_name on each provider in order.

        If a preferred provider is configured, it is tried first.
        On ProviderError, log warning and try next provider.
        On success, return the response.
        If all fail, raise NoProviderAvailableError.
        """
        if not self._providers:
            raise NoProviderAvailableError(tried=[])

        # Build ordered provider list: preferred first, then rest
        ordered = list(self._providers)
        if self._preferred:
            preferred = [p for p in ordered if p.name == self._preferred]
            others = [p for p in ordered if p.name != self._preferred]
            ordered = preferred + others

        errors: list[str] = []
        for provider in ordered:
            try:
                method = getattr(provider, method_name)
                return method(**kwargs)
            except ProviderError as exc:
                logger.warning("Provider %s failed: %s", provider.name, exc)
                errors.append(f"{provider.name}: {exc}")
            except Exception as exc:
                logger.warning(
                    "Provider %s unexpected error: %s", provider.name, exc
                )
                errors.append(f"{provider.name}: {exc}")

        raise NoProviderAvailableError(tried=self.list_providers())
