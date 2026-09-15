from __future__ import annotations
import argparse,json
from pathlib import Path
from evaluator.reporting import PROJECT_ROOT
DEFAULT_REPORT=PROJECT_ROOT/'results'/'benchmark_report_v2.json'; DEFAULT_SUMMARY=PROJECT_ROOT/'results'/'benchmark_summary_v2.md'
def render_summary(report):
    lines=['# AI Coding Agent Evaluation Report','',f"Generated: {report['generated_at']}",f"Source CSV: {report['source_csv']}",'','## Data integrity','',f"- Raw rows: {report['raw_rows']}",f"- Unique logical runs: {report['unique_logical_runs']}",f"- Duplicate groups: {report['duplicate_analysis']['duplicate_groups']}",f"- Duplicate rows: {report['duplicate_analysis']['duplicate_rows']}",f"- Excluded ambiguous rows: {report['excluded_ambiguous_rows']}",'','## Outcomes','',f"- Known outcomes: {report['known_outcomes']}",f"- Success rate among known, unambiguous outcomes: {report['success_rate']}",'','## Agents','','| Agent | Runs | Known outcomes | Success rate |','|---|---:|---:|---:|']
    for agent,data in sorted(report['agents'].items()): lines.append(f"| {agent} | {data['unique_unambiguous_runs']} | {data['known_outcomes']} | {data['success_rate']} |")
    return '\n'.join(lines)+'\n'
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--report',type=Path,default=DEFAULT_REPORT); parser.add_argument('--output',type=Path,default=DEFAULT_SUMMARY); args=parser.parse_args(); args.output.write_text(render_summary(json.loads(args.report.read_text(encoding='utf-8'))),encoding='utf-8'); print(f'Summary saved to: {args.output}')
if __name__=='__main__': main()
