# AI Agent Evaluation Framework

A task-based evaluation framework for testing coding agents against
visible tests and hidden tests.

## Features

- Baseline and agent evaluation
- Multiple independent runs
- Hidden-test verification
- Attempt and recovery tracking
- CSV result generation
- Success-rate comparison
- Failure classification

## Completed Evaluation

| Task | Agent | Runs | Success Rate |
|------|-------|------|--------------|
| task_32 | baseline | 5 | 100% |
| task_32 | agent_02 | 5 | 100% |

## Tech Stack

- Python
- Pytest
- CSV
- PowerShell
- Git

## Run Tests

```powershell
python -m pytest .\tasks\task_32 -q

## Agent Benchmark Results

The benchmark evaluated two agents across 32 tasks, with 5 runs per agent.

| Metric | Baseline | Agent 02 |
|---|---:|---:|
| Total tasks | 32 | 32 |
| Total evaluations | 160 | 160 |
| Success rate | 100% | 100% |
| Average execution time | 1.064 seconds | 1.107 seconds |
| Faster tasks | 17 | 15 |

### Summary

- Both agents achieved a 100% success rate.
- Baseline was faster on 17 tasks.
- Agent 02 was faster on 15 tasks.
- Baseline average execution time: 1.064 seconds.
- Agent 02 average execution time: 1.107 seconds.

### Benchmark Artifacts

- `results/agent_speed_comparison.csv`
- `results/final_benchmark_summary.csv`
- `results/benchmark_chart.png`
- `results/plot_benchmark.py`
- `results/benchmark_summary.md`
- `results/benchmark_report.json`
- `results/FINAL_BENCHMARK_REPORT.md`