"""Simple configuration for OpenAI API."""

from dataclasses import dataclass


@dataclass
class SimpleConfig:
    """Simple configuration for OpenAI models."""

    model: str = "gpt-4o"
    api_key: str = ""
    max_tokens: int = 4096
    temperature: float = 0.7

    def __post_init__(self):
        """Validate configuration."""
        if not self.api_key:
            raise ValueError("API key is required")
        if not self.model:
            raise ValueError("Model is required")
