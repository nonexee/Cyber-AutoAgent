#!/usr/bin/env python3
"""
Cyber-AutoAgent - Simple CLI for Autonomous Security Assessment

Minimal implementation using OpenAI models (GPT-4, etc.).
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
from src.modules.plugins import list_available_modules

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
        default="gpt-4o",
        help="OpenAI model to use (default: gpt-4o, options: gpt-4o, gpt-4-turbo, gpt-4, gpt-3.5-turbo)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="OpenAI API key (or set OPENAI_API_KEY env var)"
    )
    parser.add_argument(
        "--module",
        type=str,
        default="general",
        help="Security module to use: general (default), ctf, code_security"
    )
    parser.add_argument(
        "--list-modules",
        action="store_true",
        help="List available security modules and exit"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Handle --list-modules
    if args.list_modules:
        modules = list_available_modules()
        print("\nAvailable Security Modules:")
        print("=" * 60)
        for name, display_name in modules.items():
            print(f"  {name:20} - {display_name}")
        print("=" * 60)
        print(f"\nUsage: --module <name>")
        sys.exit(0)

    # Set verbose logging if requested
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Check for API key
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OpenAI API key not found. Set OPENAI_API_KEY environment variable or use --api-key")
        sys.exit(1)

    os.environ["OPENAI_API_KEY"] = api_key

    # Create output directory
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    logger.info("=" * 80)
    logger.info("CYBER-AUTOAGENT - SIMPLE CLI")
    logger.info("=" * 80)
    logger.info(f"Module: {args.module}")
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
        config=config,
        module=args.module
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
