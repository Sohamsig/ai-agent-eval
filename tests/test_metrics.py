from metrics.calculate_metrics import calculate_metrics


def test_metrics_for_first_attempt_success():
    results = [
        {
            "agent": "agent_01",
            "tests_passed": "True",
            "recovery_attempted": "False",
            "recovery_success": "False",
            "attempts_used": "1",
            "duration_seconds": "1.0",
            "failure_type": "success",
        },
    ]

    attempts = [
        {
            "agent": "agent_01",
            "attempt_number": "1",
            "failure_type": "success",
        },
    ]

    metrics = calculate_metrics(results, attempts)
    data = metrics["agents"]["agent_01"]

    assert data["runs"] == 1
    assert data["pass_at_1"] == 1.0
    assert data["eventual_success_rate"] == 1.0
    assert data["recovery_attempt_rate"] == 0.0
    assert data["recovery_successes"] == 0
    assert data["recovery_failures"] == 0
    assert data["average_attempts_used"] == 1.0
    assert data["average_runtime_seconds"] == 1.0
    assert data["failure_types"] == {"success": 1}
    assert data["attempt_failure_types"] == {"success": 1}
    assert data["first_attempt_failure_types"] == {}
    assert data["first_attempt_successes"] == 1
    assert data["eventual_successes"] == 1


def test_metrics_for_successful_recovery():
    results = [
        {
            "agent": "agent_04",
            "tests_passed": "True",
            "recovery_attempted": "True",
            "recovery_success": "True",
            "attempts_used": "2",
            "duration_seconds": "2.0",
            "failure_type": "success",
        },
    ]

    attempts = [
        {
            "agent": "agent_04",
            "attempt_number": "1",
            "failure_type": "assertion_failure",
        },
        {
            "agent": "agent_04",
            "attempt_number": "2",
            "failure_type": "success",
        },
    ]

    metrics = calculate_metrics(results, attempts)
    data = metrics["agents"]["agent_04"]

    assert data["runs"] == 1
    assert data["pass_at_1"] == 0.0
    assert data["eventual_success_rate"] == 1.0
    assert data["recovery_attempt_rate"] == 1.0
    assert data["recovery_success_rate"] == 1.0
    assert data["recovery_failure_rate"] == 0.0
    assert data["average_attempts_used"] == 2.0
    assert data["average_runtime_seconds"] == 2.0

    assert data["failure_types"] == {"success": 1}
    assert data["attempt_failure_types"] == {
        "assertion_failure": 1,
        "success": 1,
    }
    assert data["first_attempt_failure_types"] == {
        "assertion_failure": 1,
    }

    assert data["first_attempt_successes"] == 0
    assert data["eventual_successes"] == 1
    assert data["recovery_attempts"] == 1
    assert data["recovery_successes"] == 1
    assert data["recovery_failures"] == 0


def test_metrics_for_failed_recovery():
    results = [
        {
            "agent": "agent_05",
            "tests_passed": "False",
            "recovery_attempted": "True",
            "recovery_success": "False",
            "attempts_used": "1",
            "duration_seconds": "0.5",
            "failure_type": "recovery_error",
        },
    ]

    attempts = [
        {
            "agent": "agent_05",
            "attempt_number": "1",
            "failure_type": "assertion_failure",
        },
    ]

    metrics = calculate_metrics(results, attempts)
    data = metrics["agents"]["agent_05"]

    assert data["runs"] == 1
    assert data["pass_at_1"] == 0.0
    assert data["eventual_success_rate"] == 0.0
    assert data["recovery_attempt_rate"] == 1.0
    assert data["recovery_success_rate"] == 0.0
    assert data["recovery_failure_rate"] == 1.0

    assert data["average_attempts_used"] == 1.0
    assert data["average_runtime_seconds"] == 0.5

    assert data["failure_types"] == {"recovery_error": 1}
    assert data["attempt_failure_types"] == {
        "assertion_failure": 1,
    }
    assert data["first_attempt_failure_types"] == {
        "assertion_failure": 1,
    }

    assert data["first_attempt_successes"] == 0
    assert data["eventual_successes"] == 0
    assert data["recovery_attempts"] == 1
    assert data["recovery_successes"] == 0
    assert data["recovery_failures"] == 1


def test_metrics_for_multiple_agents():
    results = [
        {
            "agent": "baseline",
            "tests_passed": "True",
            "recovery_attempted": "False",
            "recovery_success": "False",
            "attempts_used": "1",
            "duration_seconds": "1.0",
            "failure_type": "success",
        },
        {
            "agent": "agent_04",
            "tests_passed": "True",
            "recovery_attempted": "True",
            "recovery_success": "True",
            "attempts_used": "2",
            "duration_seconds": "2.0",
            "failure_type": "success",
        },
    ]

    attempts = [
        {
            "agent": "baseline",
            "attempt_number": "1",
            "failure_type": "success",
        },
        {
            "agent": "agent_04",
            "attempt_number": "1",
            "failure_type": "assertion_failure",
        },
        {
            "agent": "agent_04",
            "attempt_number": "2",
            "failure_type": "success",
        },
    ]

    metrics = calculate_metrics(results, attempts)

    assert metrics["benchmark"]["total_runs"] == 2
    assert metrics["benchmark"]["total_attempts"] == 3
    assert metrics["benchmark"]["agents"] == 2

    assert metrics["agents"]["baseline"]["pass_at_1"] == 1.0
    assert metrics["agents"]["agent_04"]["pass_at_1"] == 0.0

    assert (
        metrics["agents"]["baseline"]["eventual_success_rate"]
        == 1.0
    )
    assert (
        metrics["agents"]["agent_04"]["eventual_success_rate"]
        == 1.0
    )
