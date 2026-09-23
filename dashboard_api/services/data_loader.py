import pandas as pd
from pathlib import Path
import math

BASE_DIR = Path(__file__).parent.parent.parent
RESULTS_FILE = BASE_DIR / 'results' / 'results_v2_execution.csv'
ATTEMPTS_FILE = BASE_DIR / 'results' / 'attempts_v2_execution.csv'

_results_cache = None
_attempts_cache = None

def load_results() -> list[dict]:
    global _results_cache
    if _results_cache is None:
        if not RESULTS_FILE.exists():
            return []
        df = pd.read_csv(RESULTS_FILE)
        for col in ['generation_success', 'tests_executed', 'tests_passed', 'final_success', 'timed_out', 'recovery_attempted', 'recovery_success']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.lower().map({'true': True, 'false': False})
        
        df = df.where(pd.notnull(df), None)
        # handle nan floats
        for col in ['duration_seconds']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: None if (isinstance(x, float) and math.isnan(x)) else x)
        _results_cache = df.to_dict('records')
    return _results_cache

def load_attempts() -> list[dict]:
    global _attempts_cache
    if _attempts_cache is None:
        if not ATTEMPTS_FILE.exists():
            return []
        df = pd.read_csv(ATTEMPTS_FILE)
        for col in ['generation_success', 'tests_executed', 'tests_passed', 'timed_out']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.lower().map({'true': True, 'false': False})
        
        df = df.where(pd.notnull(df), None)
        # handle nan floats
        for col in ['duration_seconds']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: None if (isinstance(x, float) and math.isnan(x)) else x)
        _attempts_cache = df.to_dict('records')
    return _attempts_cache

def get_experiments() -> list[str]:
    results = load_results()
    if not results:
        return []
    return list(set(r.get('experiment_id') for r in results if r.get('experiment_id')))

def get_experiment_metadata(experiment_id: str) -> dict:
    results = [r for r in load_results() if r.get('experiment_id') == experiment_id]
    attempts = [a for a in load_attempts() if a.get('experiment_id') == experiment_id]
    
    tasks = list(set(r.get('task_id') for r in results if r.get('task_id')))
    agents = list(set(r.get('agent') for r in results if r.get('agent')))
    
    execution_mode = None
    if results:
        execution_mode = results[0].get('execution_mode')
        
    created_at = None
    if results:
        created_at = results[0].get('timestamp')
        
    return {
        'task_ids': tasks,
        'agents': agents,
        'run_count': len(results),
        'attempt_count': len(attempts),
        'execution_mode': execution_mode,
        'created_at': created_at
    }
