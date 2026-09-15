from evaluator.reporting import default_results_path,load_final_records,summarize_records
def compare_agents():
    source=default_results_path(); summary=summarize_records(load_final_records(source)); print(f'AI Coding Agent Comparison\nSource CSV: {source}')
    for agent,data in summary['agents'].items(): print(f"{agent}: runs={data['unique_unambiguous_runs']}, known_outcomes={data['known_outcomes']}, success_rate={data['success_rate']}")
    return summary
if __name__=='__main__': compare_agents()
