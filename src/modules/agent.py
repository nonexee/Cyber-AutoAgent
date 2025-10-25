"""Simplified agent creation using OpenAI API."""

import logging
import os
from dataclasses import dataclass
from typing import Optional

from strands import Agent
from strands.models.openai import OpenAIModel

# Tools are part of strands.tools, not separate package
try:
    from strands.tools.shell import shell
    from strands.tools.editor import editor
    from strands.tools.stop import stop
except ImportError:
    # Fallback for older versions
    from strands_tools.shell import shell
    from strands_tools.editor import editor
    from strands_tools.stop import stop

from .config import SimpleConfig
from .memory import initialize_memory, mem0_memory
from .prompts import get_system_prompt

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration for agent creation."""

    target: str
    objective: str
    max_steps: int = 50
    config: Optional[SimpleConfig] = None
    module: str = "general"


def create_agent(agent_config: AgentConfig) -> Agent:
    """Create a simple agent using OpenAI API.

    Args:
        agent_config: Agent configuration

    Returns:
        Configured Agent instance
    """
    config = agent_config.config
    if not config:
        raise ValueError("SimpleConfig is required")

    logger.info(f"Creating agent with model: {config.model}")

    # Log optimization settings
    if config.enable_caching:
        logger.info("Prompt caching enabled - system messages will be cached")
    if config.enable_streaming:
        logger.info("Response streaming enabled")
    if config.parallel_tool_calls:
        logger.info("Parallel tool execution enabled")

    # Create OpenAI model with all parameters
    model_params = config.get_model_params()

    # Add streaming support if enabled
    if config.enable_streaming:
        model_params["stream"] = True

    model = OpenAIModel(**model_params)

    # Initialize memory system
    memory_client = initialize_memory(agent_config.target)

    # Create memory tool
    memory_tool = mem0_memory(memory_client)

    # Core tools for security assessment
    tools = [
        shell,          # Execute shell commands
        editor,         # Create/edit files
        memory_tool,    # Store findings
        stop,           # Stop when objective is met
    ]

    # Get system prompt (with module support)
    system_prompt = get_system_prompt(
        target=agent_config.target,
        objective=agent_config.objective,
        max_steps=agent_config.max_steps,
        module=agent_config.module
    )

    # Prepare system message with caching hint if enabled
    # OpenAI caches system messages automatically for repeated use
    if config.enable_caching:
        # For OpenAI, we can add a caching instruction in the system prompt
        # This helps OpenAI's caching system identify stable content
        system_prompt_with_cache_info = f"""{system_prompt}

---
[This system message is designed to be cached for optimal performance]
"""
        final_system_prompt = system_prompt_with_cache_info
    else:
        final_system_prompt = system_prompt

    # Create agent with optimizations
    agent_kwargs = {
        "model": model,
        "tools": tools,
        "system": final_system_prompt,
        "max_iterations": agent_config.max_steps,
    }

    # Enable parallel tool calls if configured
    if config.parallel_tool_calls:
        agent_kwargs["parallel_tool_calls"] = True

    agent = Agent(**agent_kwargs)

    logger.info("Agent created successfully")
    return agent
