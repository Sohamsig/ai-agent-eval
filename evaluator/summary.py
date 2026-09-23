from __future__ import annotations

import argparse
import json
from pathlib import Path

from evaluator.reporting import PROJECT_ROOT


DEFAULT_REPORT = (
    PROJECT_ROOT
    / "results"
    / "benchmark_report_v2.json"
)

DEFAULT_SUMMARY = (
    PROJECT_ROOT
    / "results"
    / "benchmark_summary_v2.md"
)


def render_summary(report: dict) -> str:
    lines = [
        "# AI Coding Agent Evaluation Report",
        "",
        f"Generated: {report['generated_at']}",
        f"Source CSV: {report['source_csv']}",
        "",
        "## Data integrity",
        "",
        f"- Raw rows: {report['raw_rows']}",
        f"- Unique logical runs: "
        f"{report['unique_logical_runs']}",
        f"- Duplicate groups: "
        f"{report['duplicate_analysis']['duplicate_groups']}",
        f"- Duplicate rows: "
        f"{report['duplicate_analysis']['duplicate_rows']}",
        f"- Excluded ambiguous rows: "
        f"{report['excluded_ambiguous_rows']}",
        "",
        "## Outcomes",
        "",
        f"- Known outcomes: {report['known_outcomes']}",
        f"- Successful runs: {report['successful_runs']}",
        f"- Failed runs: {report['failed_runs']}",
        f"- Success rate: {report['success_rate']}%",
        "",
        "## Agents",
        "",
        "| Agent | Runs | Success rate | Pass@1 | "
        "Avg attempts | Recovery rate | Avg runtime (s) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for agent, data in sorted(report["agents"].items()):
        recovery_attempts = data["recovery_attempts"]
        recovery_successes = data["recovery_successes"]

        if recovery_attempts:
            recovery_rate = round(
                recovery_successes
                / recovery_attempts
                * 100,
                2,
            )
        else:
            recovery_rate = None

        recovery_display = (
            f"{recovery_rate}%"
            if recovery_rate is not None
            else "N/A"
        )

        lines.append(
            f"| {agent} "
            f"| {data['runs']} "
            f"| {data['success_rate']}% "
            f"| {data['pass_at_1']}% "
            f"| {data['average_attempts']} "
            f"| {recovery_display} "
            f"| {data['average_runtime_seconds']} |"
        )

    lines.extend(
        [
            "",
            "## Recovery analysis",
            "",
            f"- Recovery attempts: "
            f"{report['recovery_analysis']['total_recovery_attempts']}",
            f"- Successful recoveries: "
            f"{report['recovery_analysis']['successful_recoveries']}",
            f"- Recovery rate: "
            f"{report['recovery_analysis']['recovery_rate']}%"
            if report['recovery_analysis']['recovery_rate'] is not None
            else "- Recovery rate: N/A",
            f"- Average attempts: "
            f"{report['recovery_analysis']['average_attempts']}",
            "",
            "## Failure categories",
            "",
        ]
    )

    for category, count in report[
        "failure_categories"
    ].items():
        lines.append(f"- {category}: {count}")

    lines.extend(
        [
            "",
            "## Hidden-test analysis",
            "",
            f"- Hidden-test failures: "
            f"{report['hidden_test_analysis']['hidden_test_failures']}",
            f"- Hidden-test successes: "
            f"{report['hidden_test_analysis']['hidden_test_successes']}",
            f"- Hidden tests not executed: "
            f"{report['hidden_test_analysis']['hidden_test_not_executed']}",
            f"- Hidden-test observations: "
            f"{report['hidden_test_analysis']['hidden_test_observations']}",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT,
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_SUMMARY,
    )

    args = parser.parse_args()

    report = json.loads(
        args.report.read_text(
            encoding="utf-8"
        )
    )

    args.output.write_text(
        render_summary(report),
        encoding="utf-8",
    )

    print(
        f"Summary saved to: {args.output}"
    )


if __name__ == "__main__":
    main()




