import time
from typing import Any, Callable, Dict, List, Tuple


class AutomationRunner:
    """A core engine to execute a sequence of automation tasks.

    This class manages the registration and sequential execution of tasks,
    tracking their execution time, status, and output.
    """

    def __init__(self, name: str) -> None:
        """Initializes the runner with a specific name."""
        self.name: str = name
        self.tasks: List[Tuple[str, Callable[..., Any]]] = []
        self.results: Dict[str, Dict[str, Any]] = {}

    def register_task(self, task_name: str, func: Callable[..., Any]) -> None:
        """Registers a callable task with a unique name.

        Args:
            task_name: Unique identifier for the task.
            func: The callable function to execute.
        """
        self.tasks.append((task_name, func))

    def run_all(self, *args: Any, **kwargs: Any) -> Dict[str, Dict[str, Any]]:
        """Executes all registered tasks sequentially.

        Args:
            *args: Positional arguments passed to each task.
            **kwargs: Keyword arguments passed to each task.

        Returns:
            A dictionary containing the status, execution time, and result
            of each executed task.
        """
        for task_name, func in self.tasks:
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                duration = time.perf_counter() - start_time
                self.results[task_name] = {
                    "status": "success",
                    "result": result,
                    "duration_seconds": round(duration, 4),
                }
            except Exception as exc:
                duration = time.perf_counter() - start_time
                self.results[task_name] = {
                    "status": "failed",
                    "error": str(exc),
                    "duration_seconds": round(duration, 4),
                }
        return self.results
