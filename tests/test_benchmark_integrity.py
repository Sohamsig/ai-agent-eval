

def test_final_runs_have_unique_logical_identity():
    records = [
        {
            "task_id": "task_32",
            "agent": "agent_01",
            "run_number": 1,
            "run_id": "run-1",
        },
        {
            "task_id": "task_32",
            "agent": "agent_01",
            "run_number": 2,
            "run_id": "run-2",
        },
    ]

    logical_keys = [
        (
            record["task_id"],
            record["agent"],
            record["run_number"],
        )
        for record in records
    ]

    assert len(logical_keys) == len(set(logical_keys))


def test_duplicate_logical_runs_are_detected():
    records = [
        {
            "task_id": "task_32",
            "agent": "agent_01",
            "run_number": 1,
            "run_id": "run-1",
        },
        {
            "task_id": "task_32",
            "agent": "agent_01",
            "run_number": 1,
            "run_id": "run-2",
        },
    ]

    logical_keys = [
        (
            record["task_id"],
            record["agent"],
            record["run_number"],
        )
        for record in records
    ]

    duplicate_logical_keys = {
        key
        for key in logical_keys
        if logical_keys.count(key) > 1
    }

    assert duplicate_logical_keys == {
        ("task_32", "agent_01", 1)
    }


def test_attempts_reference_existing_final_runs():
    final_runs = {
        "run-1",
        "run-2",
    }

    attempts = [
        {"run_id": "run-1", "attempt_number": 1},
        {"run_id": "run-1", "attempt_number": 2},
        {"run_id": "run-2", "attempt_number": 1},
    ]

    orphan_attempts = [
        attempt
        for attempt in attempts
        if attempt["run_id"] not in final_runs
    ]

    assert orphan_attempts == []


def test_orphan_attempt_is_detected():
    final_runs = {
        "run-1",
    }

    attempts = [
        {"run_id": "run-1", "attempt_number": 1},
        {"run_id": "missing-run", "attempt_number": 1},
    ]

    orphan_attempts = [
        attempt
        for attempt in attempts
        if attempt["run_id"] not in final_runs
    ]

    assert len(orphan_attempts) == 1
    assert orphan_attempts[0]["run_id"] == "missing-run"


def test_attempt_numbers_are_sequential():
    attempts = [
        {"run_id": "run-1", "attempt_number": 1},
        {"run_id": "run-1", "attempt_number": 2},
        {"run_id": "run-1", "attempt_number": 3},
    ]

    numbers = sorted(
        attempt["attempt_number"]
        for attempt in attempts
        if attempt["run_id"] == "run-1"
    )

    assert numbers == list(range(1, len(numbers) + 1))


def test_run_numbers_are_sequential():
    runs = [
        {"task_id": "task_32", "agent": "agent_01", "run_number": 1},
        {"task_id": "task_32", "agent": "agent_01", "run_number": 2},
        {"task_id": "task_32", "agent": "agent_01", "run_number": 3},
    ]

    numbers = sorted(
        run["run_number"]
        for run in runs
        if run["task_id"] == "task_32"
        and run["agent"] == "agent_01"
    )

    assert numbers == list(range(1, len(numbers) + 1))
