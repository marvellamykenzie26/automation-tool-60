from typing import Optional

class AutomationError(Exception):
    """Base exception class for automation-tool-60."""
    def __init__(self, message: str, code: Optional[int] = None) -> None:
        super().__init__(message)
        self.code = code

class ConfigurationError(AutomationError):
    """Raised when configuration values are invalid or missing."""
    pass

class ProcessingError(AutomationError):
    """Raised when an error occurs during task execution."""
    def __init__(self, message: str, task_id: str, code: Optional[int] = None) -> None:
        super().__init__(message, code)
        self.task_id = task_id

class ValidationError(AutomationError):
    """Raised when input data fails validation checks."""
    def __init__(self, message: str, field: str) -> None:
        super().__init__(message)
        self.field = field

class ResourceNotFoundError(AutomationError):
    """Raised when a required resource cannot be located."""
    def __init__(self, resource_name: str) -> None:
        super().__init__(f"Resource '{resource_name}' not found.")
        self.resource_name = resource_name