"""Simple plugin system for loading security modules."""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
import yaml

logger = logging.getLogger(__name__)


class Plugin:
    """Represents a security assessment plugin/module."""

    def __init__(self, name: str, path: Path):
        """Initialize plugin.

        Args:
            name: Plugin name (e.g., 'general', 'ctf')
            path: Path to plugin directory
        """
        self.name = name
        self.path = path
        self.config = self._load_config()
        self.prompt_template = self._load_prompt()

    def _load_config(self) -> Dict[str, Any]:
        """Load plugin configuration from config.yaml."""
        config_file = self.path / "config.yaml"
        if not config_file.exists():
            logger.warning(f"No config.yaml found for plugin: {self.name}")
            return {"name": self.name, "display_name": self.name.title()}

        try:
            with open(config_file) as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config for {self.name}: {e}")
            return {"name": self.name, "display_name": self.name.title()}

    def _load_prompt(self) -> str:
        """Load prompt template from prompt.md."""
        prompt_file = self.path / "prompt.md"
        if not prompt_file.exists():
            logger.error(f"No prompt.md found for plugin: {self.name}")
            return ""

        try:
            with open(prompt_file) as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to load prompt for {self.name}: {e}")
            return ""

    def get_prompt(self, target: str, objective: str, max_steps: int) -> str:
        """Get formatted system prompt with variables filled in.

        Args:
            target: Target system/challenge
            objective: Assessment objective
            max_steps: Maximum steps allowed

        Returns:
            Formatted prompt string
        """
        return self.prompt_template.format(
            target=target,
            objective=objective,
            max_steps=max_steps
        )

    @property
    def display_name(self) -> str:
        """Get display name for plugin."""
        return self.config.get("display_name", self.name.title())

    @property
    def description(self) -> str:
        """Get plugin description."""
        return self.config.get("description", "")

    @property
    def recommended_tools(self) -> list:
        """Get list of recommended tools for this plugin."""
        return self.config.get("recommended_tools", [])


class PluginLoader:
    """Loads and manages security assessment plugins."""

    def __init__(self, plugins_dir: Optional[Path] = None):
        """Initialize plugin loader.

        Args:
            plugins_dir: Directory containing plugins (default: ./plugins)
        """
        if plugins_dir is None:
            plugins_dir = Path(__file__).parent.parent.parent / "plugins"

        self.plugins_dir = Path(plugins_dir)
        self.plugins: Dict[str, Plugin] = {}
        self._load_plugins()

    def _load_plugins(self):
        """Load all plugins from plugins directory."""
        if not self.plugins_dir.exists():
            logger.warning(f"Plugins directory not found: {self.plugins_dir}")
            return

        for plugin_path in self.plugins_dir.iterdir():
            if not plugin_path.is_dir():
                continue

            # Skip hidden directories
            if plugin_path.name.startswith("."):
                continue

            # Check for prompt.md (required)
            if not (plugin_path / "prompt.md").exists():
                logger.warning(f"Skipping {plugin_path.name}: no prompt.md found")
                continue

            try:
                plugin = Plugin(plugin_path.name, plugin_path)
                self.plugins[plugin.name] = plugin
                logger.info(f"Loaded plugin: {plugin.name} - {plugin.display_name}")
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin_path.name}: {e}")

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get plugin by name.

        Args:
            name: Plugin name

        Returns:
            Plugin instance or None if not found
        """
        return self.plugins.get(name)

    def list_plugins(self) -> Dict[str, str]:
        """List all available plugins.

        Returns:
            Dict mapping plugin names to display names
        """
        return {
            name: plugin.display_name
            for name, plugin in self.plugins.items()
        }

    def get_default_plugin(self) -> Optional[Plugin]:
        """Get default plugin (general)."""
        return self.get_plugin("general")


# Global plugin loader instance
_plugin_loader: Optional[PluginLoader] = None


def get_plugin_loader() -> PluginLoader:
    """Get global plugin loader instance."""
    global _plugin_loader
    if _plugin_loader is None:
        _plugin_loader = PluginLoader()
    return _plugin_loader


def get_plugin(name: str) -> Optional[Plugin]:
    """Get plugin by name (convenience function)."""
    loader = get_plugin_loader()
    return loader.get_plugin(name)


def list_available_modules() -> Dict[str, str]:
    """List all available modules (convenience function)."""
    loader = get_plugin_loader()
    return loader.list_plugins()
