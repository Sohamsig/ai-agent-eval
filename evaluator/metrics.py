import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, pstdev

try:
    from .statistical_utils import (
        rate_statistics,
        print_rate_statistics,
    )
except ImportError:
    from statistical_utils import (
        rate_statistics,
        print_rate_statistics,
    )


RESULTS_FILE = Path(
    "results/results_v2_execution.csv"
)

ATTEMPTS_FILE = Path(
    "results/attempts_v2_execution.csv"
)


def load_csv(path):
    """Load a CSV file into a list of dictionaries."""

    if not path.exists():
        return []

    with path.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        return list(csv.DictReader(file))


def filter_experiment(
    rows,
    experiment_id=None,
):
    """Filter execution records by experiment ID."""

    if not experiment_id:
        return rows

    return [
        row
        for row in rows
        if row.get("experiment_id") == experiment_id
    ]


def as_bool(value):
    """Convert a CSV value to bool."""

    return (
        str(value)
        .strip()
        .lower()
        == "true"
    )


def as_float(value, default=0.0):
    """Safely convert a value to float."""

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value, default=0):
    """Safely convert a value to int."""

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def group_runs(rows):
    """Group final results by task and agent."""

    grouped = defaultdict(list)

    for row in rows:
        key = (
            row.get("task_id", ""),
            row.get("agent", ""),
        )

        grouped[key].append(row)

    return grouped


def group_attempts(rows):
    """Group attempt records by run ID."""

    grouped = defaultdict(list)

    for row in rows:
        grouped[row.get("run_id", "")].append(row)

    return grouped


def calculate_metrics(
    result_rows,
    attempt_rows,
):
    """Calculate run-level and attempt-level reliability metrics."""

    grouped_results = group_runs(
        result_rows
    )

    grouped_attempts = group_attempts(
        attempt_rows
    )

    metrics = {}

    for (
        task_id,
        agent,
    ), runs in grouped_results.items():

        total_runs = len(runs)

        successful_runs = [
            row
            for row in runs
            if as_bool(
                row.get("final_success")
            )
        ]

        generation_successes = [
            row
            for row in runs
            if as_bool(
                row.get(
                    "generation_success"
                )
            )
        ]

        test_executed_runs = [
            row
            for row in runs
            if as_bool(
                row.get(
                    "tests_executed"
                )
            )
        ]

        test_passed_runs = [
            row
            for row in runs
            if as_bool(
                row.get(
                    "tests_passed"
                )
            )
        ]

        success_rate = (
            len(successful_runs)
            / total_runs
            * 100
            if total_runs
            else 0.0
        )

        generation_success_rate = (
            len(generation_successes)
            / total_runs
            * 100
            if total_runs
            else 0.0
        )

        test_execution_rate = (
            len(test_executed_runs)
            / total_runs
            * 100
            if total_runs
            else 0.0
        )

        test_pass_rate = (
            len(test_passed_runs)
            / len(test_executed_runs)
            * 100
            if test_executed_runs
            else 0.0
        )

        # ---------------------------------------------------------
        # Group attempts by run
        # ---------------------------------------------------------

        run_attempts = {}

        for run in runs:
            run_id = run.get(
                "run_id",
                "",
            )

            attempts = sorted(
                grouped_attempts.get(
                    run_id,
                    [],
                ),
                key=lambda row: as_int(
                    row.get(
                        "attempt_number"
                    )
                ),
            )

            run_attempts[run_id] = attempts

        # ---------------------------------------------------------
        # True Pass@1
        # ---------------------------------------------------------

        first_attempt_successes = 0

        for attempts in run_attempts.values():

            if not attempts:
                continue

            first_attempt = attempts[0]

            if (
                as_int(
                    first_attempt.get(
                        "attempt_number"
                    )
                )
                == 1
                and as_bool(
                    first_attempt.get(
                        "tests_passed"
                    )
                )
            ):
                first_attempt_successes += 1

        pass_at_1 = (
            first_attempt_successes
            / total_runs
            * 100
            if total_runs
            else 0.0
        )

        # ---------------------------------------------------------
        # Recovery
        # ---------------------------------------------------------

        recovery_triggered_runs = [
            attempts
            for run_id, attempts in run_attempts.items()
            if any(
                as_bool(row.get("recovery_attempted"))
                for row in result_rows
                if row.get("run_id") == run_id
            )
        ]

        recovery_completed_runs = [
            attempts
            for attempts in recovery_triggered_runs
            if len(attempts) > 1
        ]

        recovery_trigger_rate = (
            len(recovery_triggered_runs)
            / total_runs
            * 100
            if total_runs
            else 0.0
        )

        # Backward-compatible name used by existing reporting code.
        recovery_attempt_rate = recovery_trigger_rate

        recovery_completed_rate = (
            len(recovery_completed_runs)
            / len(recovery_triggered_runs)
            * 100
            if recovery_triggered_runs
            else 0.0
        )

        recovery_success_count = 0

        for attempts in recovery_completed_runs:
            final_attempt = attempts[-1]

            if as_bool(final_attempt.get("tests_passed")):
                recovery_success_count += 1

        recovery_success_rate = (
            recovery_success_count
            / len(recovery_completed_runs)
            * 100
            if recovery_completed_runs
            else 0.0
        )

        recovery_error_count = (
            len(recovery_triggered_runs)
            - len(recovery_completed_runs)
        )

        recovery_error_rate = (
            recovery_error_count
            / len(recovery_triggered_runs)
            * 100
            if recovery_triggered_runs
            else 0.0
        )
        # ---------------------------------------------------------
        # Attempts
        # ---------------------------------------------------------

        attempts_used = [
            len(attempts)
            for attempts in run_attempts.values()
            if attempts
        ]

        average_attempts = (
            mean(attempts_used)
            if attempts_used
            else 0.0
        )

        # ---------------------------------------------------------
        # Runtime
        # ---------------------------------------------------------

        runtimes = [
            as_float(
                row.get(
                    "duration_seconds"
                )
            )
            for row in runs
            if row.get(
                "duration_seconds"
            )
            not in ("", None)
        ]

        average_runtime = (
            mean(runtimes)
            if runtimes
            else 0.0
        )

        runtime_stddev = (
            pstdev(runtimes)
            if len(runtimes) > 1
            else 0.0
        )

        # ---------------------------------------------------------
        # Success variance
        # ---------------------------------------------------------

        success_probability = (
            len(successful_runs)
            / total_runs
            if total_runs
            else 0.0
        )

        success_variance = (
            success_probability
            * (1 - success_probability)
        )

        # ---------------------------------------------------------
        # Final failure distribution
        # ---------------------------------------------------------

        failure_types = Counter(
            row.get(
                "failure_type",
                "unknown",
            )
            for row in runs
            if row.get(
                "failure_type"
            )
        )

        # ---------------------------------------------------------
        # Attempt failure distribution
        # ---------------------------------------------------------

        attempt_failure_types = Counter()

        for attempts in run_attempts.values():

            for attempt in attempts:

                failure_type = attempt.get(
                    "failure_type"
                )

                if failure_type:
                    attempt_failure_types[
                        failure_type
                    ] += 1

        metrics[
            (
                task_id,
                agent,
            )
        ] = {
            "total_runs": total_runs,
            "success_rate": success_rate,
            "generation_success_rate": (
                generation_success_rate
            ),
            "test_execution_rate": (
                test_execution_rate
            ),
            "test_pass_rate": test_pass_rate,
            "pass_at_1": pass_at_1,
            "recovery_attempt_rate": (
                recovery_attempt_rate
            ),
            "recovery_trigger_rate": (
                recovery_trigger_rate
            ),
            "recovery_completed_rate": (
                recovery_completed_rate
            ),
            "recovery_error_rate": (
                recovery_error_rate
            ),
            "recovery_success_rate": (
                recovery_success_rate
            ),
            "average_attempts": (
                average_attempts
            ),
            "average_runtime": (
                average_runtime
            ),
            "runtime_stddev": (
                runtime_stddev
            ),
            "success_variance": (
                success_variance
            ),
            "failure_types": dict(
                failure_types
            ),
            "attempt_failure_types": dict(
                attempt_failure_types
            ),
        }

    return metrics


def print_report(metrics):
    """Print detailed metrics for every agent."""

    print()
    print("=" * 90)
    print("AGENT RELIABILITY METRICS")
    print("=" * 90)

    for (
        task_id,
        agent,
    ), data in sorted(
        metrics.items()
    ):

        print()
        print(f"Task:  {task_id}")
        print(f"Agent: {agent}")
        print("-" * 90)

        print(
            f"Runs:                    "
            f"{data['total_runs']}"
        )

        print(
            f"Success Rate:            "
            f"{data['success_rate']:.2f}%"
        )

        print(
            f"Generation Success Rate: "
            f"{data['generation_success_rate']:.2f}%"
        )

        print(
            f"Test Execution Rate:     "
            f"{data['test_execution_rate']:.2f}%"
        )

        print(
            f"Test Pass Rate:          "
            f"{data['test_pass_rate']:.2f}%"
        )

        print(
            f"Pass@1:                  "
            f"{data['pass_at_1']:.2f}%"
        )

        print(
            f"Recovery Attempt Rate:   "
            f"{data['recovery_attempt_rate']:.2f}%"
        )

        print(
            f"Recovery Trigger Rate:   {data['recovery_trigger_rate']:.2f}%"
        )

        print(
            f"Recovery Completed Rate: {data['recovery_completed_rate']:.2f}%"
        )

        print(
            f"Recovery Error Rate:     {data['recovery_error_rate']:.2f}%"
        )

        if data["recovery_attempt_rate"] > 0:
            print(
                f"Recovery Success Rate:   "
                f"{data['recovery_success_rate']:.2f}%"
            )
        else:
            print(
                "Recovery Success Rate:   "
                "N/A (no recovery runs)"
            )

        print(
            f"Average Attempts:        "
            f"{data['average_attempts']:.2f}"
        )

        print(
            f"Average Runtime:         "
            f"{data['average_runtime']:.2f}s"
        )

        print(
            f"Runtime Std Dev:         "
            f"{data['runtime_stddev']:.2f}s"
        )

        print(
            f"Success Variance:        "
            f"{data['success_variance']:.4f}"
        )

        print()
        print("Final Failure Distribution:")

        if data["failure_types"]:

            for (
                failure_type,
                count,
            ) in sorted(
                data[
                    "failure_types"
                ].items()
            ):

                percentage = (
                    count
                    / data["total_runs"]
                    * 100
                )

                print(
                    f"  {failure_type:<25}"
                    f"{count:>4} runs "
                    f"({percentage:.2f}%)"
                )

        else:
            print("  None")

        print()
        print(
            "Attempt Failure Distribution:"
        )

        if data["attempt_failure_types"]:

            for (
                failure_type,
                count,
            ) in sorted(
                data[
                    "attempt_failure_types"
                ].items()
            ):

                print(
                    f"  {failure_type:<25}"
                    f"{count:>4} attempts"
                )

        else:
            print("  None")

    print()
    print("=" * 90)


def print_comparison(metrics):
    """Print a compact cross-agent comparison."""

    if not metrics:
        return

    print()
    print("=" * 120)
    print("AGENT COMPARISON")
    print("=" * 120)

    tasks = sorted(
        {
            task_id
            for task_id, _ in metrics.keys()
        }
    )

    for task_id in tasks:

        task_metrics = {
            agent: data
            for (
                task,
                agent,
            ), data in metrics.items()
            if task == task_id
        }

        agents = sorted(
            task_metrics.keys()
        )

        print()
        print(f"Task: {task_id}")
        print()

        header = (
            f"{'Metric':<28}"
            + "".join(
                f"{agent:>14}"
                for agent in agents
            )
        )

        print(header)
        print("-" * len(header))

        rows = [
            (
                "Runs",
                lambda d:
                f"{d['total_runs']}",
            ),
            (
                "Success Rate",
                lambda d:
                f"{d['success_rate']:.2f}%",
            ),
            (
                "Generation Success",
                lambda d:
                f"{d['generation_success_rate']:.2f}%",
            ),
            (
                "Test Pass Rate",
                lambda d:
                f"{d['test_pass_rate']:.2f}%",
            ),
            (
                "Pass@1",
                lambda d:
                f"{d['pass_at_1']:.2f}%",
            ),
            (
                "Recovery Attempt Rate",
                lambda d:
                f"{d['recovery_attempt_rate']:.2f}%",
            ),
            (
                "Recovery Success Rate",
                lambda d:
                (
                    f"{d['recovery_success_rate']:.2f}%"
                    if d["recovery_attempt_rate"] > 0
                    else "N/A"
                ),
            ),
            (
                "Mean Attempts",
                lambda d:
                f"{d['average_attempts']:.2f}",
            ),
            (
                "Mean Runtime",
                lambda d:
                f"{d['average_runtime']:.2f}s",
            ),
            (
                "Runtime Std Dev",
                lambda d:
                f"{d['runtime_stddev']:.2f}s",
            ),
        ]

        for (
            label,
            formatter,
        ) in rows:

            line = f"{label:<28}"

            for agent in agents:
                line += (
                    f"{formatter(task_metrics[agent]):>14}"
                )

            print(line)

    print()
    print("=" * 120)


def print_statistical_summary(metrics):
    """Print confidence intervals for key binary reliability metrics."""

    if not metrics:
        return

    print()
    print("=" * 120)
    print("STATISTICAL SUMMARY")
    print("=" * 120)

    for (
        task_id,
        agent,
    ), data in sorted(
        metrics.items()
    ):

        total_runs = data[
            "total_runs"
        ]

        success_count = round(
            data["success_rate"]
            / 100
            * total_runs
        )

        pass_at_1_count = round(
            data["pass_at_1"]
            / 100
            * total_runs
        )

        recovery_runs_count = round(
            data[
                "recovery_attempt_rate"
            ]
            / 100
            * total_runs
        )

        recovery_success_count = round(
            data[
                "recovery_success_rate"
            ]
            / 100
            * recovery_runs_count
        )

        success_stats = rate_statistics(
            success_count,
            total_runs,
        )

        pass_at_1_stats = rate_statistics(
            pass_at_1_count,
            total_runs,
        )

        print()
        print(f"Task:  {task_id}")
        print(f"Agent: {agent}")
        print("-" * 120)

        print_rate_statistics(
            "Success Rate",
            success_stats,
        )

        print_rate_statistics(
            "Pass@1",
            pass_at_1_stats,
        )

        if recovery_runs_count > 0:

            recovery_stats = (
                rate_statistics(
                    recovery_success_count,
                    recovery_runs_count,
                )
            )

            print_rate_statistics(
                "Recovery Success Rate",
                recovery_stats,
            )

        else:

            print(
                "Recovery Success Rate:      "
                "N/A (no recovery runs)"
            )

    print()
    print("=" * 120)


def main():
    """Run metrics and comparison analysis."""

    parser = argparse.ArgumentParser(
        description=(
            "Calculate AgentReliability "
            "metrics."
        )
    )

    parser.add_argument(
        "--experiment-id",
        help=(
            "Calculate metrics only for "
            "one experiment."
        ),
    )

    args = parser.parse_args()

    if not RESULTS_FILE.exists():

        print(
            f"Results file not found: "
            f"{RESULTS_FILE}"
        )

        return

    if not ATTEMPTS_FILE.exists():

        print(
            f"Attempts file not found: "
            f"{ATTEMPTS_FILE}"
        )

        return

    result_rows = load_csv(
        RESULTS_FILE
    )

    attempt_rows = load_csv(
        ATTEMPTS_FILE
    )

    # -------------------------------------------------------------
    # Filter by experiment
    # -------------------------------------------------------------

    result_rows = filter_experiment(
        result_rows,
        args.experiment_id,
    )

    attempt_rows = filter_experiment(
        attempt_rows,
        args.experiment_id,
    )

    if args.experiment_id:

        print()
        print(
            f"Experiment: "
            f"{args.experiment_id}"
        )

        print(
            f"Final records: "
            f"{len(result_rows)}"
        )

        print(
            f"Attempt records: "
            f"{len(attempt_rows)}"
        )

    if not result_rows:

        if args.experiment_id:

            print(
                "No benchmark results found "
                f"for experiment: "
                f"{args.experiment_id}"
            )

        else:

            print(
                "No benchmark results found."
            )

        return

    if not attempt_rows:

        if args.experiment_id:

            print(
                "No attempt results found "
                f"for experiment: "
                f"{args.experiment_id}"
            )

        else:

            print(
                "No attempt results found."
            )

        return

    # -------------------------------------------------------------
    # Calculate metrics
    # -------------------------------------------------------------

    metrics = calculate_metrics(
        result_rows,
        attempt_rows,
    )

    # -------------------------------------------------------------
    # Reports
    # -------------------------------------------------------------

    print_report(metrics)

    print_comparison(metrics)

    print_statistical_summary(
        metrics
    )


if __name__ == "__main__":
    main()



