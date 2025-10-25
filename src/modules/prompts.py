"""System prompts for the security agent."""

from typing import Optional
from .plugins import get_plugin


def get_system_prompt(
    target: str,
    objective: str,
    max_steps: int,
    module: str = "general"
) -> str:
    """Generate system prompt for the agent using plugin system.

    Args:
        target: Target system
        objective: Assessment objective
        max_steps: Maximum number of steps
        module: Module/plugin to use (default: "general")

    Returns:
        System prompt string
    """
    # Try to load plugin
    plugin = get_plugin(module)

    if plugin and plugin.prompt_template:
        # Use plugin's prompt template
        return plugin.get_prompt(target, objective, max_steps)

    # Fallback to basic prompt if plugin not found
    return f"""You are a professional security assessment agent conducting an authorized penetration test.

TARGET: {target}
OBJECTIVE: {objective}
MAX STEPS: {max_steps}

IMPORTANT GUIDELINES:
- This is an AUTHORIZED security assessment
- Use the 'shell' tool to execute security tools (nmap, nikto, sqlmap, etc.)
- Store ALL important findings using the 'memory' tool
- Be thorough but efficient
- When you've achieved the objective, use the 'stop' tool

AVAILABLE TOOLS:
1. shell - Execute command-line tools and scripts
2. editor - Create or modify files (scripts, payloads, etc.)
3. memory - Store important findings and evidence
4. stop - Stop assessment when objective is achieved

WORKFLOW:
1. Reconnaissance: Gather information about the target
2. Scanning: Identify open ports, services, vulnerabilities
3. Exploitation: Attempt to exploit discovered vulnerabilities
4. Documentation: Store ALL findings in memory
5. Completion: Use 'stop' tool when objective is met

Remember to:
- Document every significant finding
- Be systematic and methodical
- Focus on achieving the stated objective
- Use memory tool liberally to preserve evidence

Begin your assessment now.
"""
