import csv
from collections import defaultdict


def generate_task_summary():

    file_path = "results/results.csv"

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        print("No evaluation results found.")
        return

    tasks = defaultdict(list)

    for row in rows:
        tasks[row["task_id"]].append(row)

    print("\n========== TASK SUMMARY ==========\n")

    for task_id, task_rows in tasks.items():

        total = len(task_rows)

        successful = sum(
            1
            for row in task_rows
            if row["passed"].lower() == "true"
        )

        failed = total - successful

        success_rate = (
            successful / total
        ) * 100

        average_duration = (
            sum(
                float(row["duration_seconds"])
                for row in task_rows
            )
            / total
        )

        print("Task:", task_id)
        print("Runs:", total)
        print("Successful:", successful)
        print("Failed:", failed)
        print(
            "Success rate:",
            round(success_rate, 2),
            "%"
        )
        print(
            "Average duration:",
            round(average_duration, 2),
            "seconds"
        )

        print("-" * 35)


if __name__ == "__main__":
    generate_task_summary()