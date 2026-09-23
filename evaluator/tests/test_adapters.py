from pathlib import Path

import pytest

from evaluator.adapters.base import AgentAdapter
from evaluator.adapters.local import LocalAgentAdapter


class FakeAgent:
    def solve(self, task_id, repo_path):
        return {
            "agent": "fake",
            "status": "completed",
            "message": "Generated.",
            "files": {},
        }

    def repair(self, task_id, repo_path, context):
        return {
            "agent": "fake",
            "status": "completed",
            "message": "Repaired.",
            "files": {},
        }


class FakeAgentWithoutRepair:
    def solve(self, task_id, repo_path):
        return {
            "agent": "fake",
            "status": "completed",
            "message": "Generated.",
            "files": {},
        }


def test_local_adapter_implements_agent_adapter():
    adapter = LocalAgentAdapter(FakeAgent())

    assert isinstance(adapter, AgentAdapter)


def test_local_adapter_generate():
    adapter = LocalAgentAdapter(FakeAgent())

    result = adapter.generate(
        "task_32",
        Path("."),
    )

    assert result["status"] == "completed"


def test_local_adapter_repair():
    adapter = LocalAgentAdapter(FakeAgent())

    result = adapter.repair(
        "task_32",
        Path("."),
        {},
    )

    assert result is not None
    assert result["status"] == "completed"


def test_local_adapter_without_repair():
    adapter = LocalAgentAdapter(FakeAgentWithoutRepair())

    result = adapter.repair(
        "task_32",
        Path("."),
        {},
    )

    assert result is None


def test_local_adapter_requires_solve():
    class AgentWithoutSolve:
        pass

    adapter = LocalAgentAdapter(AgentWithoutSolve())

    with pytest.raises(RuntimeError, match="does not define solve"):
        adapter.generate(
            "task_32",
            Path("."),
        )
from evaluator.adapters.factory import create_agent_adapter
from evaluator.adapters.local import LocalAgentAdapter


def test_create_local_agent_adapter():
    adapter = create_agent_adapter(
        "local",
        object(),
    )

    assert isinstance(
        adapter,
        LocalAgentAdapter,
    )


def test_unsupported_provider_rejected():
    try:
        create_agent_adapter(
            "unknown",
            object(),
        )
    except ValueError as exc:
        assert "Unsupported agent provider" in str(exc)
    else:
        raise AssertionError(
            "Expected ValueError for unsupported provider"
        )
