from typing import Final
from enum import Enum

# Application-wide configuration settings
DEFAULT_TIMEOUT: Final[int] = 30
MAX_RETRIES: Final[int] = 3
BASE_DIRECTORY: Final[str] = "./data"

class AutomationMode(Enum):
    """Supported execution modes for the automation tool."""
    DEBUG: str = "debug"
    PRODUCTION: str = "production"
    TEST: str = "test"

# System environment identifiers
SUPPORTED_PLATFORMS: Final[list[str]] = ["linux", "darwin", "windows"]
VERSION_TAG: Final[str] = "v1.0.4"

def get_timeout_buffer(multiplier: float) -> int:
    """Calculate dynamic timeout duration based on multiplier."""
    return int(DEFAULT_TIMEOUT * multiplier)

# Validation error messages
ERROR_MSG_INVALID_PATH: Final[str] = "Provided path does not exist or is inaccessible."
ERROR_MSG_CONNECTION_FAILED: Final[str] = "Unable to establish connection to target host."