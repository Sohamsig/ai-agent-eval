from .data_loader import load_results, load_attempts

def list_runs(experiment_id: str, filters: dict = None) -> list[dict]:
    results = [r for r in load_results() if r.get('experiment_id') == experiment_id]
    
    if filters:
        for k, v in filters.items():
            if v is not None:
                if k == 'recovery_status':
                    continue
                results = [r for r in results if r.get(k) == v]
                
    attempts = [a for a in load_attempts() if a.get('experiment_id') == experiment_id]
    attempts_by_run = {}
    for a in attempts:
        rid = a.get('run_id')
        if rid not in attempts_by_run:
            attempts_by_run[rid] = []
        attempts_by_run[rid].append(a)
        
    out = []
    for r in results:
        rc = dict(r)
        rc['attempts'] = attempts_by_run.get(rc.get('run_id'), [])
        out.append(rc)
        
    return out

def get_run(experiment_id: str, run_id: str) -> dict:
    results = [r for r in load_results() if r.get('experiment_id') == experiment_id and r.get('run_id') == run_id]
    if not results:
        return None
    r = dict(results[0])
    attempts = [a for a in load_attempts() if a.get('experiment_id') == experiment_id and a.get('run_id') == run_id]
    r['attempts'] = attempts
    return r
