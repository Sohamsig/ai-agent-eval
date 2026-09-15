from pathlib import Path
import csv
from collections import defaultdict


RESULTS_FILE = Path("results/results.csv")


def load_results():
    results = []

    with RESULTS_FILE.open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            results.append({
                "task_id": row["task_id"],
                "agent": row["agent"],
                "run_number": row["run_number"],
                "success": row["final_success"].strip().lower()
                == "true",
                "duration": float(row["duration_seconds"]),
                "attempts": int(row["attempts_used"]),
                "failure_type": row["failure_type"],
                "generation_success": row["generation_success"],
                "tests_executed": row["tests_executed"],
                "recovery_attempted": row["recovery_attempted"],
                "recovery_success": row["recovery_success"],
            })

    return results


def main():
    results = load_results()

    print("\n========== FAILED RUNS ==========\n")

    failures = [
        result for result in results
        if not result["success"]
    ]

    if not failures:
        print("No failures found.")
        return

    for result in failures:
        print(f"Task: {result['task_id']}")
        print(f"Agent: {result['agent']}")
        print(f"Run: {result['run_number']}")
        print(f"Failure type: {result['failure_type']}")
        print(f"Generation success: {result['generation_success']}")
        print(f"Tests executed: {result['tests_executed']}")
        print(f"Recovery attempted: {result['recovery_attempted']}")
        print(f"Recovery success: {result['recovery_success']}")
        print(f"Duration: {result['duration']} seconds")
        print("-" * 45)


if __name__ == "__main__":
    main()