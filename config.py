import json
import os
from typing import Any, Dict, Optional


class ConfigLoader:
    """Configuration loader that merges file settings with defaults."""

    DEFAULTS: Dict[str, Any] = {
        "max_retries": 5,
        "timeout_seconds": 30,
        "log_level": "INFO",
        "output_directory": "outputs",
        "enable_logging": True,
        "api_endpoint": "https://api.example.com",
    }

    def __init__(self, config_path: str = "config.json") -> None:
        self.config_path = config_path
        self.config: Dict[str, Any] = self.DEFAULTS.copy()
        self._load_from_file()

    def _load_from_file(self) -> None:
        """Load configuration from JSON file if it exists."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as file:
                    user_config = json.load(file)
                if isinstance(user_config, dict):
                    self.config.update(user_config)
            except (json.JSONDecodeError, IOError, OSError):
                pass

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Retrieve a configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Update a configuration value in memory."""
        self.config[key] = value

    def save(self) -> None:
        """Save the current configuration to the file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as file:
                json.dump(self.config, file, indent=2)
        except IOError:
            pass

    def __str__(self) -> str:
        return str(self.config)