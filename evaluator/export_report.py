from __future__ import annotations
import argparse, json
from pathlib import Path
from evaluator.reporting import PROJECT_ROOT, build_report, default_results_path, load_final_records
OUTPUT_FILE=PROJECT_ROOT/"results"/"benchmark_report_v2.json"
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--input',type=Path,default=default_results_path()); parser.add_argument('--output',type=Path,default=OUTPUT_FILE); args=parser.parse_args()
    report=build_report(load_final_records(args.input),args.input); args.output.write_text(json.dumps(report,indent=2),encoding='utf-8'); print(f'Report saved to: {args.output}')
if __name__=='__main__': main()
