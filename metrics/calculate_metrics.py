from pathlib import Path
import csv
import json
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent.parent
RESULTS_FILE = ROOT / "results" / "results_v2.csv"
ATTEMPTS_FILE = ROOT / "results" / "attempts_v2.csv"
OUTPUT_JSON = ROOT / "results" / "benchmark_metrics.json"
OUTPUT_CSV = ROOT / "results" / "benchmark_metrics.csv"


def to_bool(value):
    return str(value).strip().lower() == "true"


def to_int(value):
    if value in ("", None):
        return None
    return int(value)


def to_float(value):
    if value in ("", None):
        return None
    return float(value)


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def calculate_metrics(results, attempts):
    agents = sorted({row["agent"] for row in results})

    metrics = {
        "benchmark": {
            "total_runs": len(results),
            "total_attempts": len(attempts),
            "agents": len(agents),
        },
        "agents": {},
    }

    for agent in agents:
        agent_results = [
            row for row in results
            if row["agent"] == agent
        ]

        agent_attempts = [
            row for row in attempts
            if row["agent"] == agent
        ]

        total_runs = len(agent_results)

        first_attempts = [
            row for row in agent_attempts
            if to_int(row["attempt_number"]) == 1
        ]

        first_attempt_successes = sum(
            1
            for row in first_attempts
            if row["failure_type"] == "success"
        )

        eventual_successes = sum(
            1
            for row in agent_results
            if to_bool(row["tests_passed"])
        )

        recovery_attempts = sum(
            1
            for row in agent_results
            if to_bool(row["recovery_attempted"])
        )

        recovery_successes = sum(
            1
            for row in agent_results
            if to_bool(row["recovery_attempted"])
            and to_bool(row["recovery_success"])
        )

        recovery_failures = sum(
            1
            for row in agent_results
            if to_bool(row["recovery_attempted"])
            and not to_bool(row["recovery_success"])
        )

        attempts_used = [
            to_int(row["attempts_used"])
            for row in agent_results
            if to_int(row["attempts_used"]) is not None
        ]

        durations = [
            to_float(row["duration_seconds"])
            for row in agent_results
            if to_float(row["duration_seconds"]) is not None
        ]

        failure_types = Counter(
            row["failure_type"]
            for row in agent_results
        )

        attempt_failure_types = Counter(
            row["failure_type"]
            for row in agent_attempts
            if row.get("failure_type")
        )

        first_attempt_failure_types = Counter(
            row["failure_type"]
            for row in first_attempts
            if row.get("failure_type") and row["failure_type"] != "success"
        )

        metrics["agents"][agent] = {
            "runs": total_runs,

            "pass_at_1": (
                first_attempt_successes / total_runs
                if total_runs else 0
            ),

            "eventual_success_rate": (
                eventual_successes / total_runs
                if total_runs else 0
            ),

            "recovery_attempt_rate": (
                recovery_attempts / total_runs
                if total_runs else 0
            ),

            "recovery_success_rate": (
                recovery_successes / recovery_attempts
                if recovery_attempts else None
            ),

            "recovery_failure_rate": (
                recovery_failures / recovery_attempts
                if recovery_attempts else None
            ),

            "average_attempts_used": (
                sum(attempts_used) / len(attempts_used)
                if attempts_used else None
            ),

            "average_runtime_seconds": (
                sum(durations) / len(durations)
                if durations else None
            ),

            "failure_types": dict(failure_types),
            "attempt_failure_types": dict(attempt_failure_types),
            "first_attempt_failure_types": dict(first_attempt_failure_types),

            "first_attempt_successes": first_attempt_successes,
            "eventual_successes": eventual_successes,
            "recovery_attempts": recovery_attempts,
            "recovery_successes": recovery_successes,
            "recovery_failures": recovery_failures,
        }

    return metrics


def main():
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(
            f"Missing results file: {RESULTS_FILE}"
        )

    if not ATTEMPTS_FILE.exists():
        raise FileNotFoundError(
            f"Missing attempts file: {ATTEMPTS_FILE}"
        )

    results = load_csv(RESULTS_FILE)
    attempts = load_csv(ATTEMPTS_FILE)

    metrics = calculate_metrics(results, attempts)

    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    csv_rows = []

    for agent, data in metrics["agents"].items():
        csv_rows.append({
            "agent": agent,
            "runs": data["runs"],
            "pass_at_1": data["pass_at_1"],
            "eventual_success_rate": data["eventual_success_rate"],
            "recovery_attempt_rate": data["recovery_attempt_rate"],
            "recovery_success_rate": data["recovery_success_rate"],
            "recovery_failure_rate": data["recovery_failure_rate"],
            "average_attempts_used": data["average_attempts_used"],
            "average_runtime_seconds": data["average_runtime_seconds"],
            "first_attempt_successes": data["first_attempt_successes"],
            "eventual_successes": data["eventual_successes"],
            "recovery_attempts": data["recovery_attempts"],
            "recovery_successes": data["recovery_successes"],
            "recovery_failures": data["recovery_failures"],
        })

    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=csv_rows[0].keys()
        )
        writer.writeheader()
        writer.writerows(csv_rows)

    print("=" * 70)
    print("AGENTRELIABILITY METRICS")
    print("=" * 70)

    print(f"Total runs:     {metrics['benchmark']['total_runs']}")
    print(f"Total attempts: {metrics['benchmark']['total_attempts']}")
    print(f"Agents:         {metrics['benchmark']['agents']}")
    print()

    for agent, data in metrics["agents"].items():
        print(f"Agent: {agent}")
        print(f"  Runs:                    {data['runs']}")
        print(f"  Pass@1:                  {data['pass_at_1']:.2%}")
        print(f"  Eventual success:        {data['eventual_success_rate']:.2%}")
        print(f"  Recovery attempt rate:   {data['recovery_attempt_rate']:.2%}")

        if data["recovery_success_rate"] is not None:
            print(
                f"  Recovery success rate:   "
                f"{data['recovery_success_rate']:.2%}"
            )
        else:
            print("  Recovery success rate:   N/A")

        if data["recovery_failure_rate"] is not None:
            print(
                f"  Recovery failure rate:   "
                f"{data['recovery_failure_rate']:.2%}"
            )
        else:
            print("  Recovery failure rate:   N/A")

        if data["average_attempts_used"] is not None:
            print(
                f"  Average attempts used:   "
                f"{data['average_attempts_used']:.2f}"
            )

        if data["average_runtime_seconds"] is not None:
            print(
                f"  Average runtime:          "
                f"{data['average_runtime_seconds']:.3f}s"
            )

        print(
            f"  Final failure types:      "
            f"{data['failure_types']}"
        )

        print(
            f"  Attempt failure types:    "
            f"{data['attempt_failure_types']}"
        )

        print(
            f"  First-attempt failures:   "
            f"{data['first_attempt_failure_types']}"
        )
        print()

    print("=" * 70)
    print(f"JSON report: {OUTPUT_JSON}")
    print(f"CSV report:  {OUTPUT_CSV}")
    print("=" * 70)


if __name__ == "__main__":
    main()
