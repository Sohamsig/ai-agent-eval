from types import SimpleNamespace

from evaluator.evaluate import attempt_repair


def test_agent_without_repair_is_handled_safely(tmp_path):
    agent = SimpleNamespace()

    result = attempt_repair(
        agent_module=agent,
        task_id="task_test",
        workspace=tmp_path,
        previous_solution={},
        test_result={
            "passed": False,
            "failure_type": "assertion_failure",
        },
        failure_analysis={
            "category": "assertion_failure",
        },
    )

    assert result is None