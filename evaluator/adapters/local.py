from pathlib import Path
from typing import Any

from evaluator.adapters.base import AgentAdapter


class LocalAgentAdapter(AgentAdapter):
    """Adapter for the existing local Python agents."""

    def __init__(self, agent_module: Any):
        self.agent_module = agent_module

    def generate(
        self,
        task_id: str,
        workspace: Path,
    ) -> dict[str, Any]:

        if not hasattr(self.agent_module, "solve"):
            raise RuntimeError(
                "Agent does not define solve()."
            )

        solve = self.agent_module.solve

        try:
            return solve(
                task_id,
                str(workspace),
            )
        except TypeError as first_error:
            try:
                return solve(task_id)
            except TypeError:
                raise first_error

    def repair(
        self,
        task_id: str,
        workspace: Path,
        context: dict[str, Any],
    ) -> dict[str, Any] | None:

        if not hasattr(self.agent_module, "repair"):
            return None

        repair = self.agent_module.repair

        try:
            return repair(
                task_id,
                str(workspace),
                context,
            )
        except TypeError:
            try:
                return repair(
                    task_id,
                    context,
                )
            except TypeError:
                return repair(context)
