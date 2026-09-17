from pathlib import Path
import json

from evaluator.reporting import (
    default_results_path,
    load_final_records,
    build_report,
)


def main():
    source = default_results_path()
    records = load_final_records(source)
    report = build_report(records, source)

    output_path = Path("results") / "benchmark_report_v2.json"
    output_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    benchmark = report.get("benchmark", report)

    print(f"Report generated: {output_path}")
    print(f"Source CSV: {source}")

    if "total_csv_rows" in benchmark:
        print(f"Raw rows: {benchmark['total_csv_rows']}")

    if "unique_benchmark_runs" in benchmark:
        print(
            f"Unique logical runs: "
            f"{benchmark['unique_benchmark_runs']}"
        )

    if "duplicate_groups" in report:
        print(
            f"Duplicate groups: "
            f"{report['duplicate_groups']}"
        )

    if "success_rate" in benchmark:
        print(f"Success rate: {benchmark['success_rate']}%")


if __name__ == "__main__":
    main()