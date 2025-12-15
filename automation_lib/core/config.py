"""Configuration management for the automation framework."""

import os
from typing import Any, Dict

import yaml

from automation_lib.core.exceptions import ConfigurationError, InvalidConfigurationError


class Config:
    """Configuration manager for test settings."""

    def __init__(self, config_path: str = ""):
        """Initialize configuration.

        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self._config_data: Dict[str, Any] = {}

        if config_path and os.path.exists(config_path):
            self.load_config(config_path)

    def load_config(self, config_path: str) -> None:
        """Load configuration from YAML file.

        Args:
            config_path: Path to the YAML configuration file

        Raises:
            ConfigurationError: If configuration loading fails
        """
        try:
            if not os.path.exists(config_path):
                raise ConfigurationError(
                    message=f"Configuration file not found: {config_path}"
                )

            with open(config_path, "r") as file:
                self._config_data = yaml.safe_load(file) or {}

            if not isinstance(self._config_data, dict):
                raise InvalidConfigurationError(
                    key="root",
                    value=type(self._config_data).__name__,
                    reason="Configuration must be a dictionary/mapping",
                )
        except Exception as e:
            raise ConfigurationError(
                message=f"Failed to load configuration from {config_path}",
                details=str(e),
            )

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.

        Args:
            key: Configuration key (supports dot notation, e.g., 'db.host')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self._config_data

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

        return value if value else default

    def get_env(self, key: str, default: str = "") -> str:
        """Get value from environment variable.

        Args:
            key: Environment variable name
            default: Default value if not found

        Returns:
            Environment variable value
        """
        return os.getenv(key, default)
