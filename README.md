# AI Agent Evaluation Framework

A task-based evaluation framework for testing coding agents against visible tests and hidden tests.

![Tests](https://github.com/Sohamsig/ai-agent-eval/actions/workflows/tests.yml/badge.svg)

## Features

* Baseline and agent evaluation
* Multiple independent runs
* Hidden-test verification
* Attempt and recovery tracking
* CSV result generation
* Success-rate comparison
* Failure classification
* Duplicate-run detection
* Runtime measurement
* Pass@1 reporting

## Completed Evaluation

| Task      | Agent      | Runs | Success Rate |
| --------- | ---------- | ---: | -----------: |
| `task_32` | `baseline` |    5 |         100% |
| `task_32` | `agent_02` |    5 |         100% |

## Tech Stack

* Python
* Pytest
* CSV
* PowerShell
* Git

## Run Tests

Run the tests for a specific task:

```powershell
python -m pytest .\tasks\task_32 -q
```

Run evaluator tests:

```powershell
python -m pytest evaluator/tests -q
```

Run all task test suites:

```powershell
.\run_all_tests.ps1
```

## Benchmark Results

The current controlled evaluation contains **359 benchmark runs across 32 software-engineering tasks**.

| Metric                  | Result |
| ----------------------- | -----: |
| Tasks                   |     32 |
| Recorded benchmark rows |    359 |
| Unique logical runs     |    359 |
| Duplicate groups        |      0 |
| Successful runs         |    358 |
| Failed runs             |      1 |
| Overall success rate    | 99.72% |
| Pass@1                  | 99.72% |
| Hidden-test failures    |      0 |
| Recovery attempts       |      0 |

### Agent Results

| Agent      | Runs | Successful Runs | Failed Runs | Success Rate | Pass@1 |
| ---------- | ---: | --------------: | ----------: | -----------: | -----: |
| `baseline` |  165 |             165 |           0 |         100% |   100% |
| `agent_02` |  176 |             176 |           0 |         100% |   100% |
| `agent_03` |   18 |              17 |           1 |       94.44% | 94.44% |

### Recorded Failure

One controlled generation-failure experiment was recorded to verify failure classification.

| Field             | Value                       |
| ----------------- | --------------------------- |
| Task              | `task_27`                   |
| Agent             | `agent_03`                  |
| Failure type      | `generation_failed`         |
| Reason            | `Unsupported task: task_27` |
| Tests executed    | No                          |
| Recovery attempts | 0                           |

This failure is intentionally included as part of the Phase 4 controlled evaluation experiment.

## Evaluation Metrics

### Success Rate

The percentage of benchmark runs that completed successfully.

### Pass@1

The percentage of runs whose first generated solution passed the evaluation tests.

### Recovery Attempts

Additional attempts made after an initial generation or test failure.

### Average Attempts

The average number of attempts used per benchmark run.

### Runtime

The execution duration recorded for each benchmark run.

### Failure Classification

The framework classifies failures such as:

* `generation_failed`
* `test_failure`
* `recovery_not_implemented`
* Other configured failure categories

### Duplicate Detection

The reporting pipeline detects repeated logical runs using run identifiers and legacy task-agent-run keys.

## Benchmark Artifacts

Generated benchmark artifacts are stored in the `results/` directory.

* `results/results_v2.csv`
* `results/attempts_v2.csv`
* `results/benchmark_report_v2.json`
* `results/trajectory_task_27_agent_02_run_1.json`
* `results/trajectory_task_32_agent_02_run_1.json`
* `results/trajectory_task_32_agent_02_run_2.json`
* `results/trajectory_task_32_agent_02_run_3.json`

## Generate the Benchmark Report

Generate the latest research-oriented report with:

```powershell
python -m evaluator.generate_report
```

The command generates:

```text
results/benchmark_report_v2.json
```

The report includes:

* Benchmark-wide metrics
* Agent-level comparison
* Task-wise results
* Pass@1
* Recovery analysis
* Failure categories
* Hidden-test analysis
* Duplicate-run analysis
* Known limitations

## Project Structure

```text
ai-agent-eval/
├── evaluator/
│   ├── evaluate.py
│   ├── generate_report.py
│   ├── reporting.py
│   ├── schemas.py
│   └── tests/
├── tasks/
│   ├── task_01/
│   ├── task_02/
│   ├── ...
│   └── task_32/
├── results/
│   ├── results_v2.csv
│   ├── attempts_v2.csv
│   ├── benchmark_report_v2.json
│   └── trajectory_*.json
├── run_all_tests.ps1
├── requirements.txt
└── README.md
```

## Limitations

* The benchmark currently contains a limited number of tasks.
* Agent implementations are limited in diversity.
* Results apply only to the available benchmark dataset.
* A 100% result does not prove general coding-agent reliability.
* Task difficulty is not yet calibrated across all tasks.
* Hidden-test coverage is limited to the available task fixtures.
* Runtime measurements depend on the local execution environment.
* The benchmark does not yet measure code quality or maintainability.

## Important Note

The current results are based on a controlled local benchmark dataset. They should not be interpreted as a universal measure of coding-agent performance. Future work will expand task diversity, add recovery policies, improve attempt-level logging, and evaluate additional coding-agent adapters.
