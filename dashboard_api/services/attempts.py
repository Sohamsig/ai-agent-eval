from .data_loader import load_attempts

def list_attempts(experiment_id: str, run_id: str = None) -> list[dict]:
    attempts = [a for a in load_attempts() if a.get('experiment_id') == experiment_id]
    if run_id:
        attempts = [a for a in attempts if a.get('run_id') == run_id]
    return attempts
