from pydantic import BaseModel
from typing import List, Optional, Any

class ExperimentListItem(BaseModel):
    experiment_id: str
    task_count: int
    agent_count: int
    run_count: int
    created_at: Optional[str] = None

class ExperimentSummary(BaseModel):
    experiment_id: str
    total_runs: int
    attempt_records: int
    agents: int
    tasks: List[str]
    agent_list: List[str]
    execution_mode: Optional[str] = None
    hidden_test_verification: bool
    confidence_interval: str

class AgentMetrics(BaseModel):
    agent: str
    runs: int
    generation_success_rate: float
    test_pass_rate: float
    pass_at_1: float
    final_success_rate: float
    recovery_trigger_rate: float
    recovery_completed_rate: float
    recovery_success_rate: float
    recovery_error_rate: float
    average_attempts: float
    average_runtime: float
    runtime_stddev: float
    runtimes: List[float]

class AttemptRecord(BaseModel):
    schema_version: Optional[str] = None
    timestamp: Optional[str] = None
    run_id: Optional[str] = None
    experiment_id: Optional[str] = None
    execution_mode: Optional[str] = None
    attempt_id: Optional[str] = None
    task_id: Optional[str] = None
    agent: Optional[str] = None
    run_number: Optional[int] = None
    attempt_number: Optional[int] = None
    generation_success: Optional[bool] = None
    tests_executed: Optional[bool] = None
    tests_passed: Optional[bool] = None
    tests_total: Optional[int] = None
    tests_passed_count: Optional[int] = None
    tests_failed_count: Optional[int] = None
    tests_skipped_count: Optional[int] = None
    failure_type: Optional[str] = None
    error_message: Optional[str] = None
    exit_code: Optional[str] = None
    timed_out: Optional[bool] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    duration_seconds: Optional[float] = None

class RunRecord(BaseModel):
    schema_version: Optional[str] = None
    timestamp: Optional[str] = None
    run_id: Optional[str] = None
    experiment_id: Optional[str] = None
    execution_mode: Optional[str] = None
    task_id: Optional[str] = None
    agent: Optional[str] = None
    run_number: Optional[int] = None
    generation_success: Optional[bool] = None
    tests_executed: Optional[bool] = None
    tests_passed: Optional[bool] = None
    tests_total: Optional[int] = None
    tests_passed_count: Optional[int] = None
    tests_failed_count: Optional[int] = None
    tests_skipped_count: Optional[int] = None
    final_success: Optional[bool] = None
    failure_type: Optional[str] = None
    error_message: Optional[str] = None
    exit_code: Optional[str] = None
    timed_out: Optional[bool] = None
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    recovery_attempted: Optional[bool] = None
    recovery_success: Optional[bool] = None
    attempts_used: Optional[int] = None
    max_attempts: Optional[int] = None
    duration_seconds: Optional[float] = None
    attempts: List[AttemptRecord] = []

class FailureRecord(BaseModel):
    failure_type: str
    count: int
    percentage: float
    affected_agents: List[str]
    affected_tasks: List[str]

class StatisticRecord(BaseModel):
    metric: str
    agent: str
    rate: float
    successes: int
    n: int
    ci_lower: float
    ci_upper: float

class HealthResponse(BaseModel):
    status: str
    results_file_exists: bool
    attempts_file_exists: bool
    total_results: int
    total_attempts: int
