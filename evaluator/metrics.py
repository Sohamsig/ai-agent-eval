from evaluator.reporting import default_results_path,load_final_records,summarize_records
def main():
    source=default_results_path(); summary=summarize_records(load_final_records(source)); d=summary['duplicates']; print(f"AI Coding Agent Evaluation Metrics\nSource CSV: {source}\nRaw rows: {d['raw_rows']}\nUnique logical runs: {d['logical_runs']}\nDuplicate groups: {d['duplicate_groups']}\nDuplicate rows: {d['duplicate_rows']}")
    for agent,data in summary['agents'].items(): print(f"{agent}: runs={data['unique_unambiguous_runs']}, success_rate={data['success_rate']}")
if __name__=='__main__': main()
