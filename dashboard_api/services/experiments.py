from .data_loader import get_experiments, get_experiment_metadata

def list_experiments() -> list[dict]:
    exp_ids = get_experiments()
    out = []
    for eid in exp_ids:
        meta = get_experiment_metadata(eid)
        out.append({
            'experiment_id': eid,
            'task_count': len(meta['task_ids']),
            'agent_count': len(meta['agents']),
            'run_count': meta['run_count'],
            'created_at': meta['created_at']
        })
    return out

def get_experiment_summary(experiment_id: str) -> dict:
    meta = get_experiment_metadata(experiment_id)
    if meta['run_count'] == 0:
        return None
        
    return {
        'experiment_id': experiment_id,
        'total_runs': meta['run_count'],
        'attempt_records': meta['attempt_count'],
        'agents': len(meta['agents']),
        'tasks': meta['task_ids'],
        'agent_list': meta['agents'],
        'execution_mode': meta['execution_mode'],
        'hidden_test_verification': meta['execution_mode'] == 'docker',
        'confidence_interval': 'Wilson 95%'
    }
