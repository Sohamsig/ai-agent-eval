"""Research-oriented benchmark reporting utilities."""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

from evaluator.result_schema import normalize_final_record


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"

LEGACY_RESULTS_FILE = RESULTS_DIR / "results.csv"
V2_RESULTS_FILE = RESULTS_DIR / "results_v2.csv"
ATTEMPTS_FILE = RESULTS_DIR / "attempts_v2.csv"


def default_results_path() -> Path:
    """Return the newest supported final-results CSV."""
    if V2_RESULTS_FILE.exists():
        return V2_RESULTS_FILE

    return LEGACY_RESULTS_FILE


def default_attempts_path() -> Path:
    """Return the attempts CSV when available."""
    return ATTEMPTS_FILE


def load_csv_records(
    path: Path | str,
) -> list[dict[str, Any]]:
    """Load raw CSV rows."""
    source = Path(path)

    if not source.exists():
        return []

    with source.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        return list(csv.DictReader(file))


def load_final_records(
    path: Path | str | None = None,
) -> list[dict[str, Any]]:
    """Load and normalize final benchmark records."""
    source = Path(path) if path is not None else default_results_path()

    with source.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        return [
            normalize_final_record(row)
            for row in csv.DictReader(file)
        ]


def as_bool(value: Any) -> bool | None:
    """Convert common CSV boolean values into bool."""
    if isinstance(value, bool):
        return value

    if value is None:
        return None

    normalized = str(value).strip().lower()

    if normalized in {
        "true",
        "1",
        "yes",
        "success",
        "passed",
    }:
        return True

    if normalized in {
        "false",
        "0",
        "no",
        "failed",
        "failure",
    }:
        return False

    return None


def as_float(value: Any, default: float = 0.0) -> float:
    """Safely convert a value to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    """Safely convert a value to int."""
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def logical_key(
    row: Mapping[str, Any],
) -> tuple[Any, ...]:
    """Return the logical identity of a benchmark run."""
    run_id = row.get("run_id")

    if run_id:
        return ("run_id", run_id)

    return (
        "legacy",
        row.get("task_id"),
        row.get("agent"),
        row.get("run_number"),
    )


def duplicate_report(
    records: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    """Detect duplicate logical benchmark runs."""
    groups: dict[
        tuple[Any, ...],
        list[dict[str, Any]],
    ] = defaultdict(list)

    for record in records:
        row = normalize_final_record(record)
        groups[logical_key(row)].append(row)

    duplicates = {
        key: rows
        for key, rows in groups.items()
        if len(rows) > 1
    }

    return {
        "raw_rows": sum(
            len(rows) for rows in groups.values()
        ),
        "logical_runs": len(groups),
        "duplicate_groups": len(duplicates),
        "duplicate_rows": sum(
            len(rows) - 1
            for rows in duplicates.values()
        ),
        "affected_keys": [
            list(key)
            for key in sorted(duplicates, key=str)
        ],
        "groups": dict(groups),
    }


def _success_rate(
    successful: int,
    total: int,
) -> float | None:
    """Calculate a percentage safely."""
    if total == 0:
        return None

    return round(
        successful / total * 100,
        2,
    )


def _average(
    values: list[float],
) -> float:
    """Calculate an average safely."""
    if not values:
        return 0.0

    return round(
        sum(values) / len(values),
        2,
    )


def summarize_agent(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Create research metrics for one agent."""
    outcomes = [
        as_bool(row.get("final_success"))
        for row in rows
    ]

    known_outcomes = [
        outcome
        for outcome in outcomes
        if outcome is not None
    ]

    successful_runs = sum(
        outcome is True
        for outcome in known_outcomes
    )

    attempts = [
        as_int(row.get("attempts_used"), 1)
        for row in rows
    ]

    runtimes = [
        as_float(row.get("duration_seconds"))
        for row in rows
    ]

    pass_at_1_runs = sum(
        outcome is True
        and as_int(row.get("attempts_used"), 1) == 1
        for outcome, row in zip(outcomes, rows)
    )

    recovery_attempts = sum(
        max(as_int(row.get("attempts_used"), 1) - 1, 0)
        for row in rows
    )

    recovery_successes = sum(
        as_bool(row.get("recovery_success")) is True
        for row in rows
    )

    return {
        "runs": len(rows),
        "known_outcomes": len(known_outcomes),
        "unknown_outcomes": len(rows) - len(known_outcomes),
        "successful_runs": successful_runs,
        "failed_runs": sum(
            outcome is False
            for outcome in known_outcomes
        ),
        "success_rate": _success_rate(
            successful_runs,
            len(known_outcomes),
        ),
        "pass_at_1_runs": pass_at_1_runs,
        "pass_at_1": _success_rate(
            pass_at_1_runs,
            len(rows),
        ),
        "recovery_attempts": recovery_attempts,
        "recovery_successes": recovery_successes,
        "average_attempts": _average(attempts),
        "average_runtime_seconds": _average(runtimes),
    }


def task_wise_results(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Summarize results by task."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for row in rows:
        task_id = str(row.get("task_id", "unknown"))
        grouped[task_id].append(row)

    return {
        task_id: summarize_agent(task_rows)
        for task_id, task_rows in sorted(grouped.items())
    }


def failure_categories(
    rows: list[dict[str, Any]],
) -> dict[str, int]:
    """Count final failure categories."""
    categories = Counter()

    for row in rows:
        success = as_bool(row.get("final_success"))

        if success is True:
            continue

        failure_type = (
            row.get("failure_type")
            or "unknown_failure"
        )

        categories[str(failure_type)] += 1

    return dict(sorted(categories.items()))


def hidden_test_analysis(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    """Analyze recorded hidden-test execution results."""
    hidden_test_failures = 0
    hidden_test_successes = 0
    hidden_test_not_executed = 0

    for row in rows:
        stdout = str(row.get("stdout") or "")
        stderr = str(row.get("stderr") or "")
        output = f"{stdout}\n{stderr}".lower()

        hidden_tests_executed = (
            "__hidden_tests__" in output
            or "hidden_tests" in output
            or "test_task_32_hidden.py" in output
        )

        if hidden_tests_executed:
            hidden_test_passed = (
                "passed" in output
                and "failed" not in output
            )

            hidden_test_failed = (
                "failed" in output
                or "error" in output
            )

            if hidden_test_failed:
                hidden_test_failures += 1
            elif hidden_test_passed:
                hidden_test_successes += 1
            else:
                hidden_test_not_executed += 1
        else:
            hidden_test_not_executed += 1

    return {
        "hidden_test_failures": hidden_test_failures,
        "hidden_test_successes": hidden_test_successes,
        "hidden_test_not_executed": hidden_test_not_executed,
        "hidden_test_observations": (
            hidden_test_failures
            + hidden_test_successes
            + hidden_test_not_executed
        ),
    }

def known_limitations() -> list[str]:
    """Document current benchmark limitations."""
    return [
        "The benchmark contains a limited number of tasks.",
        "The current agent implementations are limited in diversity.",
        "The recorded success rate applies only to this dataset.",
        "A 100% result does not prove general coding-agent reliability.",
        "Task difficulty is not yet calibrated across all tasks.",
        "Hidden-test coverage is limited to the available task fixtures.",
        "Runtime measurements depend on the local execution environment.",
        "The benchmark does not yet measure code quality or maintainability.",
    ]


def summarize_records(
    records: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    """Create the complete research summary."""
    normalized = [
        normalize_final_record(record)
        for record in records
    ]

    duplicates = duplicate_report(normalized)

    usable = [
        rows[0]
        for rows in duplicates["groups"].values()
        if len(rows) == 1
    ]

    agents: dict[str, Any] = {}

    for agent in sorted(
        {
            str(row.get("agent"))
            for row in usable
        }
    ):
        agent_rows = [
            row
            for row in usable
            if str(row.get("agent")) == agent
        ]

        agents[agent] = summarize_agent(agent_rows)

    known_outcomes = sum(
        item["known_outcomes"]
        for item in agents.values()
    )

    successful_runs = sum(
        item["successful_runs"]
        for item in agents.values()
    )

    total_recovery_attempts = sum(
        item["recovery_attempts"]
        for item in agents.values()
    )

    successful_recoveries = sum(
        item["recovery_successes"]
        for item in agents.values()
    )

    all_attempts = [
        as_int(row.get("attempts_used"), 1)
        for row in usable
    ]

    all_runtimes = [
        as_float(row.get("duration_seconds"))
        for row in usable
    ]

    pass_at_1_runs = sum(
        as_bool(row.get("final_success")) is True
        and as_int(row.get("attempts_used"), 1) == 1
        for row in usable
    )

    return {
        "duplicates": {
            key: value
            for key, value in duplicates.items()
            if key != "groups"
        },
        "usable_records": usable,
        "agents": agents,
        "task_wise_results": task_wise_results(usable),
        "failure_categories": failure_categories(usable),
        "hidden_test_analysis": hidden_test_analysis(usable),
        "recovery_analysis": {
            "total_recovery_attempts": total_recovery_attempts,
            "successful_recoveries": successful_recoveries,
            "recovery_rate": _success_rate(
                successful_recoveries,
                total_recovery_attempts,
            ),
            "average_attempts": _average(all_attempts),
            "average_runtime_seconds": _average(all_runtimes),
        },
        "pass_at_1": {
            "pass_at_1_runs": pass_at_1_runs,
            "pass_at_1": _success_rate(
                pass_at_1_runs,
                len(usable),
            ),
        },
        "known_outcomes": known_outcomes,
        "successful_runs": successful_runs,
    }


def build_report(
    records: Iterable[Mapping[str, Any]],
    source_path: Path | str,
) -> dict[str, Any]:
    """Build the complete research-oriented report."""
    rows = list(records)
    summary = summarize_records(rows)

    known_outcomes = summary["known_outcomes"]
    successful_runs = summary["successful_runs"]

    return {
        "report_type": (
            "AI Coding Agent Evaluation Report"
        ),
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "source_csv": str(source_path),

        "benchmark": {
            "raw_rows": len(rows),
            "unique_logical_runs": (
                summary["duplicates"]["logical_runs"]
            ),
            "unique_unambiguous_runs": len(
                summary["usable_records"]
            ),
            "excluded_ambiguous_rows": (
                summary["duplicates"]["raw_rows"]
                - len(summary["usable_records"])
            ),
            "known_outcomes": known_outcomes,
            "successful_runs": successful_runs,
            "failed_runs": (
                known_outcomes - successful_runs
            ),
            "unknown_outcomes": (
                len(summary["usable_records"])
                - known_outcomes
            ),
            "success_rate": _success_rate(
                successful_runs,
                known_outcomes,
            ),
        },

        "duplicate_analysis": summary["duplicates"],
        "agent_comparison": summary["agents"],
        "task_wise_results": summary[
            "task_wise_results"
        ],
        "failure_categories": summary[
            "failure_categories"
        ],
        "recovery_analysis": summary[
            "recovery_analysis"
        ],
        "pass_at_1": summary["pass_at_1"],
        "hidden_test_analysis": summary[
            "hidden_test_analysis"
        ],
        "known_limitations": known_limitations(),

        "agents": summary["agents"],
        "success_rate": _success_rate(
            successful_runs,
            known_outcomes,
        ),
        "raw_rows": len(rows),
        "unique_logical_runs": (
            summary["duplicates"]["logical_runs"]
        ),
        "unique_unambiguous_runs": len(
            summary["usable_records"]
        ),
        "excluded_ambiguous_rows": (
            summary["duplicates"]["raw_rows"]
            - len(summary["usable_records"])
        ),
        "known_outcomes": known_outcomes,
        "successful_runs": successful_runs,
        "failed_runs": (
            known_outcomes - successful_runs
        ),
        "unknown_outcomes": (
            len(summary["usable_records"])
            - known_outcomes
        ),
    }

