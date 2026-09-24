"""Configuration management for Titanic Analysis."""

from pathlib import Path
from typing import Any, Optional

import yaml


class Config:
    """Configuration loader and manager."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._default_config_path()
        self._config: dict[str, Any] = {}
        self.load()

    def _default_config_path(self) -> str:
        """Get default config path."""
        return str(Path(__file__).parent.parent.parent / "config" / "settings.yaml")

    def load(self) -> None:
        """Load configuration from YAML file."""
        with open(self.config_path, encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'visualization.style')."""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    def get_section(self, section: str) -> dict[str, Any]:
        """Get entire configuration section."""
        return self._config.get(section, {})

    @property
    def config(self) -> dict[str, Any]:
        """Return full configuration."""
        return self._config.copy()


_config_instance: Optional[Config] = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get singleton config instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance
