\# AgentReliability Research Artifact



AgentReliability is a reproducible framework for evaluating coding-agent

reliability beyond final pass/fail results.



\## Final Experiment



\- Experiment ID: `task32-multiagent-docker-v1`

\- Task: `task\_32`

\- Agents: 5

\- Runs per agent: 5

\- Total runs: 25

\- Execution mode: Docker

\- Hidden-test verification: Yes

\- Statistical reporting: Wilson 95% confidence intervals



\## Agents



\- baseline

\- agent\_02

\- agent\_03

\- agent\_04

\- agent\_05



\## Metrics



The framework records:



\- Final success rate

\- Pass@1

\- Generation success

\- Test execution

\- Recovery trigger rate

\- Recovery completion rate

\- Recovery error rate

\- Recovery success rate

\- Attempts used

\- Runtime

\- Runtime variance

\- Failure distributions

\- Wilson 95% confidence intervals



\## Reproduce Metrics



```powershell

python -m evaluator.metrics --experiment-id task32-multiagent-docker-v1

