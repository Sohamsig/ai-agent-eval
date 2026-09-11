import csv
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_FILE = BASE_DIR / "results" / "results.csv"
OUTPUT_FILE = BASE_DIR / "results" / "benchmark_report.json"


def load_results():
    with open(RESULTS_FILE, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def build_report(rows):
    unique_runs = {}

    for row in rows:
        task_id = row["task_id"]
        agent = row["agent"]
        run_number = row["run_number"]

        key = (task_id, agent, run_number)

        # Keep one final record for every benchmark run
        unique_runs[key] = row

    runs = list(unique_runs.values())

    total_runs = len(runs)

    successful_runs = sum(
        row["final_success"].lower() == "true"
        for row in runs
    )

    pass_at_1_runs = sum(
        row["final_success"].lower() == "true"
        and row["attempts_used"] == "1"
        for row in runs
    )

    total_runtime = sum(
        float(row["duration_seconds"])
        for row in runs
    )

    total_attempts = sum(
        int(row["attempts_used"])
        for row in runs
    )

    task_report = defaultdict(list)

    for row in runs:
        task_report[row["task_id"]].append(row)

    tasks = {}

    for task_id, task_runs in sorted(task_report.items()):
        task_total = len(task_runs)

        task_successes = sum(
            row["final_success"].lower() == "true"
            for row in task_runs
        )

        task_pass_at_1 = sum(
            row["final_success"].lower() == "true"
            and row["attempts_used"] == "1"
            for row in task_runs
        )

        tasks[task_id] = {
            "runs": task_total,
            "successful_runs": task_successes,
            "success_rate": round(
                task_successes / task_total * 100,
                2
            ),
            "pass_at_1": round(
                task_pass_at_1 / task_total * 100,
                2
            ),
            "average_attempts": round(
                sum(int(row["attempts_used"]) for row in task_runs)
                / task_total,
                2
            ),
            "average_runtime_seconds": round(
                sum(float(row["duration_seconds"]) for row in task_runs)
                / task_total,
                2
            ),
        }

    report = {
        "generated_at": datetime.now().isoformat(),
        "benchmark": {
            "total_csv_rows": len(rows),
            "unique_benchmark_runs": total_runs,
            "successful_runs": successful_runs,
            "failed_runs": total_runs - successful_runs,
            "success_rate": round(
                successful_runs / total_runs * 100,
                2
            ),
            "pass_at_1": round(
                pass_at_1_runs / total_runs * 100,
                2
            ),
            "average_attempts": round(
                total_attempts / total_runs,
                2
            ),
            "average_runtime_seconds": round(
                total_runtime / total_runs,
                2
            ),
        },
        "agents": {
            "agent_02": {
                "runs": total_runs,
                "success_rate": round(
                    successful_runs / total_runs * 100,
                    2
                ),
                "pass_at_1": round(
                    pass_at_1_runs / total_runs * 100,
                    2
                ),
            }
        },
        "tasks": tasks,
    }

    return report


def main():
    if not RESULTS_FILE.exists():
        print(f"Results file not found: {RESULTS_FILE}")
        return

    rows = load_results()
    report = build_report(rows)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("Benchmark report exported successfully.")
    print(f"Output: {OUTPUT_FILE}")
    print()
    print(json.dumps(report["benchmark"], indent=4))


if __name__ == "__main__":
    main()