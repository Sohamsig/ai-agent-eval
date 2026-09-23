import math
from .data_loader import load_results, load_attempts

def pstdev(data):
    n = len(data)
    if n == 0:
        return 0.0
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    return math.sqrt(variance)

def calculate_metrics(experiment_id: str) -> list[dict]:
    results = [r for r in load_results() if r.get('experiment_id') == experiment_id]
    attempts = [a for a in load_attempts() if a.get('experiment_id') == experiment_id]
    
    agents = list(set(r.get('agent') for r in results if r.get('agent')))
    metrics = []
    
    for agent in agents:
        agent_results = [r for r in results if r.get('agent') == agent]
        total_runs = len(agent_results)
        
        gen_success = sum(1 for r in agent_results if r.get('generation_success') is True)
        
        executed = [r for r in agent_results if r.get('tests_executed') is True]
        tests_passed = sum(1 for r in executed if r.get('tests_passed') is True)
        
        agent_attempts = [a for a in attempts if a.get('agent') == agent]
        first_attempts = [a for a in agent_attempts if a.get('attempt_number') == 1]
        pass_at_1 = sum(1 for a in first_attempts if a.get('tests_passed') is True)
        
        final_success = sum(1 for r in agent_results if r.get('final_success') is True)
        
        recovery_triggered = [r for r in agent_results if r.get('recovery_attempted') is True]
        recovery_completed = [r for r in recovery_triggered if (r.get('attempts_used') or 0) > 1]
        recovery_success = sum(1 for r in recovery_completed if r.get('recovery_success') is True)
        recovery_error = len(recovery_completed) - recovery_success
        
        attempts_used_list = [r.get('attempts_used') for r in agent_results if r.get('attempts_used') is not None]
        avg_attempts = sum(attempts_used_list) / len(attempts_used_list) if attempts_used_list else 0.0
        
        runtimes = [r.get('duration_seconds') for r in agent_results if r.get('duration_seconds') is not None]
        runtimes = [r for r in runtimes if not math.isnan(r)] if runtimes else []
        avg_runtime = sum(runtimes) / len(runtimes) if runtimes else 0.0
        rt_stddev = pstdev(runtimes)
        
        metrics.append({
            'agent': agent,
            'runs': total_runs,
            'generation_success_rate': (gen_success / total_runs) if total_runs else 0.0,
            'test_pass_rate': (tests_passed / len(executed)) if executed else 0.0,
            'pass_at_1': (pass_at_1 / len(first_attempts)) if first_attempts else 0.0,
            'final_success_rate': (final_success / total_runs) if total_runs else 0.0,
            'recovery_trigger_rate': (len(recovery_triggered) / total_runs) if total_runs else 0.0,
            'recovery_completed_rate': (len(recovery_completed) / len(recovery_triggered)) if recovery_triggered else 0.0,
            'recovery_success_rate': (recovery_success / len(recovery_completed)) if recovery_completed else 0.0,
            'recovery_error_rate': (recovery_error / len(recovery_completed)) if recovery_completed else 0.0,
            'average_attempts': avg_attempts,
            'average_runtime': avg_runtime,
            'runtime_stddev': rt_stddev,
            'runtimes': runtimes
        })
        
    return metrics
