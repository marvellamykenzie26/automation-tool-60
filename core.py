import concurrent.futures
from functools import lru_cache
from typing import Any, Dict, List, Tuple


class AutomationCore:
    """Core automation engine optimized for parallel batch execution and memoization."""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self._total_processed = 0

    @lru_cache(maxsize=512)
    def _cached_step_execution(self, step_name: str, payload_tuple: Tuple[Tuple[str, Any], ...]) -> Dict[str, Any]:
        """Executes and caches deterministic task operations to reduce redundant execution."""
        payload = dict(payload_tuple)
        return {
            "step": step_name,
            "output": f"processed_{step_name}",
            "items_count": len(payload),
        }

    def execute_batch(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processes a collection of tasks concurrently using a worker pool."""
        if not tasks:
            return []

        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_id = {
                executor.submit(self._run_task, task): task.get("id", "unknown")
                for task in tasks
            }
            for future in concurrent.futures.as_completed(future_to_id):
                task_id = future_to_id[future]
                try:
                    data = future.result()
                    results.append({"id": task_id, "status": "completed", "result": data})
                except Exception as exc:
                    results.append({"id": task_id, "status": "failed", "error": str(exc)})

        self._total_processed += len(tasks)
        return results

    def _run_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        step_name = task.get("step", "default")
        payload = task.get("payload", {})
        payload_tuple = tuple(sorted(payload.items())) if isinstance(payload, dict) else ()
        return self._cached_step_execution(step_name, payload_tuple)

    def get_metrics(self) -> Dict[str, Any]:
        """Returns engine performance and cache efficiency statistics."""
        cache_info = self._cached_step_execution.cache_info()
        return {
            "total_processed": self._total_processed,
            "cache_hits": cache_info.hits,
            "cache_misses": cache_info.misses,
            "cache_size": cache_info.currsize,
        }
