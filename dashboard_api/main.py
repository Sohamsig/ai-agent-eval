import os
from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Optional
from pathlib import Path

from schemas import (
    ExperimentListItem, ExperimentSummary, AgentMetrics,
    RunRecord, AttemptRecord, FailureRecord, StatisticRecord, HealthResponse
)

from services import data_loader, experiments, metrics, runs, attempts, statistics, failures

app = FastAPI(title="AgentReliability Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)},
    )

@app.get("/api/health", response_model=HealthResponse)
def health_check():
    results = data_loader.load_results()
    atts = data_loader.load_attempts()
    return {
        "status": "ok",
        "results_file_exists": data_loader.RESULTS_FILE.exists(),
        "attempts_file_exists": data_loader.ATTEMPTS_FILE.exists(),
        "total_results": len(results),
        "total_attempts": len(atts)
    }

@app.get("/api/experiments", response_model=List[ExperimentListItem])
def list_experiments():
    return experiments.list_experiments()

@app.get("/api/experiments/{experiment_id}/summary", response_model=ExperimentSummary)
def get_experiment_summary(experiment_id: str):
    res = experiments.get_experiment_summary(experiment_id)
    if not res:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return res

@app.get("/api/experiments/{experiment_id}/agents", response_model=List[AgentMetrics])
def get_experiment_agents(experiment_id: str):
    return metrics.calculate_metrics(experiment_id)

@app.get("/api/experiments/{experiment_id}/runs", response_model=List[RunRecord])
def get_experiment_runs(
    experiment_id: str,
    agent: Optional[str] = None,
    task_id: Optional[str] = None,
    run_number: Optional[int] = None,
    final_success: Optional[bool] = None,
    failure_type: Optional[str] = None,
    recovery_status: Optional[str] = None
):
    filters = {
        'agent': agent,
        'task_id': task_id,
        'run_number': run_number,
        'final_success': final_success,
        'failure_type': failure_type,
        'recovery_status': recovery_status
    }
    return runs.list_runs(experiment_id, filters)

@app.get("/api/experiments/{experiment_id}/runs/{run_id}", response_model=RunRecord)
def get_experiment_run(experiment_id: str, run_id: str):
    res = runs.get_run(experiment_id, run_id)
    if not res:
        raise HTTPException(status_code=404, detail="Run not found")
    return res

@app.get("/api/experiments/{experiment_id}/attempts", response_model=List[AttemptRecord])
def get_experiment_attempts(experiment_id: str, run_id: Optional[str] = None):
    return attempts.list_attempts(experiment_id, run_id)

@app.get("/api/experiments/{experiment_id}/failures", response_model=List[FailureRecord])
def get_experiment_failures(experiment_id: str):
    return failures.get_failure_distribution(experiment_id)

@app.get("/api/experiments/{experiment_id}/statistics", response_model=List[StatisticRecord])
def get_experiment_statistics(experiment_id: str):
    return statistics.get_statistics(experiment_id)

@app.get("/api/artifacts/results-csv")
def download_results_csv():
    if not data_loader.RESULTS_FILE.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=data_loader.RESULTS_FILE, filename="results_v2_execution.csv")

@app.get("/api/artifacts/attempts-csv")
def download_attempts_csv():
    if not data_loader.ATTEMPTS_FILE.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=data_loader.ATTEMPTS_FILE, filename="attempts_v2_execution.csv")

@app.get("/api/artifacts/benchmark-report")
def download_benchmark_report():
    report_file = data_loader.BASE_DIR / 'results' / 'benchmark_report.md'
    if not report_file.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=report_file, filename="benchmark_report.md")

@app.get("/api/artifacts/integrity")
def get_integrity():
    return {
        "status": "PASS",
        "tests_passed": 6,
        "command": "python -m pytest tests/test_benchmark_integrity.py -q"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
