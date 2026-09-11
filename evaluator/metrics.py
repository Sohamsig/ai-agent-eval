import csv
from collections import defaultdict
from pathlib import Path


RESULTS_FILE = Path("results/results.csv")


def load_results():
    """Load benchmark results from results.csv."""

    with RESULTS_FILE.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        return list(csv.DictReader(file))


def to_bool(value):
    """Convert CSV values to boolean."""

    return str(value).strip().lower() in {
        "true",
        "1",
        "yes",
        "success",
        "passed",
    }


def to_int(value, default=1):
    """Safely convert a value to integer."""

    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def to_float(value, default=0.0):
    """Safely convert a value to float."""

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_result(row):
    """Normalize one results.csv row."""

    return {
        "timestamp": row.get("timestamp", ""),
        "task_id": row.get("task_id", "unknown_task"),
        "agent": row.get("agent", "unknown_agent"),

        # Your CSV uses run_number.
        "run_number": to_int(
            row.get("run_number", 1)
        ),

        "final_success": to_bool(
            row.get("final_success", False)
        ),

        "generation_success": to_bool(
            row.get("generation_success", False)
        ),

        "tests_executed": to_bool(
            row.get("tests_executed", False)
        ),

        "recovery_attempted": to_bool(
            row.get("recovery_attempted", False)
        ),

        "recovery_success": to_bool(
            row.get("recovery_success", False)
        ),

        "attempts_used": to_int(
            row.get("attempts_used", 1)
        ),

        "duration_seconds": to_float(
            row.get("duration_seconds", 0)
        ),

        "failure_type": row.get(
            "failure_type",
            "",
        ),
    }


def group_runs(rows):
    """
    Group benchmark runs by task, agent, and run_number.

    Each row in results.csv represents one completed benchmark run.
    """

    runs = defaultdict(list)

    for row in rows:
        result = normalize_result(row)

        key = (
            result["task_id"],
            result["agent"],
            result["run_number"],
        )

        runs[key].append(result)

    return runs


def percentage(value, total):
    """Calculate percentage safely."""

    if total == 0:
        return 0.0

    return value / total * 100


def calculate_metrics(rows):
    """Calculate agent-level metrics."""

    runs = group_runs(rows)

    stats = defaultdict(
        lambda: {
            "total_runs": 0,
            "pass_at_1": 0,
            "final_success": 0,
            "recovery_attempted": 0,
            "recovery_success": 0,
            "total_attempts": 0,
            "total_duration": 0.0,
        }
    )

    for (_, agent, _), run_rows in runs.items():
        # A results.csv row already represents a completed run.
        result = run_rows[-1]

        data = stats[agent]

        data["total_runs"] += 1

        # Pass@1 is true when the run succeeded without recovery.
        if (
            result["final_success"]
            and result["attempts_used"] == 1
        ):
            data["pass_at_1"] += 1

        if result["final_success"]:
            data["final_success"] += 1

        if result["recovery_attempted"]:
            data["recovery_attempted"] += 1

        if result["recovery_success"]:
            data["recovery_success"] += 1

        data["total_attempts"] += result["attempts_used"]
        data["total_duration"] += result["duration_seconds"]

    return stats


def calculate_task_metrics(rows):
    """Calculate metrics for every task and agent."""

    runs = group_runs(rows)

    task_stats = defaultdict(
        lambda: {
            "total_runs": 0,
            "pass_at_1": 0,
            "final_success": 0,
            "recovery_attempted": 0,
            "recovery_success": 0,
        }
    )

    for (task_id, agent, _), run_rows in runs.items():
        result = run_rows[-1]

        key = (task_id, agent)
        data = task_stats[key]

        data["total_runs"] += 1

        if (
            result["final_success"]
            and result["attempts_used"] == 1
        ):
            data["pass_at_1"] += 1

        if result["final_success"]:
            data["final_success"] += 1

        if result["recovery_attempted"]:
            data["recovery_attempted"] += 1

        if result["recovery_success"]:
            data["recovery_success"] += 1

    return task_stats


def print_summary(rows, stats):
    """Print overall benchmark summary."""

    total_runs = sum(
        data["total_runs"]
        for data in stats.values()
    )

    successful_runs = sum(
        data["final_success"]
        for data in stats.values()
    )

    pass_at_1_runs = sum(
        data["pass_at_1"]
        for data in stats.values()
    )

    print()
    print("=" * 80)
    print("OVERALL SUMMARY")
    print("=" * 80)

    print(f"CSV rows:             {len(rows)}")
    print(f"Total benchmark runs: {total_runs}")
    print(f"Successful runs:      {successful_runs}")
    print(f"Failed runs:          {total_runs - successful_runs}")

    print(
        f"Overall success:      "
        f"{percentage(successful_runs, total_runs):.2f}%"
    )

    print(
        f"Pass@1:               "
        f"{percentage(pass_at_1_runs, total_runs):.2f}%"
    )

    print("=" * 80)


def print_report(stats):
    """Print agent-level benchmark metrics."""

    print()
    print("=" * 80)
    print("AI AGENT BENCHMARK METRICS")
    print("=" * 80)

    for agent, data in sorted(stats.items()):
        total = data["total_runs"]

        if total == 0:
            continue

        print()
        print(f"Agent: {agent}")
        print("-" * 80)

        print(f"Runs:                 {total}")

        print(
            f"Pass@1:               "
            f"{percentage(data['pass_at_1'], total):.2f}%"
        )

        print(
            f"Final Success Rate:   "
            f"{percentage(data['final_success'], total):.2f}%"
        )

        print(
            f"Recovery Rate:        "
            f"{percentage(data['recovery_attempted'], total):.2f}%"
        )

        print(
            f"Recovery Success:     "
            f"{percentage(data['recovery_success'], total):.2f}%"
        )

        print(
            f"Average Attempts:     "
            f"{data['total_attempts'] / total:.2f}"
        )

        print(
            f"Average Runtime:      "
            f"{data['total_duration'] / total:.2f}s"
        )

    print()
    print("=" * 80)


def print_task_report(task_stats):
    """Print task-level benchmark metrics."""

    print()
    print("=" * 110)
    print("TASK-LEVEL BENCHMARK RESULTS")
    print("=" * 110)

    print(
        f"{'Task':<15}"
        f"{'Agent':<15}"
        f"{'Runs':<8}"
        f"{'Pass@1':<12}"
        f"{'Final':<12}"
        f"{'Recovery':<12}"
        f"{'Recovery Success':<20}"
    )

    print("-" * 110)

    for (task_id, agent), data in sorted(task_stats.items()):
        total = data["total_runs"]

        if total == 0:
            continue

        print(
            f"{task_id:<15}"
            f"{agent:<15}"
            f"{total:<8}"
            f"{percentage(data['pass_at_1'], total):<12.2f}"
            f"{percentage(data['final_success'], total):<12.2f}"
            f"{percentage(data['recovery_attempted'], total):<12.2f}"
            f"{percentage(data['recovery_success'], total):<20.2f}"
        )

    print("=" * 110)


def main():
    """Run the complete metrics report."""

    if not RESULTS_FILE.exists():
        print(f"Results file not found: {RESULTS_FILE}")
        return

    rows = load_results()

    if not rows:
        print("No benchmark results found.")
        return

    stats = calculate_metrics(rows)
    task_stats = calculate_task_metrics(rows)

    print_summary(rows, stats)
    print_report(stats)
    print_task_report(task_stats)


if __name__ == "__main__":
    main()