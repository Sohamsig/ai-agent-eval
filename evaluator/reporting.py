"""Shared, non-destructive reporting utilities for final result records."""
from __future__ import annotations
import csv
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping
from evaluator.result_schema import normalize_final_record

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LEGACY_RESULTS_FILE = PROJECT_ROOT / "results" / "results.csv"
V2_RESULTS_FILE = PROJECT_ROOT / "results" / "results_v2.csv"

def default_results_path() -> Path:
    return V2_RESULTS_FILE if V2_RESULTS_FILE.exists() else LEGACY_RESULTS_FILE

def load_final_records(path: Path | str | None = None) -> list[dict[str, Any]]:
    source = Path(path) if path is not None else default_results_path()
    with source.open("r", newline="", encoding="utf-8-sig") as file:
        return [normalize_final_record(row) for row in csv.DictReader(file)]

def as_bool(value: Any) -> bool | None:
    if isinstance(value, bool): return value
    if isinstance(value, str):
        if value.strip().lower() in {"true","1","yes","success","passed"}: return True
        if value.strip().lower() in {"false","0","no","failed","failure"}: return False
    return None

def logical_key(row: Mapping[str, Any]) -> tuple[Any, ...]:
    return ("run_id", row["run_id"]) if row.get("run_id") else ("legacy", row.get("task_id"), row.get("agent"), row.get("run_number"))

def duplicate_report(records: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    groups: dict[tuple[Any,...], list[dict[str,Any]]] = defaultdict(list)
    for record in records:
        row = normalize_final_record(record); groups[logical_key(row)].append(row)
    duplicates = {key: rows for key, rows in groups.items() if len(rows) > 1}
    return {"raw_rows":sum(map(len,groups.values())),"logical_runs":len(groups),"duplicate_groups":len(duplicates),"duplicate_rows":sum(len(rows)-1 for rows in duplicates.values()),"affected_keys":[list(key) for key in sorted(duplicates,key=str)],"groups":dict(groups)}

def summarize_records(records: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    duplicates = duplicate_report(records)
    usable = [rows[0] for rows in duplicates["groups"].values() if len(rows) == 1]
    agents = {}
    for agent in sorted({str(row.get("agent")) for row in usable}):
        rows = [row for row in usable if str(row.get("agent")) == agent]
        outcomes = [as_bool(row.get("final_success")) for row in rows]; known = [v for v in outcomes if v is not None]; successes=sum(v is True for v in known)
        agents[agent]={"unique_unambiguous_runs":len(rows),"known_outcomes":len(known),"unknown_outcomes":len(rows)-len(known),"successful_runs":successes,"failed_runs":sum(v is False for v in known),"success_rate":round(successes/len(known)*100,2) if known else None}
    return {"duplicates":{key:value for key,value in duplicates.items() if key != "groups"},"agents":agents,"usable_records":usable}

def build_report(records: Iterable[Mapping[str, Any]], source_path: Path | str) -> dict[str, Any]:
    rows=list(records); summary=summarize_records(rows); agents=summary["agents"]; known=sum(x["known_outcomes"] for x in agents.values()); successes=sum(x["successful_runs"] for x in agents.values())
    return {"report_type":"AI Coding Agent Evaluation Report","generated_at":datetime.now(timezone.utc).isoformat(),"source_csv":str(source_path),"raw_rows":len(rows),"unique_logical_runs":summary["duplicates"]["logical_runs"],"unique_unambiguous_runs":len(summary["usable_records"]),"excluded_ambiguous_rows":summary["duplicates"]["raw_rows"]-len(summary["usable_records"]),"duplicate_analysis":summary["duplicates"],"known_outcomes":known,"successful_runs":successes,"failed_runs":known-successes,"unknown_outcomes":len(summary["usable_records"])-known,"success_rate":round(successes/known*100,2) if known else None,"agents":agents}
