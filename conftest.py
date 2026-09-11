import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS_DIR = ROOT / "tasks"

for task_dir in TASKS_DIR.glob("task_*"):
    task_path = str(task_dir.resolve())
    if task_path not in sys.path:
        sys.path.insert(0, task_path)
