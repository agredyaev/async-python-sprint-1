from typing import Any

from abc import ABC, abstractmethod
from collections.abc import Generator

from src.helpers.executor_manager import ExecutorManager


class BaseTask(ABC):
    """Base class for all tasks."""

    __slots__ = ("data_in", "executor_manager")

    def __init__(self, data_in: Generator[Any, None, None], executor_type: str = "thread") -> None:
        self.data_in = data_in
        self.executor_manager = ExecutorManager(executor_type)

    @abstractmethod
    def process(self, item: Any) -> Any:
        """Method for processing item of the iterable.
        Args:
            item (Any): Item of the iterable.
        Returns:
            Any: Processed item.
        """
        raise NotImplementedError("Process method must be implemented")

    def run(self, mode: str = "as_completed") -> Generator[Any, None, None]:
        """
        Method for running task.
        Args:
            mode (str): Mode of the executor. "as_completed" or "wait" (default: "as_completed").
        Returns:
            Generator[Any, None, None]: Generator of processed items.
        """
        yield from self.executor_manager.execute_tasks(self.data_in, self.process, mode)
