# AI Agent Evaluation Benchmark

This project evaluates AI coding agents by executing generated solutions
against visible and hidden tests.

## Evaluation Pipeline

1. Load task prompt
2. Create isolated workspace
3. Generate agent solution
4. Run visible tests
5. Run hidden tests
6. Classify failures
7. Record execution metrics
8. Compare baseline and agent performance

## Metrics

- Task pass rate
- Average execution time
- Failure classification
- Visible test success
- Hidden test success
- Agent repair success

## Current Status

- [x] Task validation
- [x] Isolated test execution
- [x] Visible test evaluation
- [x] Hidden test evaluation
- [x] CSV result logging
- [x] Baseline agent
- [x] Metrics calculation
- [ ] LLM-powered agent
- [ ] Multi-agent repair
- [ ] SWE-bench integration
