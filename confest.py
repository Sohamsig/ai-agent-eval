import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TASKS_DIR = ROOT / "tasks"

# Add the root of the project, not every task directory.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))