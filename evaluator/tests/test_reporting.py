from evaluator.reporting import build_report, duplicate_report, normalize_final_record, summarize_records
from evaluator.summary import render_summary

def test_legacy_normalization_preserves_unknown_values():
    row=normalize_final_record({"task_id":"t","agent":"a","run":"1","passed":"true","duration_seconds":"unknown"}); assert row["run_number"]=="1" and row["final_success"]=="true" and row["duration_seconds"] is None
def test_v2_multiple_agents_and_rate():
    report=build_report([{"run_id":"one","task_id":"t","agent":"a","run_number":1,"final_success":True},{"run_id":"two","task_id":"t","agent":"b","run_number":1,"final_success":False}],"sample.csv"); assert set(report["agents"])=={"a","b"} and report["success_rate"]==50.0
def test_duplicates_are_not_silently_selected():
    rows=[{"task_id":"t","agent":"a","run_number":1,"final_success":True},{"task_id":"t","agent":"a","run_number":1,"final_success":False}]; report=build_report(rows,"sample.csv"); assert duplicate_report(rows)["duplicate_groups"]==1 and report["unique_unambiguous_runs"]==0 and report["success_rate"] is None
def test_unknown_outcome_is_not_failure():
    summary=summarize_records([{"task_id":"t","agent":"a","run_number":1,"final_success":"unknown"}]); assert summary["agents"]["a"]["known_outcomes"]==0 and summary["agents"]["a"]["success_rate"] is None


def test_summary_renders_na_for_no_recovery_attempts():
    report = build_report(
        [
            {
                "run_id": "one",
                "task_id": "t",
                "agent": "a",
                "run_number": 1,
                "final_success": True,
            }
        ],
        "sample.csv",
    )

    summary = render_summary(report)

    assert "| a | 1 | 100.0% | 100.0% | 1.0 | N/A | 0.0 |" in summary
    assert "None%" not in summary

def test_hidden_test_analysis_distinguishes_not_executed():
    rows = [
        {
            "run_id": "hidden-pass",
            "task_id": "task_32",
            "agent": "baseline",
            "run_number": 1,
            "final_success": True,
            "stdout": """
============================= test session starts =============================
__hidden_tests__/test_task_32_hidden.py::test_negative_timeout_rejected PASSED
============================== 6 passed in 0.02s ==============================
""",
            "stderr": "",
        },
        {
            "run_id": "hidden-not-run",
            "task_id": "task_32",
            "agent": "agent_05",
            "run_number": 1,
            "final_success": False,
            "failure_type": "recovery_error",
            "stdout": """
============================= test session starts =============================
test_client.py ....F.FF.F....... [100%]
======================== 4 failed, 13 passed in 0.18s ========================
""",
            "stderr": "",
        },
    ]

    from evaluator.reporting import hidden_test_analysis

    analysis = hidden_test_analysis(rows)

    assert analysis["hidden_test_successes"] == 1
    assert analysis["hidden_test_failures"] == 0
    assert analysis["hidden_test_not_executed"] == 1
    assert analysis["hidden_test_observations"] == 2

def test_summary_renders_hidden_tests_not_executed():
    report = build_report(
        [
            {
                "run_id": "hidden-pass",
                "task_id": "task_32",
                "agent": "baseline",
                "run_number": 1,
                "final_success": True,
                "stdout": "__hidden_tests__/test_task_32_hidden.py::test_example PASSED",
                "stderr": "",
            },
            {
                "run_id": "hidden-not-run",
                "task_id": "task_32",
                "agent": "agent_05",
                "run_number": 1,
                "final_success": False,
                "failure_type": "recovery_error",
                "stdout": "test_client.py ....F.FF.F.......",
                "stderr": "",
            },
        ],
        "sample.csv",
    )

    summary = render_summary(report)

    assert "- Hidden tests not executed: 1" in summary
