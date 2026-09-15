from collections import defaultdict
from evaluator.reporting import as_bool,default_results_path,load_final_records,summarize_records
def generate_task_summary():
    source=default_results_path(); summary=summarize_records(load_final_records(source)); tasks=defaultdict(list)
    for row in summary['usable_records']: tasks[row.get('task_id')].append(row)
    print(f"AI Coding Agent Task Summary\nSource CSV: {source}\nDuplicate groups excluded: {summary['duplicates']['duplicate_groups']}")
    for task,rows in sorted(tasks.items(),key=lambda item:str(item[0])):
        known=[as_bool(row.get('final_success')) for row in rows]; known=[x for x in known if x is not None]; rate=round(sum(x is True for x in known)/len(known)*100,2) if known else None; print(f'{task}: runs={len(rows)}, success_rate={rate}')
    return tasks
if __name__=='__main__': generate_task_summary()
