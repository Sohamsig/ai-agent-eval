from pathlib import Path
from datetime import datetime

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS_FILE = ROOT / "results" / "results_v2.csv"
REPORT_FILE = ROOT / "reports" / "benchmark_report.md"


def percentage(value: float) -> str:
    return f"{value * 100:.2f}%"


def main() -> None:
    if not RESULTS_FILE.exists():
        raise FileNotFoundError(f"Results file not found: {RESULTS_FILE}")

    df = pd.read_csv(RESULTS_FILE)

    required_columns = {
        "task_id",
        "agent",
        "run_id",
        "final_success",
        "duration_seconds",
        "recovery_attempted",
        "recovery_success",
        "attempts_used",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["final_success"] = df["final_success"].astype(bool)
    df["recovery_attempted"] = df["recovery_attempted"].astype(bool)
    df["recovery_success"] = df["recovery_success"].astype(bool)

    total_runs = len(df)
    total_tasks = df["task_id"].nunique()
    total_agents = df["agent"].nunique()
    successful_runs = int(df["final_success"].sum())
    failed_runs = total_runs - successful_runs

    agent_summary = (
        df.groupby("agent")
        .agg(
            runs=("run_id", "count"),
            successful=("final_success", "sum"),
            average_duration=("duration_seconds", "mean"),
            recovery_attempts=("recovery_attempted", "sum"),
            recovery_successes=("recovery_success", "sum"),
            average_attempts=("attempts_used", "mean"),
        )
        .reset_index()
    )

    agent_summary["success_rate"] = (
        agent_summary["successful"] / agent_summary["runs"]
    )

    task_summary = (
        df.groupby(["task_id", "agent"])
        .agg(
            runs=("run_id", "count"),
            successful=("final_success", "sum"),
            average_duration=("duration_seconds", "mean"),
        )
        .reset_index()
    )

    task_summary["success_rate"] = (
        task_summary["successful"] / task_summary["runs"]
    )

    failure_summary = (
        df[~df["final_success"]]["failure_type"]
        .fillna("unknown")
        .value_counts()
    )

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = []

    report.append("# AI Agent Benchmark Evaluation Report")
    report.append("")
    report.append(f"> Generated: `{generated_at}`")
    report.append("")

    report.append("## Executive Summary")
    report.append("")
    report.append(f"- **Tasks evaluated:** {total_tasks}")
    report.append(f"- **Agents evaluated:** {total_agents}")
    report.append(f"- **Total runs:** {total_runs:,}")
    report.append(f"- **Successful runs:** {successful_runs:,}")
    report.append(f"- **Failed runs:** {failed_runs:,}")
    report.append(
        f"- **Overall success rate:** "
        f"{percentage(successful_runs / total_runs)}"
    )
    report.append("")

    report.append("## Agent Comparison")
    report.append("")
    report.append(
        "| Agent | Runs | Successful | Success Rate | "
        "Avg Duration (s) | Recovery Attempts | Avg Attempts |"
    )
    report.append(
        "|---|---:|---:|---:|---:|---:|---:|"
    )

    for row in agent_summary.itertuples(index=False):
        report.append(
            f"| {row.agent} | "
            f"{int(row.runs)} | "
            f"{int(row.successful)} | "
            f"{percentage(row.success_rate)} | "
            f"{row.average_duration:.4f} | "
            f"{int(row.recovery_attempts)} | "
            f"{row.average_attempts:.2f} |"
        )

    report.append("")

    report.append("## Task-wise Results")
    report.append("")
    report.append(
        "| Task | Agent | Runs | Successful | Success Rate | Avg Duration (s) |"
    )
    report.append(
        "|---|---|---:|---:|---:|---:|"
    )

    for row in task_summary.itertuples(index=False):
        report.append(
            f"| {row.task_id} | "
            f"{row.agent} | "
            f"{int(row.runs)} | "
            f"{int(row.successful)} | "
            f"{percentage(row.success_rate)} | "
            f"{row.average_duration:.4f} |"
        )

    report.append("")

    report.append("## Failure Analysis")
    report.append("")

    if failure_summary.empty:
        report.append("No failures were recorded.")
    else:
        report.append("| Failure Type | Count |")
        report.append("|---|---:|")
        for failure_type, count in failure_summary.items():
            report.append(f"| {failure_type} | {int(count)} |")

    report.append("")

    report.append("## Recovery Analysis")
    report.append("")
    report.append(
        f"- **Recovery attempts:** "
        f"{int(df['recovery_attempted'].sum())}"
    )
    report.append(
        f"- **Recovery successes:** "
        f"{int(df['recovery_success'].sum())}"
    )
    report.append(
        f"- **Average attempts used:** "
        f"{df['attempts_used'].mean():.2f}"
    )
    report.append("")

    report.append("## Interpretation")
    report.append("")
    report.append(
        "The benchmark measures agent reliability under the current "
        "task suite and execution configuration."
    )
    report.append("")
    report.append(
        "A 100% success rate indicates that all recorded runs passed "
        "the configured evaluation checks. It does not, by itself, "
        "prove that one agent produces better code than another."
    )
    report.append("")
    report.append(
        "Future improvements should include hidden tests, code-quality "
        "metrics, task difficulty labels, regression testing, and "
        "more challenging software-engineering tasks."
    )
    report.append("")

    REPORT_FILE.write_text("\n".join(report), encoding="utf-8")

    print("Benchmark report generated successfully.")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    main()