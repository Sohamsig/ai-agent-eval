from types import SimpleNamespace

from evaluator.evaluate import attempt_repair


def test_attempt_repair_returns_none_when_repair_is_missing(tmp_path):
    agent = SimpleNamespace()

    result = attempt_repair(
        agent_module=agent,
        task_id="task_test",
        workspace=tmp_path,
        previous_solution={},
        test_result={},
        failure_analysis={},
    )

    assert result is None


def test_attempt_repair_supports_three_argument_signature(tmp_path):
    calls = []

    def repair(task_id, workspace, context):
        calls.append((task_id, workspace, context))

        return {
            "status": "completed",
            "message": "Repair completed.",
            "files": {
                "actual_task_file.py": "VALUE = 42\n",
            },
        }

    agent = SimpleNamespace(repair=repair)

    result = attempt_repair(
        agent_module=agent,
        task_id="task_test",
        workspace=tmp_path,
        previous_solution={"old": "solution"},
        test_result={"passed": False},
        failure_analysis={"category": "test_failure"},
    )

    assert result is not None
    assert result["status"] == "completed"
    assert "actual_task_file.py" in result["files"]
    assert len(calls) == 1
    assert calls[0][0] == "task_test"


def test_attempt_repair_supports_two_argument_signature(tmp_path):
    def repair(task_id, context):
        return {
            "status": "completed",
            "files": {
                "actual_task_file.py": "VALUE = 42\n",
            },
        }

    agent = SimpleNamespace(repair=repair)

    result = attempt_repair(
        agent_module=agent,
        task_id="task_test",
        workspace=tmp_path,
        previous_solution={},
        test_result={},
        failure_analysis={},
    )

    assert result is not None
    assert result["status"] == "completed"


def test_attempt_repair_supports_one_argument_signature(tmp_path):
    def repair(context):
        return {
            "status": "completed",
            "files": {
                "actual_task_file.py": "VALUE = 42\n",
            },
        }

    agent = SimpleNamespace(repair=repair)

    result = attempt_repair(
        agent_module=agent,
        task_id="task_test",
        workspace=tmp_path,
        previous_solution={},
        test_result={},
        failure_analysis={},
    )

    assert result is not None
    assert result["status"] == "completed"