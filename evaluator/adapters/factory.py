from typing import Any

from evaluator.adapters.base import AgentAdapter
from evaluator.adapters.local import LocalAgentAdapter


def create_agent_adapter(
    provider: str,
    agent_module: Any,
) -> AgentAdapter:
    """Create an agent adapter for the selected provider."""

    if provider == "local":
        return LocalAgentAdapter(agent_module)

    raise ValueError(
        f"Unsupported agent provider: {provider}"
    )
