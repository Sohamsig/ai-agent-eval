import csv
from collections import defaultdict


def compare_agents():

    file_path = "results/results.csv"

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    if not rows:
        print("No evaluation results found.")
        return

    agents = defaultdict(list)

    for row in rows:
        agents[row["agent"]].append(row)

    print("\n========== AGENT COMPARISON ==========\n")

    for agent, agent_rows in agents.items():

        total = len(agent_rows)

        successful = sum(
            1
            for row in agent_rows
            if row["passed"].lower() == "true"
        )

        success_rate = (
            successful / total
        ) * 100

        average_duration = (
            sum(
                float(row["duration_seconds"])
                for row in agent_rows
            )
            / total
        )

        print("Agent:", agent)
        print("Runs:", total)
        print("Successful:", successful)
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
    compare_agents()