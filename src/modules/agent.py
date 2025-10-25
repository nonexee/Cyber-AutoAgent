"""Simplified agent creation using Anthropic API."""

import logging
import os
from dataclasses import dataclass
from typing import Optional

from strands import Agent
from strands.models.anthropic import AnthropicModel
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
    """Create a simple agent using Anthropic API.

    Args:
        agent_config: Agent configuration

    Returns:
        Configured Agent instance
    """
    config = agent_config.config
    if not config:
        raise ValueError("SimpleConfig is required")

    logger.info(f"Creating agent with model: {config.model}")

    # Create Anthropic model
    model = AnthropicModel(
        model=config.model,
        api_key=config.api_key,
        max_tokens=config.max_tokens,
        temperature=config.temperature
    )

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

    # Create agent
    agent = Agent(
        model=model,
        tools=tools,
        system=system_prompt,
        max_iterations=agent_config.max_steps
    )

    logger.info("Agent created successfully")
    return agent
