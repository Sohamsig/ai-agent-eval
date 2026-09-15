from pathlib import Path

from evaluator.evaluate import evaluate_with_retries


def test_retry_workflow_recovers_after_failed_initial_solution(
    tmp_path,
    monkeypatch,
):
    test_results = [
        {
            "passed": False,
            "failure_type": "assertion_failure",
            "stdout": "assertion failed",
            "stderr": "",
            "return_code": 1,
        },
        {
            "passed": True,
            "failure_type": "success",
            "stdout": "1 passed",
            "stderr": "",
            "return_code": 0,
        },
    ]

    repair_calls = []

    def fake_run_tests(*args, **kwargs):
        return test_results.pop(0)

    def fake_run_failure_analysis(*args, **kwargs):
        return {
            "category": "assertion_failure",
            "summary": "Expected value did not match.",
        }

    def fake_apply_agent_solution(*args, **kwargs):
        return []

    def fake_append_attempt_result(*args, **kwargs):
        pass

    def fake_append_final_result(*args, **kwargs):
        pass

    monkeypatch.setattr(
        "evaluator.evaluate.run_tests",
        fake_run_tests,
    )

    monkeypatch.setattr(
        "evaluator.evaluate.run_hidden_tests",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "evaluator.evaluate.run_failure_analysis",
        fake_run_failure_analysis,
    )

    monkeypatch.setattr(
        "evaluator.evaluate.apply_agent_solution",
        fake_apply_agent_solution,
    )

    monkeypatch.setattr(
        "evaluator.evaluate.append_attempt_result",
        fake_append_attempt_result,
    )

    monkeypatch.setattr(
        "evaluator.evaluate.append_final_result",
        fake_append_final_result,
    )

    monkeypatch.setattr(
        "evaluator.evaluate.generate_solution",
        lambda *args, **kwargs: {
            "status": "completed",
            "files": {
                "actual_task_file.py": "VALUE = 1\n",
            },
        },
    )

    monkeypatch.setattr(
        "evaluator.evaluate.load_agent",
        lambda *args, **kwargs: type(
            "FakeAgent",
            (),
            {
                "repair": staticmethod(
                    lambda task_id, workspace, context: (
                        repair_calls.append("repair")
                        or {
                            "status": "completed",
                            "files": {
                                "actual_task_file.py": "VALUE = 42\n",
                            },
                        }
                    )
                )
            },
        ),
    )

    result = evaluate_with_retries(
        task_id="task_test",
        agent="baseline",
        repo_path=tmp_path,
        test_command="python -m pytest",
        run_number=1,
        max_attempts=2,
    )

    assert result["final_success"] is True
    assert result["recovery_attempted"] is True
    assert result["recovery_success"] is True
    assert result["attempts_used"] == 2
    assert result["failure_type"] == "success"
    assert repair_calls == ["repair"]