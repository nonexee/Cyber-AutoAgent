#!/usr/bin/env python3
"""
Cyber-AutoAgent - Simple CLI for Autonomous Security Assessment

Minimal implementation using Claude via Anthropic API.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.modules.agent import create_agent, AgentConfig
from src.modules.config import SimpleConfig

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Cyber-AutoAgent - Autonomous Security Assessment Tool",
        epilog="Use only on authorized targets"
    )
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="Target system to assess (ensure you have permission!)"
    )
    parser.add_argument(
        "--objective",
        type=str,
        required=True,
        help="Security assessment objective"
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=50,
        help="Maximum number of tool executions (default: 50)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-5-sonnet-20241022",
        help="Claude model to use (default: claude-3-5-sonnet-20241022)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Set verbose logging if requested
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Check for API key
    api_key = args.api_key or os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable or use --api-key")
        sys.exit(1)

    os.environ["ANTHROPIC_API_KEY"] = api_key

    # Create output directory
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    logger.info("=" * 80)
    logger.info("CYBER-AUTOAGENT - SIMPLE CLI")
    logger.info("=" * 80)
    logger.info(f"Target: {args.target}")
    logger.info(f"Objective: {args.objective}")
    logger.info(f"Model: {args.model}")
    logger.info(f"Max iterations: {args.max_iterations}")
    logger.info("=" * 80)

    # Create configuration
    config = SimpleConfig(
        model=args.model,
        api_key=api_key,
        max_tokens=4096,
        temperature=0.7
    )

    # Create agent configuration
    agent_config = AgentConfig(
        target=args.target,
        objective=args.objective,
        max_steps=args.max_iterations,
        config=config
    )

    try:
        # Create and run agent
        logger.info("Creating agent...")
        agent = create_agent(agent_config)

        logger.info("Starting assessment...")
        initial_prompt = f"Begin security assessment of {args.target} with objective: {args.objective}"

        result = agent(initial_prompt)

        logger.info("=" * 80)
        logger.info("ASSESSMENT COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Output saved to: {output_dir}")

    except KeyboardInterrupt:
        logger.warning("\nAssessment interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Assessment failed: {e}", exc_info=args.verbose)
        sys.exit(1)


if __name__ == "__main__":
    main()
