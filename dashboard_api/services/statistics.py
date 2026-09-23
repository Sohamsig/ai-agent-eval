import math

def wilson_interval(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return 0.0, 0.0
        
    p = successes / n
    denominator = 1 + z**2 / n
    center_adjusted_probability = p + z**2 / (2 * n)
    adjusted_standard_deviation = z * math.sqrt((p * (1 - p) + z**2 / (4 * n)) / n)
    
    lower_bound = (center_adjusted_probability - adjusted_standard_deviation) / denominator
    upper_bound = (center_adjusted_probability + adjusted_standard_deviation) / denominator
    
    return max(0.0, lower_bound), min(1.0, upper_bound)

def get_statistics(experiment_id: str) -> list[dict]:
    from .data_loader import load_results, load_attempts
    
    results = [r for r in load_results() if r.get('experiment_id') == experiment_id]
    attempts = [a for a in load_attempts() if a.get('experiment_id') == experiment_id]
    
    agents = list(set(r.get('agent') for r in results if r.get('agent')))
    
    stats = []
    
    for agent in agents:
        agent_results = [r for r in results if r.get('agent') == agent]
        n_runs = len(agent_results)
        
        # final_success_rate
        final_successes = sum(1 for r in agent_results if r.get('final_success') is True)
        lower, upper = wilson_interval(final_successes, n_runs)
        rate = final_successes / n_runs if n_runs > 0 else 0.0
        stats.append({
            'metric': 'final_success_rate', 'agent': agent, 'rate': rate,
            'successes': final_successes, 'n': n_runs, 'ci_lower': lower, 'ci_upper': upper
        })
        
        # pass_at_1
        agent_first_attempts = [a for a in attempts if a.get('agent') == agent and a.get('attempt_number') == 1]
        n_first_attempts = len(agent_first_attempts)
        pass_at_1_successes = sum(1 for a in agent_first_attempts if a.get('tests_passed') is True)
        lower, upper = wilson_interval(pass_at_1_successes, n_first_attempts)
        rate = pass_at_1_successes / n_first_attempts if n_first_attempts > 0 else 0.0
        stats.append({
            'metric': 'pass_at_1', 'agent': agent, 'rate': rate,
            'successes': pass_at_1_successes, 'n': n_first_attempts, 'ci_lower': lower, 'ci_upper': upper
        })
        
        # recovery_trigger_rate
        recovery_triggers = sum(1 for r in agent_results if r.get('recovery_attempted') is True)
        lower, upper = wilson_interval(recovery_triggers, n_runs)
        rate = recovery_triggers / n_runs if n_runs > 0 else 0.0
        stats.append({
            'metric': 'recovery_trigger_rate', 'agent': agent, 'rate': rate,
            'successes': recovery_triggers, 'n': n_runs, 'ci_lower': lower, 'ci_upper': upper
        })
        
        # recovery_success_rate
        completed_recovery_runs = [r for r in agent_results if r.get('recovery_attempted') is True and (r.get('attempts_used') or 0) > 1]
        n_recovery = len(completed_recovery_runs)
        recovery_successes = sum(1 for r in completed_recovery_runs if r.get('recovery_success') is True)
        lower, upper = wilson_interval(recovery_successes, n_recovery)
        rate = recovery_successes / n_recovery if n_recovery > 0 else 0.0
        stats.append({
            'metric': 'recovery_success_rate', 'agent': agent, 'rate': rate,
            'successes': recovery_successes, 'n': n_recovery, 'ci_lower': lower, 'ci_upper': upper
        })
        
    return stats
