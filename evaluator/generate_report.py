"""Generate a research-oriented benchmark report."""

import json
from pathlib import Path

from evaluator.reporting import (
    build_report,
    default_results_path,
    load_final_records,
)


def main() -> None:
    source = default_results_path()
    records = load_final_records(source)
    report = build_report(records, source)

    output_path = Path("results") / "benchmark_report_v2.json"

    output_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    benchmark = report["benchmark"]
    recovery = report["recovery_analysis"]
    pass_at_1 = report["pass_at_1"]

    print(f"Report generated: {output_path}")
    print(f"Source CSV: {source}")
    print(f"Raw rows: {benchmark['raw_rows']}")
    print(f"Unique logical runs: {benchmark['unique_logical_runs']}")
    print(
        "Duplicate groups: "
        f"{report['duplicate_analysis']['duplicate_groups']}"
    )
    print(f"Success rate: {benchmark['success_rate']}%")
    print(f"Pass@1: {pass_at_1['pass_at_1']}%")
    print(f"Average attempts: {recovery['average_attempts']}")
    print(
        "Average runtime: "
        f"{recovery['average_runtime_seconds']} seconds"
    )
    print(f"Failure categories: {report['failure_categories']}")
    print(
        "Hidden-test failures: "
        f"{report['hidden_test_analysis']['hidden_test_failures']}"
    )


if __name__ == "__main__":
    main()