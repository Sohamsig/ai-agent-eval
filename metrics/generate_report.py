from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
METRICS_FILE = ROOT / "results" / "benchmark_metrics.json"
OUTPUT_FILE = ROOT / "results" / "benchmark_report.md"


def pct(value):
    if value is None:
        return "N/A"
    return f"{value:.1%}"


def num(value):
    if value is None:
        return "N/A"
    return f"{value:.3f}"


def main():
    if not METRICS_FILE.exists():
        raise FileNotFoundError(
            f"Missing metrics file: {METRICS_FILE}"
        )

    with METRICS_FILE.open("r", encoding="utf-8") as f:
        metrics = json.load(f)

    benchmark = metrics["benchmark"]
    agents = metrics["agents"]

    total_runs = benchmark["total_runs"]
    total_attempts = benchmark["total_attempts"]

    eventual_successes = sum(
        data["eventual_successes"]
        for data in agents.values()
    )

    first_attempt_successes = sum(
        data["first_attempt_successes"]
        for data in agents.values()
    )

    recovery_attempts = sum(
        data["recovery_attempts"]
        for data in agents.values()
    )

    recovery_successes = sum(
        data["recovery_successes"]
        for data in agents.values()
    )

    recovery_failures = sum(
        data["recovery_failures"]
        for data in agents.values()
    )

    report = []

    report.append("# AgentReliability Benchmark Report")
    report.append("")
    report.append(
        "> A reproducible evaluation framework for measuring "
        "coding-agent reliability beyond final pass/fail results."
    )
    report.append("")

    report.append("## Benchmark Overview")
    report.append("")
    report.append("| Metric | Value |")
    report.append("|---|---:|")
    report.append(f"| Agents | {benchmark['agents']} |")
    report.append(f"| Total runs | {total_runs} |")
    report.append(f"| Total attempts | {total_attempts} |")
    report.append(
        f"| First-attempt successes | "
        f"{first_attempt_successes}/{total_runs} "
        f"({first_attempt_successes / total_runs:.1%}) |"
    )
    report.append(
        f"| Eventual successes | "
        f"{eventual_successes}/{total_runs} "
        f"({eventual_successes / total_runs:.1%}) |"
    )
    report.append(
        f"| Recovery-triggered runs | "
        f"{recovery_attempts}/{total_runs} "
        f"({recovery_attempts / total_runs:.1%}) |"
    )
    report.append(
        f"| Successful recoveries | "
        f"{recovery_successes}/{recovery_attempts} "
        f"({recovery_successes / recovery_attempts:.1%}) |"
        if recovery_attempts
        else "| Successful recoveries | N/A |"
    )
    report.append(
        f"| Recovery failures | "
        f"{recovery_failures}/{recovery_attempts} "
        f"({recovery_failures / recovery_attempts:.1%}) |"
        if recovery_attempts
        else "| Recovery failures | N/A |"
    )
    report.append("")

    report.append("## Agent Metrics")
    report.append("")
    report.append(
        "| Agent | Runs | Pass@1 | Eventual Success | "
        "Recovery Attempt | Recovery Success | Avg Attempts | Avg Runtime |"
    )
    report.append(
        "|---|---:|---:|---:|---:|---:|---:|---:|"
    )

    for agent, data in agents.items():
        report.append(
            f"| {agent} "
            f"| {data['runs']} "
            f"| {pct(data['pass_at_1'])} "
            f"| {pct(data['eventual_success_rate'])} "
            f"| {pct(data['recovery_attempt_rate'])} "
            f"| {pct(data['recovery_success_rate'])} "
            f"| {data['average_attempts_used']:.2f} "
            f"| {num(data['average_runtime_seconds'])}s |"
        )

    report.append("")

    report.append("## Execution Failure Analysis")
    report.append("")

    for agent, data in agents.items():
        report.append(f"### {agent}")
        report.append("")

        report.append(
            f"- Final failure types: "
            f"`{data['failure_types']}`"
        )

        report.append(
            f"- Attempt failure types: "
            f"`{data['attempt_failure_types']}`"
        )

        report.append(
            f"- First-attempt failures: "
            f"`{data['first_attempt_failure_types']}`"
        )

        report.append(
            f"- First-attempt successes: "
            f"{data['first_attempt_successes']}"
        )

        report.append(
            f"- Eventual successes: "
            f"{data['eventual_successes']}"
        )

        report.append(
            f"- Recovery attempts: "
            f"{data['recovery_attempts']}"
        )

        report.append(
            f"- Successful recoveries: "
            f"{data['recovery_successes']}"
        )

        report.append(
            f"- Recovery failures: "
            f"{data['recovery_failures']}"
        )

        report.append("")

    report.append("## Interpretation")
    report.append("")
    report.append(
        "The benchmark demonstrates why final pass/fail alone can "
        "hide differences in agent execution behavior."
    )
    report.append("")
    report.append(
        "Agent 04 reaches successful final outcomes after recovery, "
        "while Agent 05 encounters recovery errors after its initial "
        "test failure. These execution paths are represented separately "
        "from the final outcome."
    )
    report.append("")
    report.append(
        "Pass@1 measures success on the first attempt. "
        "Eventual success measures whether the run ultimately succeeds "
        "after allowed recovery attempts."
    )
    report.append("")

    report.append("## Reproducibility")
    report.append("")
    report.append(
        "Results are generated from the versioned CSV outputs produced "
        "by the AgentReliability evaluator."
    )
    report.append("")
    report.append(
        "Source files:"
    )
    report.append("")
    report.append("- `results_v2.csv`")
    report.append("- `attempts_v2.csv`")
    report.append("- `benchmark_metrics.json`")
    report.append("- `benchmark_metrics.csv`")
    report.append("")

    OUTPUT_FILE.write_text(
        "\n".join(report) + "\n",
        encoding="utf-8"
    )

    print("=" * 70)
    print("BENCHMARK REPORT GENERATED")
    print("=" * 70)
    print(f"Report: {OUTPUT_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()
