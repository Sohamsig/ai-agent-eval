# AgentReliability: A Reproducible Framework for Measuring Coding-Agent Reliability Beyond Final Pass/Fail Results

**Soham Babrekar**
B.Tech Computer Science and Engineering
India

---

# ABSTRACT

Coding agents based on large language models are increasingly capable of generating, modifying, testing, and debugging software. As these systems become more autonomous, evaluating them only by whether they eventually pass a test suite provides an incomplete picture of their behavior. Two agents may both achieve a successful final result while following substantially different execution trajectories: one may succeed on its first attempt, while another may initially fail, diagnose the failure, perform a repair, and succeed on a later attempt.

This work presents **AgentReliability**, a reproducible evaluation framework designed to measure coding-agent reliability beyond final pass/fail outcomes. The framework records generation outcomes, test execution, failure classifications, recovery behavior, attempts, runtime, and final task outcomes. It supports isolated execution workspaces, Docker-based test execution, hidden-test verification, attempt-level logging, recovery tracking, duplicate-run detection, experiment identifiers, and statistical reporting.

A controlled experiment was conducted using `task_32`, five evaluation agents, and five independent runs per agent, resulting in **25 evaluation runs**. The experiment measured Pass@1, eventual success, recovery behavior, attempts used, runtime, and Wilson 95% confidence intervals.

The results demonstrate that final success alone can conceal important differences in agent behavior. **Agent 04 achieved 0% Pass@1 but 100% eventual success**, successfully recovering from an initial failure in all five runs. **Agent 05 also achieved 0% Pass@1, but recovery failed in all five runs, resulting in 0% eventual success.** In contrast, the baseline, Agent 02, and Agent 03 achieved 100% Pass@1 and 100% eventual success.

These results demonstrate that coding-agent reliability is multidimensional. First-attempt correctness, eventual success, recovery behavior, failure type, number of attempts, and execution cost provide information that cannot be represented by a single final pass/fail value. AgentReliability therefore provides a more detailed and reproducible representation of coding-agent execution behavior.

---

# 1. INTRODUCTION

## 1.1 Background

Large language models have significantly increased the capabilities of automated software development systems. Modern coding agents can interpret natural-language requirements, inspect source code, generate modifications, execute tests, diagnose failures, and attempt repairs.

Benchmarks such as SWE-bench demonstrate the importance of evaluating language models in realistic software-engineering environments rather than only on isolated code-generation problems. SWE-bench evaluates models on real GitHub issues that require modifications to existing software repositories and therefore introduces execution, repository understanding, and debugging into the evaluation process.

Earlier code-generation evaluation has also used functional correctness and repeated sampling as important evaluation concepts. The Codex evaluation work introduced HumanEval and investigated repeated sampling for measuring code-generation performance.

However, a final binary result does not fully describe the execution trajectory of an autonomous coding agent.

Consider two agents:

* Agent A generates a correct solution immediately.
* Agent B generates an incorrect solution, runs tests, analyzes the failure, repairs the implementation, and eventually succeeds.

If both agents are recorded only as `PASS`, their behaviors appear identical even though their execution processes are substantially different.

This motivates a more detailed evaluation approach that records not only the final state but also the path taken to reach that state.

---

## 1.2 Problem Statement

Traditional coding-agent evaluation commonly emphasizes whether a generated solution eventually passes a predefined test suite.

Although this provides an important measure of functional correctness, it does not directly capture:

* whether the first generated solution was correct;
* how many attempts were required;
* whether the agent recovered from a failure;
* whether recovery was successful;
* what type of failure occurred;
* whether recovery itself produced another failure;
* how much execution time was required;
* and whether the observed behavior is consistent across independent runs.

Therefore, the research problem addressed by this work is:

**How can coding-agent evaluation capture first-attempt performance, recovery behavior, failure modes, execution cost, and eventual success in a reproducible manner rather than representing an agent using only a final pass/fail result?**

AgentReliability addresses this problem by treating an agent execution as a sequence of measurable attempts rather than as a single binary outcome.

---

## 1.3 Motivation

The primary motivation for AgentReliability is to make coding-agent evaluation more informative and reproducible.

A final successful result can represent multiple execution trajectories. For example, an agent may:

1. generate a correct solution immediately;
2. generate an incorrect solution and recover successfully;
3. generate an incorrect solution and fail during recovery;
4. repeatedly attempt repairs without reaching a valid solution.

These behaviors have different reliability characteristics even when some of them produce the same final result.

AgentReliability therefore records the execution process, including initial generation, test execution, failure classification, recovery attempts, subsequent test execution, final outcome, number of attempts, and runtime.

This enables researchers to study coding agents as interactive systems rather than only as one-shot code generators.

---

## 1.4 Research Questions

This study investigates the following research questions:

**RQ1. Does final task success adequately characterize coding-agent reliability?**

**RQ2. Can recovery-aware evaluation distinguish different failure and recovery trajectories?**

**RQ3. What additional measurements provide useful information beyond final pass/fail results?**

The experiment is designed as an initial controlled demonstration of these questions rather than as a general ranking of coding agents.

---

# 2. RESEARCH METHODOLOGY

## 2.1 Evaluation Objective

The objective of AgentReliability is to measure the complete execution trajectory of a coding agent.

For each evaluation run, the framework records:

* solution-generation outcome;
* test execution;
* test results;
* failure classification;
* recovery trigger;
* recovery completion;
* recovery success;
* number of attempts;
* execution duration;
* final task outcome.

This allows the framework to distinguish between first-attempt success and eventual success.

The evaluation therefore treats reliability as a collection of related measurements rather than a single score.

---

## 2.2 Evaluation Pipeline

The AgentReliability evaluation pipeline consists of the following stages:

### Step 1: Task Selection

A benchmark task is selected with its task description, source files, tests, and execution configuration.

### Step 2: Workspace Creation

An isolated workspace is created for the evaluation run. The agent operates within this workspace.

### Step 3: Initial Solution Generation

The selected agent receives the task context and generates an initial candidate solution.

### Step 4: Test Execution

The generated solution is executed against the configured visible test suite.

### Step 5: Result Recording

The framework records test outcomes, execution duration, failure information, and other run-level information.

### Step 6: Failure Classification

If the initial execution fails, the framework classifies the failure using categories such as:

* syntax error;
* import error;
* assertion failure;
* type error;
* name error;
* attribute error;
* key error;
* index error;
* timeout;
* recovery error;
* test failure.

### Step 7: Recovery

When recovery is supported by the agent, the framework provides the failure context to the recovery mechanism.

The recovery process may inspect the previous solution, test output, failure classification, task description, and relevant source/test files.

### Step 8: Retesting

The repaired solution is tested again.

The process continues until the task succeeds or the configured maximum number of attempts is reached.

### Step 9: Hidden-Test Verification

After the visible test stage succeeds, a separate hidden-test verification stage is used to provide additional correctness verification.

### Step 10: Result Storage

The framework stores both run-level and attempt-level records in CSV format.

### Step 11: Statistical Analysis

The recorded results are aggregated by agent and experiment to calculate success rates, Pass@1, recovery metrics, attempts, runtime, failure distributions, and confidence intervals.

---

## 2.3 Execution Isolation

The experiment used Docker-based test execution to improve reproducibility and reduce environmental differences between evaluation runs.

The Docker execution environment provides an isolated filesystem and process environment. Docker containers also support network isolation; the `none` network mode completely isolates the container's networking stack.

For the reported experiment, test execution used Docker with network access disabled.

The evaluation should therefore be understood as:

**Agent generation → isolated workspace → Docker test execution → result recording → recovery → retesting → hidden verification**

The hidden-test verification stage remained a separate host-side verification stage rather than being described as Dockerized.

---

## 2.4 Experimental Configuration

The primary experiment was identified as:

**Experiment ID:** `task32-multiagent-docker-v1`

The configuration was:

| Configuration        | Value                                            |
| -------------------- | ------------------------------------------------ |
| Benchmark task       | `task_32`                                        |
| Agents               | Baseline, Agent 02, Agent 03, Agent 04, Agent 05 |
| Runs per agent       | 5                                                |
| Total runs           | 25                                               |
| Maximum attempts     | 3                                                |
| Test execution       | Docker                                           |
| Hidden verification  | Enabled                                          |
| Execution mode       | Isolated                                         |
| Statistical interval | Wilson 95% CI                                    |

Each agent therefore received five independent evaluation runs under the same task configuration.

---

## 2.5 Recorded Data

AgentReliability records data at two levels.

### Run-Level Data

Run-level records include:

* schema version;
* timestamp;
* run ID;
* experiment ID;
* execution mode;
* task ID;
* agent;
* run number;
* generation success;
* tests executed;
* tests passed;
* test counts;
* final success;
* failure type;
* error message;
* exit code;
* timeout status;
* standard output;
* standard error;
* recovery status;
* attempts used;
* maximum attempts;
* duration.

### Attempt-Level Data

Attempt-level records include:

* attempt ID;
* task ID;
* agent;
* run number;
* attempt number;
* generation status;
* test execution;
* test results;
* failure classification;
* error information;
* execution duration.

Separating run-level and attempt-level information makes it possible to reconstruct an agent's execution trajectory.

---

## 2.6 Evaluation Metrics

AgentReliability calculates several metrics.

### Pass@1

Pass@1 measures the percentage of runs in which the agent succeeds on its first attempt.

$$
Pass@1 = \frac{\text{First-attempt successful runs}}{\text{Total runs}} \times 100
$$

### Eventual Success Rate

Eventual success measures the percentage of runs that eventually succeed within the allowed attempts.

$$
EventualSuccess =
\frac{\text{Runs eventually successful}}
{\text{Total runs}}
\times 100
$$

### Recovery Trigger Rate

Recovery Trigger Rate measures how frequently a run requires recovery after an initial failure.

### Recovery Completed Rate

Recovery Completed Rate measures the proportion of recovery-triggered runs that proceed to another evaluation attempt.

### Recovery Success Rate

Recovery Success Rate measures the proportion of completed recovery trajectories that ultimately succeed.

### Mean Attempts

Mean Attempts measures the average number of evaluation attempts required per run.

### Runtime

Runtime measures the execution duration of evaluation runs.

### Failure Distribution

Failure classification records the types of failures observed during evaluation.

These metrics allow a final success result to be interpreted together with the trajectory that produced it.

---

## 2.7 Statistical Reporting

Because each agent was evaluated only five times, percentages alone are insufficient to communicate the uncertainty of the observed rates.

AgentReliability therefore reports **95% Wilson score confidence intervals** for binary rates.

The Wilson interval is particularly useful for binomial proportions with small sample sizes and avoids some limitations of the simple normal approximation.

For this experiment, rates of 100% across five observations produced a Wilson 95% confidence interval of:

**56.55%–100.00%**

Rates of 0% produced:

**0.00%–43.45%**

These intervals should not be interpreted as evidence that the agents have stable population-level success rates. Instead, they communicate the uncertainty associated with this small controlled experiment.

---

# 3. EXPERIMENTAL RESULTS

## 3.1 Experimental Overview

The experiment consisted of 25 independent runs of `task_32`.

Five agents were evaluated:

* Baseline
* Agent 02
* Agent 03
* Agent 04
* Agent 05

Each agent was evaluated five times.

All agents achieved successful solution generation in the reported experiment. However, their subsequent execution trajectories differed substantially.

---

## 3.2 Overall Results

| Agent    | Runs | Pass@1 | Final Success | Recovery Trigger | Recovery Success | Mean Attempts | Mean Runtime |
| -------- | ---: | -----: | ------------: | ---------------: | ---------------: | ------------: | -----------: |
| Baseline |    5 |   100% |          100% |               0% |              N/A |          1.00 |       1.41 s |
| Agent 02 |    5 |   100% |          100% |               0% |              N/A |          1.00 |       1.50 s |
| Agent 03 |    5 |   100% |          100% |               0% |              N/A |          1.00 |       1.34 s |
| Agent 04 |    5 |     0% |          100% |             100% |             100% |          2.00 |       2.42 s |
| Agent 05 |    5 |     0% |            0% |             100% |               0% |          1.00 |       1.06 s |

All five agents achieved a generation success rate of 100% in this experiment.

The results show that generation success alone does not indicate whether the generated solution will pass tests or recover from failure.

---

## 3.3 Pass@1 and Eventual Success

The most significant difference appears when Pass@1 is compared with final success.

The baseline, Agent 02, and Agent 03 achieved:

* 100% Pass@1;
* 100% final success;
* one attempt on average;
* no recovery requirement.

Agent 04 achieved:

* 0% Pass@1;
* 100% final success;
* 100% recovery triggering;
* 100% recovery success;
* 2.00 mean attempts.

Therefore, Agent 04 provides a clear example where **eventual success alone would hide the fact that the initial solution failed in every run**.

If the evaluation reported only final success, the baseline and Agent 04 would both appear as 100% successful.

However, Pass@1 and attempts reveal substantially different execution trajectories.

Agent 05 provides another trajectory:

* 0% Pass@1;
* 0% final success;
* 100% recovery trigger;
* 100% recovery error.

Thus, the framework distinguishes initial failure followed by successful recovery from initial failure followed by unsuccessful recovery.

---

## 3.4 Recovery Behavior

Recovery behavior is one of the central measurements provided by AgentReliability.

### Agent 04

Agent 04 triggered recovery in all five runs.

The recovery process completed successfully in all five runs, producing:

* Recovery Trigger Rate: 100%
* Recovery Completed Rate: 100%
* Recovery Success Rate: 100%
* Mean Attempts: 2.00

This indicates that the agent did not succeed on its initial attempt but was able to recover within the configured evaluation process.

### Agent 05

Agent 05 also triggered recovery in all five runs.

However, the recovery process encountered an error before a second successful evaluation attempt could be completed.

The resulting measurements were:

* Recovery Trigger Rate: 100%
* Recovery Completed Rate: 0%
* Recovery Error Rate: 100%
* Recovery Success Rate: 0%
* Final Success: 0%

The distinction between Agent 04 and Agent 05 demonstrates why recovery behavior should be recorded separately from final success.

---

## 3.5 Statistical Results

The experiment contained five observations per agent.

For rates of 100%, the reported Wilson 95% confidence interval was:

**56.55%–100.00%**

For rates of 0%, the interval was:

**0.00%–43.45%**

The statistical results were:

| Agent    | Success Rate |     95% CI | Pass@1 |     95% CI |
| -------- | -----------: | ---------: | -----: | ---------: |
| Agent 02 |         100% | 56.55–100% |   100% | 56.55–100% |
| Agent 03 |         100% | 56.55–100% |   100% | 56.55–100% |
| Agent 04 |         100% | 56.55–100% |     0% |   0–43.45% |
| Agent 05 |           0% |   0–43.45% |     0% |   0–43.45% |
| Baseline |         100% | 56.55–100% |   100% | 56.55–100% |

Agent 04's recovery success rate was also 100%, with a Wilson 95% confidence interval of 56.55%–100%.

The intervals demonstrate the uncertainty caused by the small number of experimental runs.

---

## 3.6 Runtime

Runtime provides another dimension of agent execution behavior.

The observed mean runtimes were:

| Agent    | Mean Runtime |
| -------- | -----------: |
| Baseline |       1.41 s |
| Agent 02 |       1.50 s |
| Agent 03 |       1.34 s |
| Agent 04 |       2.42 s |
| Agent 05 |       1.06 s |

Agent 04 required two attempts on average and also had the highest mean runtime in this experiment.

This illustrates how recovery can introduce additional execution cost.

Runtime should nevertheless be interpreted cautiously because it depends on the local hardware, Docker environment, Python runtime, system load, and other execution conditions.

---

## 3.7 Key Findings

The experiment produced several observations.

### Finding 1: Final success does not capture first-attempt behavior

Baseline and Agent 04 both achieved 100% final success, but their Pass@1 values were 100% and 0%, respectively.

### Finding 2: Recovery behavior is measurable

Agent 04 recovered successfully from its initial failures in all five runs.

### Finding 3: Recovery failure is distinguishable from initial failure

Agent 05 triggered recovery but encountered recovery errors, resulting in 0% final success.

### Finding 4: Attempts provide additional reliability information

Agent 04 required an average of two attempts, while the agents that succeeded immediately required one.

### Finding 5: Runtime adds an execution-cost dimension

Recovery-based execution can require additional runtime compared with immediate success.

Together, these observations support the use of trajectory-aware metrics alongside final success.

---

# 4. DISCUSSION

## 4.1 Final Success Can Hide Execution Differences

The most important observation from the experiment is that identical final outcomes can correspond to different execution behaviors.

The baseline achieved 100% final success through first-attempt success.

Agent 04 also achieved 100% final success, but every run required recovery.

A conventional final pass/fail evaluation would classify both outcomes identically.

AgentReliability distinguishes them through Pass@1, recovery metrics, attempts, and runtime.

---

## 4.2 Recovery as a Reliability Dimension

Recovery is particularly relevant for autonomous coding agents because software engineering is inherently iterative.

An agent may encounter:

* incorrect assumptions;
* failing tests;
* type errors;
* missing imports;
* invalid implementation logic;
* incomplete modifications.

An evaluation framework that records only the final state cannot distinguish whether an agent was robust from the beginning or whether it relied heavily on repair cycles.

Recovery-aware evaluation makes this behavior observable.

---

## 4.3 Reliability Is Multidimensional

The experiment suggests that coding-agent reliability should not be represented by one binary value.

Relevant dimensions include:

1. Initial correctness
2. Eventual correctness
3. Recovery behavior
4. Failure type
5. Number of attempts
6. Execution time
7. Run-to-run consistency

These dimensions describe different properties of an agent's behavior.

The framework therefore does not attempt to replace final success with a single alternative score. Instead, it provides a richer set of measurements.

---

## 4.4 Implications for Coding-Agent Evaluation

A coding-agent evaluation report can provide substantially more information by reporting:

* Pass@1;
* eventual success;
* recovery trigger rate;
* recovery completion rate;
* recovery success rate;
* mean attempts;
* runtime;
* failure distribution.

This allows researchers to distinguish agents that solve tasks immediately from agents that depend on recovery.

The results also motivate future research into recovery policies, repair quality, and trajectory-level evaluation.

---

## 4.5 Reproducibility

Reproducibility is a central design goal of AgentReliability.

The framework records:

* experiment IDs;
* task IDs;
* stable run IDs;
* attempt IDs;
* execution modes;
* agent identifiers;
* run numbers;
* test outcomes;
* failure information;
* recovery information;
* runtime;
* result CSVs.

The benchmark integrity test suite was also executed successfully, with **6 tests passing**, providing an additional automated check of benchmark/result integrity.

The final metrics report was regenerated successfully from the stored experiment data.

---

# 5. THREATS TO VALIDITY

## 5.1 Small Sample Size

Each agent was evaluated only five times.

Consequently, the observed 0% and 100% rates should not be interpreted as definitive population-level estimates.

Wilson confidence intervals are reported to make this uncertainty explicit.

---

## 5.2 Single Benchmark Task

The controlled experiment evaluates only `task_32`.

Therefore, the results cannot establish that the observed behavior will occur across different software-engineering tasks.

A larger benchmark containing diverse tasks would be required to evaluate generality.

---

## 5.3 Agent Implementation

The evaluated agents are experimental evaluation agents rather than necessarily production-scale commercial coding systems.

In particular, Agent 03 uses a deterministic offline heuristic recovery backend rather than a hosted large language model.

Therefore, the primary purpose of the experiment is to demonstrate the evaluation framework and its ability to distinguish execution trajectories, rather than to establish a general ranking of commercial coding models.

---

## 5.4 Task-Specific Recovery Behavior

Recovery behavior can depend strongly on the task.

The recovery mechanisms used in this experiment may perform differently on tasks involving:

* larger repositories;
* multiple interacting modules;
* complex dependencies;
* ambiguous requirements;
* concurrency;
* external services.

Consequently, the recovery findings should be treated as task-specific observations.

---

## 5.5 Runtime Environment

Runtime measurements are affected by:

* CPU performance;
* memory availability;
* Docker overhead;
* Python version;
* system load;
* filesystem performance;
* test-suite complexity.

Therefore, runtime values should primarily be compared within controlled experimental environments.

---

# 6. CONCLUSION

This work introduced **AgentReliability**, a reproducible framework for evaluating coding-agent reliability beyond final pass/fail outcomes.

The framework records execution trajectories including initial generation, test execution, failure classification, recovery, attempts, runtime, and final outcomes.

A controlled experiment containing 25 runs across five agents demonstrated why these measurements are useful.

The baseline achieved 100% Pass@1 and 100% final success.

Agent 04 achieved 0% Pass@1 but 100% final success through successful recovery in every run.

Agent 05 also achieved 0% Pass@1, but its recovery process failed in every run, resulting in 0% final success.

These observations demonstrate that agents with different execution trajectories can appear identical under a final pass/fail evaluation.

AgentReliability therefore provides a richer representation of coding-agent behavior by measuring both **initial performance and recovery behavior**.

The current experiment is intentionally limited: it uses one task and five runs per agent. Consequently, it should be considered an initial controlled demonstration rather than a general evaluation or ranking of coding agents.

Future experiments across larger and more diverse benchmarks are required to determine how well these reliability dimensions generalize.

---

# 7. FUTURE WORK

Several directions can extend AgentReliability.

## 7.1 Larger Benchmarks

Evaluate the framework across larger collections of software-engineering tasks to determine whether the observed reliability patterns generalize.

## 7.2 Real LLM Coding Agents

Add adapters for real coding-agent systems and language-model providers, including OpenAI, Claude, Gemini, and other agent implementations.

## 7.3 Advanced Recovery Policies

Investigate different recovery strategies, including:

* iterative self-repair;
* test-driven repair;
* failure-specific repair policies;
* retry budgets;
* context-aware recovery;
* recovery stopping criteria.

## 7.4 Expanded Statistical Analysis

Future experiments can use larger sample sizes and investigate:

* confidence intervals;
* variance;
* effect sizes;
* trajectory distributions;
* failure correlations;
* recovery probability;
* runtime distributions.

## 7.5 Multi-Agent Experiments

Evaluate multiple coding agents on the same task collection and analyze their execution trajectories using a common evaluation protocol.

## 7.6 Public Reproducible Benchmark

A future public release could include:

* task definitions;
* task configurations;
* execution infrastructure;
* agent adapters;
* Docker environments;
* benchmark integrity tests;
* run-level results;
* attempt-level results;
* statistical analysis tools.

Such a release would allow other researchers to reproduce and extend the experiments.

---

# 8. REFERENCES

[1] C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan, **“SWE-bench: Can Language Models Resolve Real-World GitHub Issues?”**, arXiv:2310.06770, 2023.

[2] M. Chen et al., **“Evaluating Large Language Models Trained on Code,”** arXiv:2107.03374, 2021.

[3] E. B. Wilson, **“Probable Inference, the Law of Succession, and Statistical Inference,”** Journal of the American Statistical Association, vol. 22, no. 158, pp. 209–212, 1927.

[4] Docker Documentation, **“None network driver,”** Docker Engine Documentation. The `none` network driver provides a completely isolated networking stack for a container.

[5] Docker Documentation, **“Running containers,”** Docker Engine Documentation. Docker containers provide isolated filesystem, networking, and process environments.

[6] R. Aleithan, H. Xue, M. M. Mohajer, E. Nnorom, G. Uddin, and S. Wang, **“SWE-Bench+: Enhanced Coding Benchmark for LLMs,”** arXiv:2410.06992, 2024.

---

## Experimental Artifact

The experimental artifacts associated with this research include:

* `results/results_v2_execution.csv`
* `results/attempts_v2_execution.csv`
* `metrics/task32-multiagent-final.txt`
* benchmark integrity tests
* AgentReliability evaluator implementation
* Docker-based execution configuration

The reported experiment is identified by:

**`task32-multiagent-docker-v1`**

and contains **25 independent evaluation runs across five agents**.
