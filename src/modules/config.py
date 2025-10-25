"""Simple configuration for OpenAI API with optimization support."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SimpleConfig:
    """Simple configuration for OpenAI models with caching and optimizations."""

    model: str = "gpt-4o"
    api_key: str = ""
    max_tokens: int = 4096
    temperature: float = 0.7

    # Optimization features
    enable_caching: bool = True  # Enable prompt caching for system messages
    enable_streaming: bool = True  # Stream responses for better UX
    parallel_tool_calls: bool = True  # Allow parallel tool execution

    # Advanced options
    top_p: Optional[float] = None  # Nucleus sampling parameter
    frequency_penalty: Optional[float] = None  # Reduce repetition
    presence_penalty: Optional[float] = None  # Encourage topic diversity

    # Context management
    max_context_tokens: Optional[int] = None  # Limit context window usage

    def __post_init__(self):
        """Validate configuration."""
        if not self.api_key:
            raise ValueError("API key is required")
        if not self.model:
            raise ValueError("Model is required")

        # Set reasonable defaults for penalties if not specified
        if self.frequency_penalty is None:
            self.frequency_penalty = 0.0
        if self.presence_penalty is None:
            self.presence_penalty = 0.0

    def get_model_params(self) -> dict:
        """Get model parameters for API calls.

        Returns:
            Dictionary of model parameters
        """
        params = {
            "model": self.model,
            "api_key": self.api_key,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }

        # Add optional parameters if set
        if self.top_p is not None:
            params["top_p"] = self.top_p
        if self.frequency_penalty is not None and self.frequency_penalty != 0.0:
            params["frequency_penalty"] = self.frequency_penalty
        if self.presence_penalty is not None and self.presence_penalty != 0.0:
            params["presence_penalty"] = self.presence_penalty

        return params
