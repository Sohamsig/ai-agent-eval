from evaluator.reporting import build_report, duplicate_report, normalize_final_record, summarize_records

def test_legacy_normalization_preserves_unknown_values():
    row=normalize_final_record({"task_id":"t","agent":"a","run":"1","passed":"true","duration_seconds":"unknown"}); assert row["run_number"]=="1" and row["final_success"]=="true" and row["duration_seconds"] is None
def test_v2_multiple_agents_and_rate():
    report=build_report([{"run_id":"one","task_id":"t","agent":"a","run_number":1,"final_success":True},{"run_id":"two","task_id":"t","agent":"b","run_number":1,"final_success":False}],"sample.csv"); assert set(report["agents"])=={"a","b"} and report["success_rate"]==50.0
def test_duplicates_are_not_silently_selected():
    rows=[{"task_id":"t","agent":"a","run_number":1,"final_success":True},{"task_id":"t","agent":"a","run_number":1,"final_success":False}]; report=build_report(rows,"sample.csv"); assert duplicate_report(rows)["duplicate_groups"]==1 and report["unique_unambiguous_runs"]==0 and report["success_rate"] is None
def test_unknown_outcome_is_not_failure():
    summary=summarize_records([{"task_id":"t","agent":"a","run_number":1,"final_success":"unknown"}]); assert summary["agents"]["a"]["known_outcomes"]==0 and summary["agents"]["a"]["success_rate"] is None
