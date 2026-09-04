import os
import json
import logging

# Configure logger for automation-tool-60
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(filepath: str) -> dict:
    """Loads configuration from a JSON file with robust error handling."""
    if not filepath:
        raise ValueError("Configuration path cannot be empty")

    if not os.path.exists(filepath):
        logger.error(f"Config file missing: {filepath}")
        return {}

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in {filepath}: {e}")
        return {}
    except PermissionError:
        logger.error(f"Permission denied accessing {filepath}")
        return {}
    except Exception as e:
        logger.critical(f"Unexpected error loading config: {e}")
        return {}

def get_env_or_default(key: str, default: str) -> str:
    """Retrieves environment variable with fallback mechanism."""
    try:
        return os.environ.get(key, default)
    except Exception:
        return default