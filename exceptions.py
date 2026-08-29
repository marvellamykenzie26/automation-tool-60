"""Custom exceptions and helper functions for automation-tool-60.

Provides base error classes and common operations for error handling.
"""

import logging

from typing import Optional, Dict, Any

class BaseAutomationError(Exception):
    """Base exception class for the automation tool."""

    def __init__(self, message: str, code: int = 500, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.context = context or {}

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the error."""
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            "context": self.context
        }

class ConfigurationError(BaseAutomationError):
    """Raised when there is an issue with configuration."""

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code=400, context=context)

class NetworkError(BaseAutomationError):
    """Raised for network or connectivity issues."""

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code=503, context=context)

class TaskError(BaseAutomationError):
    """Raised when a task fails during execution."""

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, code=500, context=context)

def log_error(error: BaseAutomationError, logger: Optional[logging.Logger] = None) -> None:
    """Log the error using the provided logger or default."""

    if logger is None:
        logger = logging.getLogger(__name__)

    logger.error(
        error.message,
        extra={
            "error_code": error.code,
            "error_context": error.context,
            "error_type": error.__class__.__name__
        }
    )

def get_error_details(error: Exception) -> Dict[str, Any]:
    """Extract details from any exception, wrapping in base if needed."""

    if isinstance(error, BaseAutomationError):
        return error.to_dict()
    else:
        return {
            "error_type": error.__class__.__name__,
            "message": str(error),
            "code": 500,
            "context": {}
        }
