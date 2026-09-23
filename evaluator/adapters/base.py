from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class AgentAdapter(ABC):
    """Provider-independent interface for coding agents."""

    @abstractmethod
    def generate(
        self,
        task_id: str,
        workspace: Path,
    ) -> dict[str, Any]:
        """Generate an initial solution for a task."""
        raise NotImplementedError

    @abstractmethod
    def repair(
        self,
        task_id: str,
        workspace: Path,
        context: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Generate a repaired solution after a failed attempt."""
        raise NotImplementedError
