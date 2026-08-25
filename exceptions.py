"""exceptions.py for implementing error handling for edge cases"""
import logging
from typing import Any, Callable, Optional, Dict
from contextlib import contextmanager
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Custom exceptions and handlers for automation edge cases
class AutomationError(Exception):
    def __init__(self, message: str, error_code: int = 500, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.context = context or {}
    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message}"
class EdgeCaseError(AutomationError):
    pass
class FileNotFoundError(EdgeCaseError):
    def __init__(self, filepath: str):
        super().__init__(f"File not found at {filepath}", 404, {"filepath": filepath})
class InvalidInputError(EdgeCaseError):
    def __init__(self, input_name: str, details: str):
        super().__init__(f"Invalid input {input_name}: {details}", 400, {"input": input_name, "details": details})
class TimeoutError(EdgeCaseError):
    def __init__(self, task: str, seconds: float):
        super().__init__(f"Timeout after {seconds}s on {task}", 408, {"task": task, "timeout": seconds})
class ResourceError(EdgeCaseError):
    def __init__(self, resource_type: str, current: int, max_allowed: int):
        super().__init__(f"{resource_type} limit exceeded: {current}/{max_allowed}", 429, {"resource": resource_type, "current": current, "max": max_allowed})
@contextmanager
def handle_edge_cases(operation_name: str):
    try:
        logging.info(f"Beginning operation: {operation_name}")
        yield
        logging.info(f"Operation completed: {operation_name}")
    except FileNotFoundError as e:
        logging.warning(f"File edge case: {e}. Using defaults.")
    except InvalidInputError as e:
        logging.error(f"Input edge case: {e}")
        raise
    except TimeoutError as e:
        logging.warning(f"Timeout edge case: {e}. Proceeding without result.")
    except ResourceError as e:
        logging.critical(f"Resource edge case: {e}")
        raise
    except EdgeCaseError as e:
        logging.error(f"General edge case: {e}")
    except Exception as e:
        logging.exception(f"Unexpected error during {operation_name}")
        raise AutomationError(f"Unhandled error in {operation_name}: {str(e)}") from e
def safe_run(func: Callable[[], Any], default: Any = None) -> Any:
    try:
        return func()
    except FileNotFoundError as e:
        logging.warning(str(e))
        return default
    except InvalidInputError as e:
        logging.error(str(e))
        return default
    except TimeoutError as e:
        logging.warning(str(e))
        return default
    except ResourceError as e:
        logging.error(str(e))
        return None
    except EdgeCaseError as e:
        logging.error(str(e))
        return default
    except Exception as e:
        logging.error(f"Unexpected: {e}")
        raise AutomationError(str(e)) from e