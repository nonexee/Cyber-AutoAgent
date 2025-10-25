"""Simple FAISS-based memory system."""

import logging
import os
from pathlib import Path
from typing import Any, Dict

from mem0 import Memory
from strands.tool import Tool

logger = logging.getLogger(__name__)


def initialize_memory(target: str) -> Memory:
    """Initialize FAISS-based memory for a target.

    Args:
        target: Target identifier

    Returns:
        Memory client instance
    """
    # Create memory directory
    memory_dir = Path("outputs") / target.replace(":", "_").replace("/", "_") / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Initializing memory at: {memory_dir}")

    # Simple FAISS configuration
    config = {
        "vector_store": {
            "provider": "faiss",
            "config": {
                "path": str(memory_dir),
                "embedding_model_dims": 1024
            }
        }
    }

    # Create memory client
    memory = Memory.from_config(config)
    logger.info("Memory initialized successfully")

    return memory


def mem0_memory(memory_client: Memory) -> Tool:
    """Create a memory tool for storing findings.

    Args:
        memory_client: Initialized Memory instance

    Returns:
        Memory storage tool
    """

    def store_finding(content: str, category: str = "finding") -> str:
        """Store a security finding in memory.

        Args:
            content: Finding content to store
            category: Category of the finding (default: "finding")

        Returns:
            Confirmation message
        """
        try:
            metadata = {"category": category, "type": "security_finding"}
            memory_client.add(content, metadata=metadata)
            logger.info(f"Stored finding: {content[:100]}...")
            return f"Successfully stored finding in memory (category: {category})"
        except Exception as e:
            logger.error(f"Failed to store finding: {e}")
            return f"Failed to store finding: {e}"

    return Tool(
        function=store_finding,
        name="memory",
        description="Store important security findings and evidence in persistent memory. "
                    "Use this to save discovered vulnerabilities, credentials, or other critical information."
    )
