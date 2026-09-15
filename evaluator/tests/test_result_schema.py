from evaluator.result_schema import (
    duplicate_keys,
    new_attempt_id,
    new_run_id,
    normalize_attempt_record,
    normalize_final_record,
    validate_attempt_record,
    validate_final_record,
)


def test_generated_identifiers_are_unique_uuid_strings():
    run_ids = {new_run_id() for _ in range(20)}
    attempt_ids = {new_attempt_id() for _ in range(20)}
    assert len(run_ids) == 20
    assert len(attempt_ids) == 20
    assert all(len(value) == 36 for value in run_ids | attempt_ids)


def test_normalize_final_legacy_fields_preserves_unknown_and_nulls():
    raw = {"task_id": "task_01", "agent": "agent_02", "run": "1", "passed": "True", "note": "keep"}
    normalized = normalize_final_record(raw)
    assert normalized["run_number"] == "1"
    assert normalized["final_success"] == "True"
    assert normalized["run_id"] is None
    assert normalized["failure_type"] is None
    assert normalized["note"] == "keep"


def test_normalize_attempt_legacy_fields_and_explicit_unknown():
    normalized = normalize_attempt_record({"run": "2", "attempt": "1", "passed": "false", "stderr": "unknown"})
    assert normalized["run_number"] == "2"
    assert normalized["attempt_number"] == "1"
    assert normalized["tests_passed"] == "false"
    assert normalized["stderr"] is None


def test_final_validation_requires_new_identity_fields():
    issues = validate_final_record({"timestamp": "2026-01-01T00:00:00+00:00", "task_id": "task_01", "agent": "agent_02", "run_number": 1})
    assert {issue.field for issue in issues} >= {"schema_version", "run_id"}


def test_attempt_validation_accepts_complete_record():
    record = {
        "schema_version": "2", "timestamp": "2026-01-01T00:00:00+00:00",
        "run_id": new_run_id(), "attempt_id": new_attempt_id(), "task_id": "task_01",
        "agent": "agent_02", "run_number": 1, "attempt_number": 1,
    }
    assert validate_attempt_record(record) == []


def test_duplicate_detection_never_discards_rows():
    records = [
        {"run_id": "same", "task_id": "task_01", "agent": "a", "run_number": 1},
        {"run_id": "same", "task_id": "task_01", "agent": "a", "run_number": 1},
        {"run_id": "other", "task_id": "task_01", "agent": "a", "run_number": 1},
    ]
    duplicates = duplicate_keys(records, record_type="final")
    assert duplicates == {("run_id", "same"): [normalize_final_record(records[0]), normalize_final_record(records[1])]}


def test_v2_writers_link_attempt_to_final_run_without_touching_historical_csvs(monkeypatch):
    from evaluator import evaluate

    captured = []
    monkeypatch.setattr(evaluate, "append_csv_row", lambda path, fields, record: captured.append((path, fields, record)))
    run_id = new_run_id()
    evaluate.append_attempt_result(
        task_id="task_01", agent="agent_02", run_number=1, attempt_number=1,
        generation_success=True,
        run_id=run_id,
        test_result={"tests_executed": True, "passed": True, "return_code": 0, "duration_seconds": 0.1},
    )
    evaluate.append_final_result({
        "run_id": run_id, "task_id": "task_01", "agent": "agent_02", "run_number": 1,
        "generation_success": True, "tests_executed": True, "final_success": True,
        "attempts_used": 1, "max_attempts": 3, "duration_seconds": 0.1,
    })

    attempt = captured[0][2]
    final = captured[1][2]
    assert attempt["run_id"] == final["run_id"] == run_id
    assert attempt["attempt_id"]
