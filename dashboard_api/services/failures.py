import pandas as pd
from .data_loader import load_results, load_attempts

def get_failure_distribution(experiment_id: str) -> list[dict]:
    results = [r for r in load_results() if r.get('experiment_id') == experiment_id]
    attempts = [a for a in load_attempts() if a.get('experiment_id') == experiment_id]
    
    failures = {}
    total_failures = 0
    
    for r in results:
        ft = r.get('failure_type')
        if ft and ft != 'None' and pd.notnull(ft):
            total_failures += 1
            if ft not in failures:
                failures[ft] = {'count': 0, 'agents': set(), 'tasks': set()}
            failures[ft]['count'] += 1
            failures[ft]['agents'].add(r.get('agent'))
            failures[ft]['tasks'].add(r.get('task_id'))
            
    for a in attempts:
        ft = a.get('failure_type')
        if ft and ft != 'None' and pd.notnull(ft):
            total_failures += 1
            if ft not in failures:
                failures[ft] = {'count': 0, 'agents': set(), 'tasks': set()}
            failures[ft]['count'] += 1
            failures[ft]['agents'].add(a.get('agent'))
            failures[ft]['tasks'].add(a.get('task_id'))
            
    out = []
    for ft, data in failures.items():
        out.append({
            'failure_type': ft,
            'count': data['count'],
            'percentage': data['count'] / total_failures if total_failures > 0 else 0.0,
            'affected_agents': list(data['agents']),
            'affected_tasks': list(data['tasks'])
        })
        
    return out
