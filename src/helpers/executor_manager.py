from typing import Any

import os

from collections.abc import Generator
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed, wait


class ExecutorManager:
    """Manages executor and processing of futures."""

    def __init__(self, executor_type: str = "thread") -> None:
        self.cpu_count = os.cpu_count() or 2
        self.executor_type = executor_type
        (self.executor_class, self.num_workers) = self._select_executor()

    def _select_executor(self) -> tuple[type[ProcessPoolExecutor | ThreadPoolExecutor], int]:
        """Select the appropriate executor and determine the number of workers."""
        if self.executor_type == "process":
            return ProcessPoolExecutor, self.cpu_count - 1
        return ThreadPoolExecutor, self.cpu_count * 2 - 1

    def execute_tasks(
        self, tasks: Generator[Any, None, None], process_func: Any, mode: str = "as_completed"
    ) -> Generator[Any, None, None]:
        """Execute the tasks using the selected executor and mode."""

        with self.executor_class(max_workers=self.num_workers) as executor:
            futures = [executor.submit(process_func, task) for task in tasks]

            futures_iter: Any

            if mode == "wait":
                done, _ = wait(futures)
                futures_iter = done
            else:
                futures_iter = as_completed(futures)

            for future in futures_iter:
                result = future.result()
                if result is not None:
                    yield result
