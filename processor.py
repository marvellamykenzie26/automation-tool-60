import concurrent.futures
from typing import List, Callable, Any

class BatchProcessor:
    """Efficiently processes tasks in parallel batches to optimize execution time."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def _execute_single(self, func: Callable[[Any], Any], item: Any) -> Any:
        try:
            return func(item)
        except Exception as e:
            return {"error": str(e), "item": item}

    def execute_batch(self, func: Callable[[Any], Any], items: List[Any]) -> List[Any]:
        """Executes a function over a list of items concurrently using a thread pool."""
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_item = {executor.submit(self._execute_single, func, item): item for item in items}
            for future in concurrent.futures.as_completed(future_to_item):
                try:
                    data = future.result()
                    results.append(data)
                except Exception as e:
                    item = future_to_item[future]
                    results.append({"error": f"Execution failure: {str(e)}", "item": item})
        return results