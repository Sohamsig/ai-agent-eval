# AgentReliability

A reproducible, task-based evaluation framework for measuring coding-agent reliability beyond final pass/fail results.

![Tests](https://github.com/Sohamsig/ai-agent-eval/actions/workflows/tests.yml/badge.svg)

AgentReliability evaluates software-engineering agents through isolated task workspaces, repeatable test execution, hidden-test verification, failure classification, recovery tracking, attempt-level logging, runtime measurement, and statistical reporting.

<img width="402" height="747" alt="image" src="https://github.com/user-attachments/assets/5c4433d6-079d-4b2e-abfd-6f43a5e3bacd" />

## 🎥 Project Demo

> A short demonstration of AgentReliability evaluating coding agents, detecting failures, tracking recovery, and generating reliability metrics.

[▶️ Watch AgentReliability Demo]()

## Why AgentReliability?

A coding agent that succeeds on its first attempt behaves differently from an agent that fails, performs recovery, and eventually succeeds.

Traditional pass/fail evaluation can hide this difference.

AgentReliability records the execution process so researchers can study:

* First-attempt success
* Eventual success
* Recovery behavior
* Failure modes
* Number of attempts
* Execution time
* Run-to-run consistency
* Agent-level differences

## Features

* Baseline and agent evaluation
* Multiple independent runs
* Isolated execution workspaces
* Docker-based test execution
* Hidden-test verification
* Attempt and recovery tracking
* Attempt-level logging
* CSV result generation
* Success-rate comparison
* Failure classification
* Duplicate-run detection
* Runtime measurement
* Pass@1 reporting
* Recovery success measurement
* Experiment IDs
* Local and Docker execution modes
* Wilson 95% confidence intervals
* Agent-level comparison
* Reproducible benchmark artifacts

## Tech Stack

* Python
* Pytest
* Docker
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

Run benchmark integrity tests:

```powershell
python -m pytest tests\test_benchmark_integrity.py -q
```

Run all task test suites:

```powershell
.\run_all_tests.ps1
```

## Final Controlled Evaluation

The final frozen experiment is:

```text
Experiment ID: task32-multiagent-docker-v1
Task:          task_32
Agents:        5
Runs/agent:    5
Final runs:    25
Attempt records: 30
Execution:     Docker
```

### Agents

* `baseline`
* `agent_02`
* `agent_03`
* `agent_04`
* `agent_05`

## Benchmark Results

| Agent      | Runs | Pass@1 | Final Success | Recovery Trigger | Recovery Success | Mean Attempts | Mean Runtime |
| ---------- | ---: | -----: | ------------: | ---------------: | ---------------: | ------------: | -----------: |
| `baseline` |    5 |   100% |          100% |               0% |              N/A |          1.00 |        1.41s |
| `agent_02` |    5 |   100% |          100% |               0% |              N/A |          1.00 |        1.50s |
| `agent_03` |    5 |   100% |          100% |               0% |              N/A |          1.00 |        1.34s |
| `agent_04` |    5 |     0% |          100% |             100% |             100% |          2.00 |        2.42s |
| `agent_05` |    5 |     0% |            0% |             100% |               0% |          1.00 |        1.06s |

### Key Observation

`agent_04` demonstrates why final success alone does not fully describe coding-agent behavior.

Across five runs:

* Pass@1: **0%**
* Final success: **100%**
* Recovery trigger: **100%**
* Recovery success: **100%**
* Mean attempts: **2.00**

Every successful run required recovery.

`agent_05` demonstrates a different failure mode:

* Pass@1: **0%**
* Final success: **0%**
* Recovery trigger: **100%**
* Recovery completed: **0%**
* Recovery error: **100%**

All five runs ended with `recovery_error`.

These results demonstrate the framework's ability to distinguish first-attempt success, eventual success, successful recovery, and recovery failure.

## Statistical Reporting

The framework reports Wilson score 95% confidence intervals for binary rates.

For observed rates of 100% with `n=5`:

```text
95% CI: 56.55% - 100.00%
```

For observed rates of 0% with `n=5`:

```text
95% CI: 0.00% - 43.45%
```

Because the final experiment contains only five runs per agent, these results are a controlled demonstration of the evaluation framework rather than a statistically generalizable ranking of coding agents.

## Evaluation Metrics

### Success Rate

The percentage of benchmark runs that eventually completed successfully.

### Generation Success Rate

The percentage of runs for which an agent successfully generated an initial candidate solution.

### Test Execution Rate

The percentage of runs for which the configured evaluation tests were executed successfully.

### Test Pass Rate

The percentage of benchmark runs whose executed tests passed.

### Pass@1

The percentage of runs whose first generated solution passed the evaluation tests without requiring recovery.

### Recovery Trigger Rate

The percentage of runs in which the recovery process was invoked after an initial failure.

### Recovery Completed Rate

The percentage of recovery-triggered runs that proceeded to a subsequent attempt.

### Recovery Error Rate

The percentage of recovery-triggered runs where recovery failed before a subsequent attempt could be completed.

### Recovery Success Rate

The percentage of completed recovery runs that eventually reached a successful final state.

### Average Attempts

The average number of attempts used per benchmark run.

### Runtime

The execution duration recorded for each benchmark run.

### Runtime Standard Deviation

The variation in execution time across independent runs.

### Failure Classification

The framework classifies failures including:

* `generation_failed`
* `test_failure`
* `recovery_not_implemented`
* `recovery_error`
* `syntax_error`
* `import_error`
* `assertion_failure`
* `type_error`
* `name_error`
* `attribute_error`
* `key_error`
* `index_error`
* `timeout`

### Duplicate Detection

The reporting pipeline detects repeated logical runs using stable run and experiment identifiers and compatibility checks for legacy task-agent-run combinations.

## Execution Isolation

The final controlled experiment uses Docker for benchmark test execution.

Docker execution uses an isolated workspace and disables network access for the benchmark test container.

The benchmark image is:

```text
agentreliability-test:latest
```

Hidden-test verification is performed as a separate verification stage. The current implementation therefore does **not** claim that hidden-test execution itself is Dockerized.

## Benchmark Integrity

The final benchmark passes the repository's benchmark-integrity tests:

```powershell
python -m pytest tests\test_benchmark_integrity.py -q
```

Verified result:

```text
6 passed
```

These checks help detect duplicate or inconsistent benchmark records.

## Generate Metrics

Generate the final metrics for the frozen experiment with:

```powershell
python -m evaluator.metrics --experiment-id task32-multiagent-docker-v1
```

The metrics report includes:

* Success rate
* Generation success rate
* Test execution rate
* Test pass rate
* Pass@1
* Recovery trigger rate
* Recovery completion rate
* Recovery error rate
* Recovery success rate
* Average attempts
* Runtime
* Runtime standard deviation
* Success variance
* Failure distributions
* Wilson 95% confidence intervals

## Generate the Benchmark Report

Generate the research-oriented report with:

```powershell
python -m evaluator.generate_report
```

The reporting layer provides:

* Benchmark-wide metrics
* Agent-level comparison
* Task-wise results
* Pass@1
* Recovery analysis
* Failure categories
* Hidden-test analysis
* Duplicate-run analysis
* Known limitations

## Benchmark Artifacts

Execution-aware benchmark artifacts are stored in the `results/` directory.

```text
results/
├── results_v2_execution.csv
└── attempts_v2_execution.csv
```

The final metrics output is stored at:

```text
metrics/task32-multiagent-final.txt
```

Additional historical artifacts may also exist in `results/`. Historical experiments are retained separately and should not be interpreted as equivalent to the final controlled experiment.

## Research Artifacts

The research documentation is stored in:

```text
research/
├── AgentReliability_Research_Paper.md
├── AgentReliability_Research_Paper.docx
├── AgentReliability_Research_Paper.pdf
└── README.md
```

The research paper documents:

* Evaluation methodology
* Experimental configuration
* Evaluation pipeline
* Metrics
* Statistical reporting
* Experimental results
* Recovery analysis
* Threats to validity
* Conclusion
* Future work
* Reproducibility artifacts

## Project Structure

```text
ai-agent-eval/

├── agents/
│   ├── agent_02.py
│   ├── agent_03.py
│   ├── agent_04.py
│   └── agent_05.py
│
├── evaluator/
│   ├── evaluate.py
│   ├── metrics.py
│   ├── generate_report.py
│   ├── reporting.py
│   ├── schemas.py
│   ├── statistical_utils.py
│   └── tests/
│
├── tasks/
│   ├── task_01/
│   ├── task_02/
│   ├── ...
│   └── task_33/
│
├── tests/
│   └── test_benchmark_integrity.py
│
├── results/
│   ├── results_v2.csv
│   ├── attempts_v2.csv
│   ├── results_v2_execution.csv
│   └── attempts_v2_execution.csv
│
├── metrics/
│   └── task32-multiagent-final.txt
│
├── research/
│   ├── AgentReliability_Research_Paper.md
│   ├── AgentReliability_Research_Paper.docx
│   ├── AgentReliability_Research_Paper.pdf
│   └── README.md
│
├── run_all_tests.ps1
├── requirements.txt
└── README.md
```

## Limitations

* The final controlled experiment contains only one task.
* Each agent has only five independent runs.
* The sample size is therefore too small for broad statistical generalization.
* Agent implementations are limited in diversity.
* Some agents in the controlled demonstration are deterministic or task-specific evaluation implementations rather than production LLM agents.
* Hidden-test coverage is limited to the available task fixtures.
* Hidden-test verification is currently a separate stage rather than a fully containerized stage.
* Runtime measurements depend on the local execution environment.
* Task difficulty is not yet calibrated across the complete task collection.
* The benchmark does not yet comprehensively measure code quality or maintainability.
* The current experiment should not be interpreted as a universal ranking of coding agents.

## Scientific Integrity

The benchmark is maintained with the following principles:

* Do not modify benchmark tasks to improve agent results.
* Preserve failed runs rather than silently removing them.
* Use unique experiment IDs for separate experiments.
* Keep historical experiments separate from the final controlled experiment.
* Distinguish generation failure, test failure, recovery error, and eventual success.
* Report uncertainty for small samples.
* Do not interpret controlled demonstration results as general agent rankings.

## Future Work

Planned extensions include:

* Recovery policies
* Improved attempt-level logging
* Framework-level tests
* Fully containerized hidden-test execution
* OpenAI agent adapter
* Claude agent adapter
* Gemini agent adapter
* Grok agent adapter
* Multi-agent experiments
* Larger multi-task benchmarks
* Larger statistical studies
* Cost-aware evaluation
* Recovery latency measurement
* Failure-transition analysis
* Reproducible public benchmark release

## License

This project can be released under the repository's selected open-source license.

## Author

**Soham Babrekar**

B.Tech Computer Science and Engineering, India
