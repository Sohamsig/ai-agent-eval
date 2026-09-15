from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evaluator.result_schema import (
    ATTEMPT_RESULT_FIELDS,
    FINAL_RESULT_FIELDS,
    new_attempt_id,
    new_run_id,
    normalize_attempt_record,
    normalize_final_record,
    validate_attempt_record,
    validate_final_record,
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Make project imports available when this file is executed as:
# python .\evaluator\evaluate.py
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

EVALUATOR_ROOT = PROJECT_ROOT / "evaluator"
TASKS_ROOT = PROJECT_ROOT / "tasks"
AGENTS_ROOT = PROJECT_ROOT / "agents"
WORKSPACES_ROOT = PROJECT_ROOT / "workspaces"
RESULTS_ROOT = PROJECT_ROOT / "results"
HIDDEN_TESTS_ROOT = EVALUATOR_ROOT / "hidden_tests"


# ============================================================
# CONFIGURATION
# ============================================================

AGENTS = [
    "baseline",
    "agent_02",
]

RUNS_PER_AGENT = 5
MAX_ATTEMPTS = 3


# ============================================================
# TASK REGISTRY
# ============================================================
#
# The benchmark currently contains task_01 through task_32.
#
# Test commands are discovered automatically from the task
# directory. This makes the evaluator less dependent on manually
# maintaining 32 test filenames.
#
# If a task contains:
#
#     test_foo.py
#
# the evaluator runs:
#
#     python -m pytest test_foo.py
#
# If multiple test_*.py files exist, they are all executed.
#
# You can override a task manually in TASK_OVERRIDES below.
# ============================================================

TASKS = {
    f"task_{i:02d}": {
        "path": TASKS_ROOT / f"task_{i:02d}",
        "test_command": None,
    }
    for i in range(1, 33)
}


# Optional explicit overrides.
#
# Example:
#
# "task_10": {
#     "path": TASKS_ROOT / "task_10",
#     "test_command": "python -m pytest test_csv_utils.py",
# }
#
# Leave empty unless a task requires a special command.

TASK_OVERRIDES: dict[str, dict[str, Any]] = {}


# ============================================================
# GENERAL HELPERS
# ============================================================

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_directories() -> None:
    WORKSPACES_ROOT.mkdir(parents=True, exist_ok=True)
    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)
    HIDDEN_TESTS_ROOT.mkdir(parents=True, exist_ok=True)


def safe_text(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    try:
        return json.dumps(value, indent=2, default=str)
    except Exception:
        return str(value)


def remove_pycache(root: Path) -> None:
    if not root.exists():
        return

    for path in root.rglob("__pycache__"):
        if path.is_dir():
            try:
                shutil.rmtree(path)
            except Exception:
                pass


# ============================================================
# TASK DISCOVERY
# ============================================================

def discover_test_files(task_path: Path) -> list[Path]:
    if not task_path.exists():
        return []

    tests = sorted(
        path
        for path in task_path.glob("test_*.py")
        if path.is_file()
    )

    return tests


def discover_test_command(task_id: str) -> str:
    task = TASKS[task_id]
    task_path = Path(task["path"])

    # Explicit override
    override = TASK_OVERRIDES.get(task_id)

    if override and override.get("test_command"):
        return str(override["test_command"])

    if task.get("test_command"):
        return str(task["test_command"])

    test_files = discover_test_files(task_path)

    if not test_files:
        raise RuntimeError(
            f"No test files found for {task_id} in {task_path}"
        )

    names = [test.name for test in test_files]

    return (
        "python -m pytest "
        + " ".join(names)
    )


# ============================================================
# TASK VALIDATION
# ============================================================

def validate_task_configuration(task_id: str) -> tuple[bool, str]:
    if task_id not in TASKS:
        return False, f"Unknown task: {task_id}"

    task_path = Path(TASKS[task_id]["path"])

    if not task_path.exists():
        return False, f"Task directory does not exist: {task_path}"

    if not task_path.is_dir():
        return False, f"Task path is not a directory: {task_path}"

    prompt_path = task_path / "prompt.txt"

    if not prompt_path.exists():
        return False, f"Missing prompt.txt in {task_path}"

    test_files = discover_test_files(task_path)

    if not test_files:
        return False, f"No test_*.py file found in {task_path}"

    try:
        test_command = discover_test_command(task_id)
    except Exception as exc:
        return False, str(exc)

    return True, test_command


def validate_tasks(task_ids: list[str] | None = None) -> bool:
    print()
    print("=" * 70)
    print("VALIDATING TASK CONFIGURATION")
    print("=" * 70)

    if task_ids is None:
        task_ids = list(TASKS.keys())

    all_valid = True

    for task_id in task_ids:
        ok, message = validate_task_configuration(task_id)

        if ok:
            print(f"[OK] {task_id:<12} {message}")
        else:
            print(f"[FAIL] {task_id:<12} {message}")
            all_valid = False

    print()

    if all_valid:
        print(f"All {len(task_ids)} task configurations are valid.")
    else:
        print("One or more task configurations are invalid.")

    return all_valid


# ============================================================
# WORKSPACE CREATION
# ============================================================

def create_clean_workspace(
    task_id: str,
    agent: str,
    run_number: int,
) -> Path:

    task_path = Path(TASKS[task_id]["path"])

    workspace = (
        WORKSPACES_ROOT
        / f"{task_id}_{agent}_{run_number}"
    )

    if workspace.exists():
        shutil.rmtree(workspace)

    shutil.copytree(
        task_path,
        workspace,
    )

    # --------------------------------------------------------
    # Compatibility package
    #
    # Some tests may import:
    #
    # from tasks.task_10.csv_utils import ...
    #
    # Therefore create:
    #
    # workspace/
    #   tasks/
    #       __init__.py
    #       task_10/
    #           __init__.py
    #           ...
    # --------------------------------------------------------

    tasks_package = workspace / "tasks"
    task_package = tasks_package / task_id

    tasks_package.mkdir(
        parents=True,
        exist_ok=True,
    )

    task_package.mkdir(
        parents=True,
        exist_ok=True,
    )

    (tasks_package / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )

    (task_package / "__init__.py").write_text(
        "",
        encoding="utf-8",
    )

    # Copy task files into compatibility package.
    for item in task_path.iterdir():

        if item.name == "__pycache__":
            continue

        destination = task_package / item.name

        if item.is_file():
            shutil.copy2(
                item,
                destination,
            )

    remove_pycache(workspace)

    return workspace


# ============================================================
# AGENT LOADING
# ============================================================

def load_agent(agent_name: str):
    """
    Load an agent directly from:

        PROJECT_ROOT / agents / <agent_name>.py

    This intentionally does NOT use:

        importlib.import_module("agents.agent_02")

    because the evaluator must not depend on the current working
    directory or Python package resolution.
    """

    agent_path = (
        AGENTS_ROOT
        / f"{agent_name}.py"
    )

    if not agent_path.exists():
        raise RuntimeError(
            f"Agent file not found: {agent_path}"
        )

    try:
        module_name = (
            f"benchmark_agent_{agent_name}"
        )

        spec = importlib.util.spec_from_file_location(
            module_name,
            agent_path,
        )

        if spec is None:
            raise RuntimeError(
                f"Could not create import specification "
                f"for {agent_path}"
            )

        if spec.loader is None:
            raise RuntimeError(
                f"Agent loader is unavailable for "
                f"{agent_path}"
            )

        module = (
            importlib.util.module_from_spec(spec)
        )

        spec.loader.exec_module(module)

        return module

    except Exception as exc:
        raise RuntimeError(
            f"Could not import agent '{agent_name}': "
            f"{type(exc).__name__}: {exc}"
        ) from exc


# ============================================================
# AGENT RESPONSE VALIDATION
# ============================================================

def validate_agent_solution(
    solution: Any,
) -> dict[str, Any]:

    if not isinstance(solution, dict):
        raise RuntimeError(
            "Agent solve() must return a dictionary."
        )

    status = solution.get("status")

    if status is None:
        raise RuntimeError(
            "Agent response is missing 'status'."
        )

    if status != "completed":
        return solution

    files = solution.get("files")

    if files is None:
        raise RuntimeError(
            "Completed agent response is missing 'files'."
        )

    if not isinstance(files, dict):
        raise RuntimeError(
            "'files' must be a dictionary."
        )

    for filename, content in files.items():

        if not isinstance(filename, str):
            raise RuntimeError(
                "Agent file names must be strings."
            )

        if not isinstance(content, str):
            raise RuntimeError(
                f"Content for '{filename}' must be a string."
            )

    return solution


# ============================================================
# WORKSPACE PATH SECURITY
# ============================================================

def safe_workspace_path(
    workspace: Path,
    relative_path: str,
) -> Path:

    if not isinstance(relative_path, str):
        raise RuntimeError(
            "Agent file path must be a string."
        )

    # Normalize Windows separators.
    relative_path = relative_path.replace(
        "\\",
        "/",
    )

    relative = Path(relative_path)

    if relative.is_absolute():
        raise RuntimeError(
            f"Absolute paths are not allowed: "
            f"{relative_path}"
        )

    destination = (
        workspace / relative
    ).resolve()

    workspace_resolved = (
        workspace.resolve()
    )

    try:
        destination.relative_to(
            workspace_resolved
        )
    except ValueError:
        raise RuntimeError(
            f"Agent attempted to write outside "
            f"workspace: {relative_path}"
        )

    return destination


# ============================================================
# APPLY AGENT SOLUTION
# ============================================================

def apply_agent_solution(
    workspace: Path,
    task_id: str,
    solution: dict[str, Any],
) -> list[str]:

    files = solution.get(
        "files",
        {},
    )

    if not files:
        print("[Agent] No files generated by agent.")
        return []

    written_files: list[str] = []

    task_package = (
        workspace
        / "tasks"
        / task_id
    )

    task_package.mkdir(
        parents=True,
        exist_ok=True,
    )

    (task_package / "__init__.py").touch(
        exist_ok=True
    )

    for filename, content in files.items():

        destination = safe_workspace_path(
            workspace,
            filename,
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_text(
            content,
            encoding="utf-8",
        )

        written_files.append(
            filename
        )

        print(
            f"[Agent] Wrote: {filename}"
        )

        # ----------------------------------------------------
        # Synchronize ONLY the current task package.
        #
        # Important:
        # Do not copy agent-generated files into every task.
        # ----------------------------------------------------

        package_destination = (
            task_package
            / Path(filename)
        )

        package_destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        package_destination.write_text(
            content,
            encoding="utf-8",
        )

        print(
            f"[Agent] Synchronized: "
            f"{package_destination}"
        )

    remove_pycache(workspace)

    return written_files


# ============================================================
# FAILURE CLASSIFICATION
# ============================================================

def classify_test_failure(
    stdout: str,
    stderr: str,
    return_code: int,
) -> str:

    combined = (
        (stdout or "")
        + "\n"
        + (stderr or "")
    ).lower()

    # Evaluator/environment failures
    evaluator_errors = [
        "no module named 'tasks'",
        "no module named \"tasks\"",
        "pytest internal error",
        "internalerror",
        "pluggy._manager",
        "keyboardinterrupt",
    ]

    for marker in evaluator_errors:
        if marker in combined:
            return "evaluator_error"

    if return_code == 0:
        return "success"

    # Common engineering failure categories
    if (
        "syntaxerror" in combined
        or "invalid syntax" in combined
    ):
        return "syntax_error"

    if (
        "modulenotfounderror" in combined
        or "importerror" in combined
    ):
        return "import_error"

    if (
        "typeerror" in combined
    ):
        return "type_error"

    if (
        "nameerror" in combined
    ):
        return "name_error"

    if (
        "attributeerror" in combined
    ):
        return "attribute_error"

    if (
        "keyerror" in combined
    ):
        return "key_error"

    if (
        "indexerror" in combined
    ):
        return "index_error"

    if (
        "assertionerror" in combined
        or "assert " in combined
        or "failed" in combined
    ):
        return "assertion_failure"

    if (
        "timeout" in combined
        or "timed out" in combined
    ):
        return "timeout"

    if (
        "connectionerror" in combined
        or "connection refused" in combined
    ):
        return "connection_error"

    if (
        "permissionerror" in combined
        or "permission denied" in combined
    ):
        return "permission_error"

    return "test_failure"

# ============================================================
# TEST COMMAND HELPERS
# ============================================================

def build_test_environment(workspace: Path, task_dir: Path) -> dict:
    """Create the environment used when running tests."""
    env = os.environ.copy()

    python_paths = [
        str(workspace),
        str(task_dir),
    ]

    existing_pythonpath = env.get("PYTHONPATH")
    if existing_pythonpath:
        python_paths.append(existing_pythonpath)

    env["PYTHONPATH"] = os.pathsep.join(python_paths)
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    return env

def tokenize_test_command(
    test_command: str,
) -> list[str]:
    """
    Convert a test command string into subprocess arguments.

    The command is never executed through a shell.

    Examples:

        python -m pytest test_client.py

    becomes:

        ["python", "-m", "pytest", "test_client.py"]
    """

    if not isinstance(test_command, str):
        raise ValueError("test_command must be a string.")

    command = test_command.strip()

    if not command:
        raise ValueError("test_command cannot be empty.")

    # Windows-compatible command parsing.
    try:
        tokens = shlex.split(
            command,
            posix=False,
        )
    except ValueError as exc:
        raise ValueError(
            f"Could not parse test command: {exc}"
        ) from exc

    if not tokens:
        raise ValueError("test_command produced no arguments.")

    # Remove wrapping quotes from individual Windows tokens.
    cleaned_tokens: list[str] = []

    for token in tokens:
        cleaned_tokens.append(
            token.strip('"').strip("'")
        )

    return cleaned_tokens


def normalize_test_command(
    test_command: str,
) -> list[str]:
    """
    Normalize a test command for isolated execution.

    The evaluator replaces the command executable with the
    current Python interpreter when the command uses:

        python
        python.exe
        py
        pytest

    This makes execution reproducible and avoids depending on
    the user's PATH.
    """

    tokens = tokenize_test_command(test_command)

    executable = Path(tokens[0]).name.lower()

    python_names = {
        "python",
        "python.exe",
        "python3",
        "python3.exe",
        "py",
        "py.exe",
    }

    pytest_names = {
        "pytest",
        "pytest.exe",
    }

    if executable in python_names:
        tokens[0] = sys.executable

    elif executable in pytest_names:
        tokens = [
            sys.executable,
            "-m",
            "pytest",
            *tokens[1:],
        ]

    else:
        raise ValueError(
            "Only Python and pytest test commands are supported. "
            f"Received executable: {tokens[0]}"
        )

    # If the command is simply:
    #
    # python test_file.py
    #
    # it is allowed, but normal benchmark commands should use
    # python -m pytest.
    return tokens


def resolve_command_paths(
    command: list[str],
    workspace: Path,
) -> list[str]:
    """
    Resolve relative test paths against the isolated workspace.

    Python executable paths and pytest configuration paths are
    preserved correctly.
    """

    resolved: list[str] = []

    options_with_values = {
        "-c",
        "--config",
        "--rootdir",
        "--basetemp",
        "--junitxml",
        "--html",
        "--cov",
    }

    index = 0

    while index < len(command):
        token = command[index]

        # Always preserve executable.
        if index == 0:
            resolved.append(token)
            index += 1
            continue

        # Handle options that consume the next argument.
        if token in options_with_values:
            resolved.append(token)

            if index + 1 < len(command):
                value = command[index + 1]

                if Path(value).is_absolute():
                    resolved.append(value)
                else:
                    resolved.append(
                        str(
                            (workspace / value).resolve()
                        )
                    )

                index += 2
                continue

            index += 1
            continue

        # Preserve flags.
        if token.startswith("-"):
            resolved.append(token)
            index += 1
            continue

        # Preserve Python module names.
        if token in {
            "pytest",
            "unittest",
        }:
            resolved.append(token)
            index += 1
            continue

        token_path = Path(token)

        # Preserve already absolute paths.
        if token_path.is_absolute():
            resolved.append(str(token_path))
            index += 1
            continue

        # Resolve relative test paths inside workspace.
        candidate = (
            workspace / token_path
        ).resolve()

        try:
            candidate.relative_to(
                workspace.resolve()
            )

        except ValueError:
            raise ValueError(
                "Test command references a path outside "
                f"the isolated workspace: {token}"
            )

        resolved.append(str(candidate))
        index += 1

    return resolved

def create_isolated_pytest_config(workspace: Path) -> Path:
    """
    Create a minimal pytest configuration inside the isolated
    workspace so pytest does not inherit the project's root
    pytest.ini.
    """

    config_path = workspace / ".benchmark_pytest.ini"

    config_path.write_text(
        """[pytest]
addopts = -p no:cacheprovider
testpaths = .
""",
        encoding="utf-8",
    )

    return config_path

# ============================================================
# RUN TESTS
# ============================================================

def run_tests(
    workspace: Path,
    task_id: str,
    test_command: str,
) -> dict[str, Any]:
    """
    Run tests inside an isolated workspace.

    Important isolation rules:

    - Tests execute with cwd=workspace.
    - Only the workspace is added to PYTHONPATH.
    - The main project pytest.ini is not used.
    - A temporary isolated pytest configuration is used.
    - Third-party pytest plugins are disabled.
    - shell=False prevents shell interpretation.
    - Test paths are resolved relative to the workspace.
    """

    start = time.perf_counter()
    workspace = Path(workspace).resolve()

    def result(
        *,
        passed: bool,
        return_code: int,
        stdout: str = "",
        stderr: str = "",
        failure_type: str,
        tests_executed: bool,
    ) -> dict[str, Any]:
        return {
            "passed": passed,
            "return_code": return_code,
            "duration_seconds": round(
                time.perf_counter() - start,
                4,
            ),
            "stdout": stdout,
            "stderr": stderr,
            "failure_type": failure_type,
            "tests_executed": tests_executed,
        }

    if not workspace.exists():
        return result(
            passed=False,
            return_code=-1,
            stderr=f"Workspace does not exist: {workspace}",
            failure_type="evaluator_error",
            tests_executed=False,
        )

    if not workspace.is_dir():
        return result(
            passed=False,
            return_code=-1,
            stderr=f"Workspace is not a directory: {workspace}",
            failure_type="evaluator_error",
            tests_executed=False,
        )

    if not test_command or not test_command.strip():
        return result(
            passed=False,
            return_code=-1,
            stderr="No test command was provided.",
            failure_type="evaluator_error",
            tests_executed=False,
        )

    remove_pycache(workspace)

    # --------------------------------------------------------
    # Create isolated pytest configuration
    # --------------------------------------------------------

    pytest_config = create_isolated_pytest_config(workspace)

    # --------------------------------------------------------
    # Build clean environment
    # --------------------------------------------------------

    env = os.environ.copy()

    for variable in [
        "PYTHONPATH",
        "PYTHONHOME",
        "PYTEST_ADDOPTS",
        "PYTEST_PLUGINS",
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD",
        "PROJECT_ROOT",
        "EVALUATOR_ROOT",
    ]:
        env.pop(variable, None)

    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"
    env["PYTHONNOUSERSITE"] = "1"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"

    # Only the isolated workspace and its task package are importable.
    task_package = workspace / "tasks" / task_id

    python_paths = [
        str(workspace),
    ]

    if task_package.exists() and task_package.is_dir():
        python_paths.append(str(task_package))

    env["PYTHONPATH"] = os.pathsep.join(python_paths)

    # --------------------------------------------------------
    # Parse command
    # --------------------------------------------------------

    try:
        command = tokenize_test_command(test_command)

    except ValueError as exc:
        return result(
            passed=False,
            return_code=-1,
            stderr=f"Invalid test command: {exc}",
            failure_type="evaluator_error",
            tests_executed=False,
        )

    if not command:
        return result(
            passed=False,
            return_code=-1,
            stderr="Test command produced no arguments.",
            failure_type="evaluator_error",
            tests_executed=False,
        )

    # --------------------------------------------------------
    # Normalize executable
    # --------------------------------------------------------

    executable_name = Path(command[0]).name.lower()

    python_names = {
        "python",
        "python.exe",
        "python3",
        "python3.exe",
        "py",
        "py.exe",
    }

    pytest_names = {
        "pytest",
        "pytest.exe",
    }

    if executable_name in python_names:
        command[0] = sys.executable

    elif executable_name in pytest_names:
        command = [
            sys.executable,
            "-m",
            "pytest",
            *command[1:],
        ]

    else:
        return result(
            passed=False,
            return_code=-1,
            stderr=(
                "Only Python and pytest commands are supported. "
                f"Received: {command[0]}"
            ),
            failure_type="evaluator_error",
            tests_executed=False,
        )

    # --------------------------------------------------------
    # Add isolated pytest configuration
    # --------------------------------------------------------

    if "-m" in command:
        try:
            pytest_index = command.index("pytest")
        except ValueError:
            pytest_index = -1

        if pytest_index != -1:
            command.insert(
                pytest_index + 1,
                "-c",
            )
            command.insert(
                pytest_index + 2,
                str(pytest_config),
            )

    # --------------------------------------------------------
    # Resolve test paths
    # --------------------------------------------------------

    try:
        command = resolve_command_paths(
            command,
            workspace,
        )

    except ValueError as exc:
        return result(
            passed=False,
            return_code=-1,
            stderr=str(exc),
            failure_type="evaluator_error",
            tests_executed=False,
        )

    # --------------------------------------------------------
    # Reject shell syntax
    # --------------------------------------------------------

    forbidden_shell_tokens = {
        "|",
        "||",
        "&",
        "&&",
        ";",
        ">",
        ">>",
        "<",
        "2>",
        "2>>",
        "$(",
        "`",
    }

    if any(
        token in forbidden_shell_tokens
        for token in command
    ):
        return result(
            passed=False,
            return_code=-1,
            stderr=(
                "Test command contains unsupported shell syntax: "
                f"{test_command}"
            ),
            failure_type="evaluator_error",
            tests_executed=False,
        )

    # --------------------------------------------------------
    # Execute tests
    # --------------------------------------------------------

    try:
        completed = subprocess.run(
            command,
            cwd=str(workspace),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
            shell=False,
        )

        stdout = completed.stdout or ""
        stderr = completed.stderr or ""

        passed = completed.returncode == 0

        failure_type = classify_test_failure(
            stdout,
            stderr,
            completed.returncode,
        )

        return result(
            passed=passed,
            return_code=completed.returncode,
            stdout=stdout,
            stderr=stderr,
            failure_type=failure_type,
            tests_executed=True,
        )

    except subprocess.TimeoutExpired as exc:
        timeout_stdout = exc.stdout or ""
        timeout_stderr = exc.stderr or ""

        if isinstance(timeout_stdout, bytes):
            timeout_stdout = timeout_stdout.decode(
                "utf-8",
                errors="replace",
            )

        if isinstance(timeout_stderr, bytes):
            timeout_stderr = timeout_stderr.decode(
                "utf-8",
                errors="replace",
            )

        return result(
            passed=False,
            return_code=-1,
            stdout=timeout_stdout,
            stderr=(
                timeout_stderr
                + "\n"
                + "Test execution timed out after 120 seconds."
            ),
            failure_type="timeout",
            tests_executed=True,
        )

    except FileNotFoundError as exc:
        return result(
            passed=False,
            return_code=-1,
            stderr=f"Test executable was not found: {exc}",
            failure_type="evaluator_error",
            tests_executed=False,
        )

    except Exception as exc:
        return result(
            passed=False,
            return_code=-1,
            stderr=(
                f"{type(exc).__name__}: {exc}\n"
                + traceback.format_exc()
            ),
            failure_type="evaluator_error",
            tests_executed=False,
        )

    finally:
        # Remove temporary pytest configuration after execution.
        try:
            if pytest_config.exists():
                pytest_config.unlink()
        except Exception:
            pass
    """
    Run the provided test command inside an isolated workspace.

    Important isolation rules:
    - The supplied test_command is actually executed.
    - The evaluator project is not added to PYTHONPATH.
    - Third-party pytest plugins are disabled.
    - The command runs from the isolated workspace.
    - A temporary isolated pytest configuration is written into the workspace.
    - shell=False prevents shell interpretation.
    """

    start = time.perf_counter()
    workspace = Path(workspace).resolve()

    def result(
        *,
        passed: bool,
        return_code: int,
        stdout: str = "",
        stderr: str = "",
        failure_type: str,
        tests_executed: bool,
    ) -> dict[str, Any]:
        return {
            "passed": passed,
            "return_code": return_code,
            "duration_seconds": round(time.perf_counter() - start, 4),
            "stdout": stdout,
            "stderr": stderr,
            "failure_type": failure_type,
            "tests_executed": tests_executed,
        }

    if not workspace.exists():
        return result(
            passed=False,
            return_code=-1,
            stderr=f"Workspace does not exist: {workspace}",
            failure_type="evaluator_error",
            tests_executed=False,
        )

    if not workspace.is_dir():
        return result(
            passed=False,
            return_code=-1,
            stderr=f"Workspace is not a directory: {workspace}",
            failure_type="evaluator_error",
            tests_executed=False,
        )

    if not test_command or not test_command.strip():
        return result(
            passed=False,
            return_code=-1,
            stderr="No test command was provided.",
            failure_type="evaluator_error",
            tests_executed=False,
        )

    remove_pycache(workspace)

    env = os.environ.copy()

    # Remove variables that could leak evaluator/project configuration.
    for variable in [
        "PYTHONPATH",
        "PYTHONHOME",
        "PYTEST_ADDOPTS",
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD",
        "PROJECT_ROOT",
        "EVALUATOR_ROOT",
    ]:
        env.pop(variable, None)

    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUNBUFFERED"] = "1"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"

    # Only the isolated workspace and its task directory may be importable.
    task_package = workspace / "tasks" / task_id

    # Prefer the task package so imports resolve to the synchronized
    # task implementation instead of a stale root-level file.
    python_paths = []

    if task_package.exists() and task_package.is_dir():
        python_paths.append(str(task_package))

    python_paths.append(str(workspace))

    env["PYTHONPATH"] = os.pathsep.join(python_paths)

    # Parse the command without invoking a shell.
    try:
        command = shlex.split(test_command, posix=False)
    except ValueError as exc:
        return result(
            passed=False,
            return_code=-1,
            stderr=f"Invalid test command: {exc}",
            failure_type="evaluator_error",
            tests_executed=False,
        )

    if not command:
        return result(
            passed=False,
            return_code=-1,
            stderr="Test command produced no executable arguments.",
            failure_type="evaluator_error",
            tests_executed=False,
        )

    # Convert "python" / "python.exe" to the current interpreter.
    executable_name = Path(command[0]).name.lower()

    if executable_name in {
        "python",
        "python.exe",
        "python3",
        "python3.exe",
    }:
        command[0] = sys.executable

    # Avoid commands that require shell expansion or command chaining.
    forbidden_shell_tokens = {
        "|",
        "||",
        "&",
        "&&",
        ";",
        ">",
        ">>",
        "<",
        "2>",
        "2>>",
        "$(",
        "`",
    }

    if any(token in forbidden_shell_tokens for token in command):
        return result(
            passed=False,
            return_code=-1,
            stderr=(
                "Test command contains shell syntax that is not allowed "
                "with shell=False: "
                f"{test_command}"
            ),
            failure_type="evaluator_error",
            tests_executed=False,
        )

    try:
        completed = subprocess.run(
            command,
            cwd=str(workspace),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
            shell=False,
        )

        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
        passed = completed.returncode == 0

        failure_type = classify_test_failure(
            stdout,
            stderr,
            completed.returncode,
        )

        return result(
            passed=passed,
            return_code=completed.returncode,
            stdout=stdout,
            stderr=stderr,
            failure_type=failure_type,
            tests_executed=True,
        )

    except subprocess.TimeoutExpired as exc:
        timeout_stdout = exc.stdout or ""
        timeout_stderr = exc.stderr or ""

        if isinstance(timeout_stdout, bytes):
            timeout_stdout = timeout_stdout.decode(
                "utf-8",
                errors="replace",
            )

        if isinstance(timeout_stderr, bytes):
            timeout_stderr = timeout_stderr.decode(
                "utf-8",
                errors="replace",
            )

        timeout_message = (
            timeout_stderr
            + "\n"
            + "Test execution timed out after 120 seconds."
        )

        return result(
            passed=False,
            return_code=-1,
            stdout=timeout_stdout,
            stderr=timeout_message,
            failure_type="timeout",
            tests_executed=True,
        )

    except FileNotFoundError as exc:
        return result(
            passed=False,
            return_code=-1,
            stderr=f"Test executable was not found: {exc}",
            failure_type="evaluator_error",
            tests_executed=False,
        )

    except Exception as exc:
        return result(
            passed=False,
            return_code=-1,
            stderr=(
                f"{type(exc).__name__}: {exc}\n"
                + traceback.format_exc()
            ),
            failure_type="evaluator_error",
            tests_executed=False,
        )

# ============================================================

def get_hidden_test_path(task_id: str) -> Path:
    """
    Return the hidden-test file path for a task.
    Supports both:
        hidden_tests/task_01_hidden.py
        hidden_tests/task_01/test_hidden.py
    """
    candidates = [
        HIDDEN_TESTS_ROOT / f"test_{task_id}_hidden.py",
        HIDDEN_TESTS_ROOT / task_id / "test_hidden.py",
        HIDDEN_TESTS_ROOT / task_id / "hidden_tests.py",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        f"No hidden test file found for task '{task_id}'. "
        f"Checked: {', '.join(str(path) for path in candidates)}"
    )

# HIDDEN TESTS
# ============================================================

def run_hidden_tests(
    workspace: Path,
    task_id: str,
) -> dict[str, Any] | None:
    """
    Run hidden tests inside the isolated workspace.

    Hidden tests are copied into the workspace and executed
    using an absolute path so they cannot accidentally resolve
    relative to the main project.
    """

    try:
        hidden_test = get_hidden_test_path(task_id)
    except FileNotFoundError:
        print(
            f"[Hidden Tests] No hidden tests found for {task_id}; "
            "skipping hidden-test execution."
        )
        return None

    if hidden_test is None:
        return None

    workspace = Path(workspace).resolve()

    hidden_tests_directory = (
        workspace / "__hidden_tests__"
    )

    hidden_tests_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = (
        hidden_tests_directory / hidden_test.name
    )

    shutil.copy2(
        hidden_test,
        destination,
    )

    # Use an absolute path for the copied hidden test.
    command = (
        f'python -m pytest "{destination}" -vv -s'
    )

    hidden_result = run_tests(
        workspace=workspace,
        task_id=task_id,
        test_command=command,
    )

    # Print the actual hidden-test output.
    # This makes hidden failures debuggable.
    print()
    print("[Hidden Tests] Return code:")
    print(hidden_result.get("return_code"))

    if hidden_result.get("stdout"):
        print()
        print("[Hidden Tests] stdout:")
        print(hidden_result["stdout"])

    if hidden_result.get("stderr"):
        print()
        print("[Hidden Tests] stderr:")
        print(hidden_result["stderr"])

    return hidden_result

# ============================================================
# FAILURE ANALYSIS
# ============================================================

def run_failure_analysis(
    task_id: str,
    attempt_number: int,
    test_result: dict[str, Any],
) -> dict[str, Any]:

    stdout = test_result.get(
        "stdout",
        "",
    )

    stderr = test_result.get(
        "stderr",
        "",
    )

    combined = (
        stdout
        + "\n"
        + stderr
    )

    category = test_result.get(
        "failure_type",
        "unknown",
    )

    likely_cause = (
        "Inspect the failing test output and "
        "identify the smallest implementation change "
        "that addresses the failure."
    )

    if category == "syntax_error":
        likely_cause = (
            "Invalid Python syntax or malformed source."
        )

    elif category == "import_error":
        likely_cause = (
            "Missing dependency, incorrect import, "
            "or incorrect module/package structure."
        )

    elif category == "assertion_failure":
        likely_cause = (
            "Implementation behavior does not match "
            "the expected behavior in the tests."
        )

    elif category == "type_error":
        likely_cause = (
            "A function received or returned an "
            "unexpected type."
        )

    elif category == "name_error":
        likely_cause = (
            "A variable, function, or symbol is missing "
            "or incorrectly named."
        )

    elif category == "attribute_error":
        likely_cause = (
            "Code accesses an attribute that does not "
            "exist on the object."
        )

    elif category == "key_error":
        likely_cause = (
            "A dictionary key is missing or incorrectly "
            "handled."
        )

    elif category == "index_error":
        likely_cause = (
            "Code accesses an invalid list or sequence index."
        )

    elif category == "timeout":
        likely_cause = (
            "The implementation did not complete within "
            "the allowed execution time."
        )

    # Keep a useful excerpt without exploding the trajectory.
    excerpt = combined[-4000:]

    return {
        "task_id": task_id,
        "attempt": attempt_number,
        "category": category,
        "likely_cause": likely_cause,
        "error_excerpt": excerpt,
    }


# ============================================================
# TRAJECTORY LOGGER
# ============================================================

class TrajectoryLogger:

    def __init__(
        self,
        task_id: str,
        agent: str,
        run_number: int,
    ):
        self.task_id = task_id
        self.agent = agent
        self.run_number = run_number

        self.started_at = utc_now()

        self.events: list[dict[str, Any]] = []

    def add(
        self,
        event_type: str,
        data: dict[str, Any] | None = None,
    ) -> None:

        self.events.append(
            {
                "timestamp": utc_now(),
                "event": event_type,
                "data": data or {},
            }
        )

    def save(
        self,
        path: Path,
    ) -> None:

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = {
            "task_id": self.task_id,
            "agent": self.agent,
            "run_number": self.run_number,
            "started_at": self.started_at,
            "finished_at": utc_now(),
            "events": self.events,
        }

        path.write_text(
            json.dumps(
                payload,
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )


# ============================================================
# RESULT STORAGE
# ============================================================

RESULTS_CSV = (
    RESULTS_ROOT / "results_v2.csv"
)

ATTEMPTS_CSV = (
    RESULTS_ROOT / "attempts_v2.csv"
)


RESULT_FIELDS = FINAL_RESULT_FIELDS
ATTEMPT_FIELDS = ATTEMPT_RESULT_FIELDS


def append_csv_row(
    path: Path,
    fields: list[str],
    row: dict[str, Any],
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    exists = path.exists()

    with path.open(
        "a",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )

        if not exists:
            writer.writeheader()

        writer.writerow(
            {
                field: row.get(
                    field,
                    "",
                )
                for field in fields
            }
        )


def append_attempt_result(
    task_id: str,
    agent: str,
    run_number: int,
    attempt_number: int,
    test_result: dict[str, Any],
    generation_success: bool,
    run_id: str,
) -> None:
    record = normalize_attempt_record({
        "schema_version": "2",
        "timestamp": utc_now(),
        "run_id": run_id,
        "attempt_id": new_attempt_id(),
        "task_id": task_id,
        "agent": agent,
        "run_number": run_number,
        "attempt_number": attempt_number,
        "generation_success": generation_success,
        "tests_executed": test_result.get("tests_executed"),
        "tests_passed": test_result.get("passed"),
        "failure_type": test_result.get("failure_type"),
        "error_message": test_result.get("stderr"),
        "exit_code": test_result.get("return_code"),
        "stdout": test_result.get("stdout"),
        "stderr": test_result.get("stderr"),
        "duration_seconds": test_result.get("duration_seconds"),
    })
    issues = validate_attempt_record(record)
    if issues:
        raise ValueError(f"Invalid attempt result: {issues}")
    append_csv_row(ATTEMPTS_CSV, ATTEMPT_FIELDS, record)


def append_final_result(
    result: dict[str, Any],
) -> None:

    record = normalize_final_record({
        **result,
        "schema_version": "2",
        "timestamp": utc_now(),
        "tests_passed": result.get("tests_passed", False),
        "error_message": result.get("stderr", ""),
        "exit_code": result.get("return_code"),
        "timed_out": result.get("timed_out", False),
        "max_attempts": result.get("max_attempts"),
    })
    issues = validate_final_record(record)
    if issues:
        raise ValueError(f"Invalid final result: {issues}")
    append_csv_row(RESULTS_CSV, RESULT_FIELDS, record)


# ============================================================
# AGENT SOLUTION GENERATION
# ============================================================

def generate_solution(
    agent_module: Any,
    task_id: str,
    workspace: Path,
) -> dict[str, Any]:

    if not hasattr(
        agent_module,
        "solve",
    ):
        raise RuntimeError(
            "Agent does not define solve()."
        )

    solve = agent_module.solve

    # Preferred API:
    #
    # solve(task_id, repo_path)
    #
    # Backward compatibility:
    #
    # solve(task_id)
    #

    try:
        solution = solve(
            task_id,
            str(workspace),
        )

    except TypeError as first_error:

        try:
            solution = solve(
                task_id
            )

        except TypeError:
            raise first_error

    return validate_agent_solution(
        solution
    )


# ============================================================
# AGENT REPAIR
# ============================================================

def attempt_repair(
    agent_module: Any,
    task_id: str,
    workspace: Path,
    previous_solution: dict[str, Any],
    test_result: dict[str, Any],
    failure_analysis: dict[str, Any],
) -> dict[str, Any] | None:

    if not hasattr(
        agent_module,
        "repair",
    ):
        return None

    repair = agent_module.repair

    context = {
        "task_id": task_id,
        "workspace": str(workspace),
        "previous_solution": previous_solution,
        "test_result": test_result,
        "failure_analysis": failure_analysis,
    }

    try:
        repaired = repair(
            task_id,
            str(workspace),
            context,
        )

    except TypeError:

        try:
            repaired = repair(
                task_id,
                context,
            )

        except TypeError:

            repaired = repair(
                context
            )

    return validate_agent_solution(
        repaired
    )


# ============================================================
# EVALUATE WITH RETRIES
# ============================================================

def evaluate_with_retries(
    task_id: str,
    agent: str,
    repo_path: Path,
    test_command: str,
    run_number: int,
    max_attempts: int,
) -> dict[str, Any]:

    logger = TrajectoryLogger(
        task_id=task_id,
        agent=agent,
        run_number=run_number,
    )

    evaluation_start = (
        time.perf_counter()
    )

    result: dict[str, Any] = {
        "schema_version": "2",
        "run_id": new_run_id(),
        "task_id": task_id,
        "agent": agent,
        "run_number": run_number,
        "final_success": False,
        "generation_success": False,
        "tests_executed": False,
        "tests_passed": False,
        "recovery_attempted": False,
        "recovery_success": False,
        "attempts_used": 0,
        "max_attempts": max_attempts,
        "duration_seconds": 0,
        "failure_type": "",
        "stdout": "",
        "stderr": "",
        "return_code": None,
        "timed_out": False,
    }

    # --------------------------------------------------------
    # Load agent
    # --------------------------------------------------------

    try:

        logger.add(
            "agent_load_started",
            {
                "agent": agent,
            },
        )

        agent_module = load_agent(
            agent
        )

        logger.add(
            "agent_loaded",
            {},
        )

    except Exception as exc:

        result["failure_type"] = (
            "evaluator_error"
        )

        error_message = (
            f"{type(exc).__name__}: {exc}"
        )

        print()
        print("[EVALUATOR ERROR]")
        print(error_message)
        print(
            traceback.format_exc()
        )

        logger.add(
            "agent_load_failed",
            {
                "error": error_message,
                "traceback": traceback.format_exc(),
            },
        )

        result["duration_seconds"] = round(
            time.perf_counter()
            - evaluation_start,
            4,
        )

        trajectory_path = (
            RESULTS_ROOT
            / f"trajectory_"
            f"{task_id}_"
            f"{agent}_"
            f"run_{run_number}.json"
        )

        logger.save(
            trajectory_path
        )

        append_final_result(
            result
        )

        return result

    # --------------------------------------------------------
    # Generate initial solution
    # --------------------------------------------------------

    try:

        print()
        print(
            "[Agent] Generating solution..."
        )

        logger.add(
            "generation_started",
            {},
        )

        solution = generate_solution(
            agent_module,
            task_id,
            repo_path,
        )

        result["generation_success"] = (
            solution.get(
                "status"
            )
            == "completed"
        )

        logger.add(
            "generation_completed",
            {
                "status": solution.get(
                    "status"
                ),
                "message": solution.get(
                    "message",
                    "",
                ),
                "files": list(
                    solution.get(
                        "files",
                        {},
                    ).keys()
                ),
            },
        )

        print(
            "[Agent] Status:",
            solution.get(
                "status"
            ),
        )

        if solution.get(
            "message"
        ):
            print(
                "[Agent] Message:",
                solution.get(
                    "message"
                ),
            )

        print()
        print(
            "[Agent] Applying solution..."
        )

        written = apply_agent_solution(
            repo_path,
            task_id,
            solution,
        )

        logger.add(
            "solution_applied",
            {
                "files": written,
            },
        )

    except Exception as exc:

        result["failure_type"] = (
            "generation_error"
        )

        result["stderr"] = (
            f"{type(exc).__name__}: {exc}\n"
            + traceback.format_exc()
        )

        print()
        print("[GENERATION ERROR]")
        print(
            result["stderr"]
        )

        logger.add(
            "generation_failed",
            {
                "error": result["stderr"],
            },
        )

        result["duration_seconds"] = round(
            time.perf_counter()
            - evaluation_start,
            4,
        )

        trajectory_path = (
            RESULTS_ROOT
            / f"trajectory_"
            f"{task_id}_"
            f"{agent}_"
            f"run_{run_number}.json"
        )

        logger.save(
            trajectory_path
        )

        append_final_result(
            result
        )

        return result

    # --------------------------------------------------------
    # Test / repair loop
    # --------------------------------------------------------

    current_solution = solution

    for attempt_number in range(
        1,
        max_attempts + 1,
    ):

        print()
        print(
            f"[Attempt {attempt_number}/"
            f"{max_attempts}] Running tests..."
        )

        logger.add(
            "test_started",
            {
                "attempt": attempt_number,
            },
        )

        test_result = run_tests(
            workspace=repo_path,
            task_id=task_id,
            test_command=test_command,
        )

        result["tests_executed"] = test_result.get(
            "tests_executed",
            False,
        )

        result["tests_passed"] = test_result.get(
            "passed",
            False,
        )

        result["attempts_used"] = (
            attempt_number
        )

        result["stdout"] = test_result.get(
            "stdout",
            "",
        )

        result["stderr"] = test_result.get(
            "stderr",
            "",
        )

        result["return_code"] = test_result.get(
            "return_code"
        )

        result["timed_out"] = test_result.get(
            "timed_out",
            False,
        )

        print(
            "[Attempt] Passed:",
            test_result.get(
                "passed"
            ),
        )

        print(
            "[Attempt] Duration:",
            test_result.get(
                "duration_seconds"
            ),
            "seconds",
        )

        logger.add(
            "test_completed",
            {
                "attempt": attempt_number,
                "passed": test_result.get(
                    "passed"
                ),
                "return_code": test_result.get(
                    "return_code"
                ),
                "duration_seconds": test_result.get(
                    "duration_seconds"
                ),
                "failure_type": test_result.get(
                    "failure_type"
                ),
            },
        )

        append_attempt_result(
            task_id=task_id,
            agent=agent,
            run_number=run_number,
            attempt_number=attempt_number,
            test_result=test_result,
            generation_success=result[
                "generation_success"
            ],
            run_id=result["run_id"],
        )

        # ----------------------------------------------------
        # Evaluator error
        # ----------------------------------------------------

        if (
            test_result.get(
                "failure_type"
            )
            == "evaluator_error"
        ):

            result["failure_type"] = (
                "evaluator_error"
            )

            logger.add(
                "evaluator_error",
                {
                    "attempt": attempt_number,
                    "stdout": test_result.get(
                        "stdout",
                        "",
                    ),
                    "stderr": test_result.get(
                        "stderr",
                        "",
                    ),
                },
            )

            print()
            print(
                "[EVALUATOR ERROR]"
            )
            print(
                test_result.get(
                    "stderr",
                    "",
                )
            )

            break

        # ----------------------------------------------------
        # Visible tests passed
        # ----------------------------------------------------

        if test_result.get(
            "passed"
        ):

            print()
            print(
                f"[PASS] Attempt "
                f"{attempt_number}"
            )

            # ----------------------------------------------
            # Run hidden tests if available
            # ----------------------------------------------

            hidden_result = run_hidden_tests(
                repo_path,
                task_id,
            )

            if hidden_result is not None:

                result["tests_executed"] = hidden_result.get(
                    "tests_executed",
                    True,
                )

                result["tests_passed"] = hidden_result.get(
                    "passed",
                    False,
                )

                result["stdout"] = hidden_result.get(
                    "stdout",
                    "",
                )

                result["stderr"] = hidden_result.get(
                    "stderr",
                    "",
                )

                result["return_code"] = hidden_result.get(
                    "return_code"
                )

                result["timed_out"] = hidden_result.get(
                    "timed_out",
                    False,
                )

                print()
                print(
                    "[Hidden Tests] Running..."
                )

                logger.add(
                    "hidden_tests_started",
                    {
                        "attempt": attempt_number,
                    },
                )

                print(
                    "[Hidden Tests] Passed:",
                    hidden_result.get(
                        "passed"
                    ),
                )

                logger.add(
                    "hidden_tests_completed",
                    {
                        "passed": hidden_result.get(
                            "passed"
                        ),
                        "return_code": hidden_result.get(
                            "return_code"
                        ),
                        "duration_seconds": hidden_result.get(
                            "duration_seconds"
                        ),
                        "failure_type": hidden_result.get(
                            "failure_type"
                        ),
                    },
                )

                if not hidden_result.get(
                    "passed"
                ):

                    # Hidden test failure means the task
                    # is not actually solved.

                    result["failure_type"] = (
                        "hidden_test_failure"
                    )

                    hidden_analysis = (
                        run_failure_analysis(
                            task_id,
                            attempt_number,
                            hidden_result,
                        )
                    )

                    logger.add(
                        "hidden_test_failure_analysis",
                        hidden_analysis,
                    )

                    # Use hidden failure as the next
                    # repair signal.
                    test_result = hidden_result

                else:

                    result[
                        "final_success"
                    ] = True

                    result[
                        "failure_type"
                    ] = "success"

                    if result[
                        "recovery_attempted"
                    ]:
                        result[
                            "recovery_success"
                        ] = True

                    break

            else:

                result[
                    "final_success"
                ] = True

                result[
                    "failure_type"
                ] = "success"

                if result[
                    "recovery_attempted"
                ]:
                    result[
                        "recovery_success"
                    ] = True

                break

        # ----------------------------------------------------
        # Normal failure
        # ----------------------------------------------------

        result["failure_type"] = (
            test_result.get(
                "failure_type",
                "test_failure",
            )
        )

        failure_analysis = (
            run_failure_analysis(
                task_id,
                attempt_number,
                test_result,
            )
        )

        logger.add(
            "failure_analysis",
            failure_analysis,
        )

        print()
        print(
            "[FAIL] Test failure:"
        )
        print(
            failure_analysis[
                "category"
            ]
        )

        # ----------------------------------------------------
        # Maximum attempts reached
        # ----------------------------------------------------

        if attempt_number >= max_attempts:
            print()
            print(
                "[STOP] Maximum attempts reached."
            )

            logger.add(
                "max_attempts_reached",
                {},
            )

            break

        # ----------------------------------------------------
        # Try repair
        # ----------------------------------------------------

        print()
        print(
            "[Recovery] Attempting repair..."
        )

        logger.add(
            "recovery_started",
            {
                "attempt": attempt_number,
            },
        )

        try:

            repaired_solution = (
                attempt_repair(
                    agent_module=agent_module,
                    task_id=task_id,
                    workspace=repo_path,
                    previous_solution=current_solution,
                    test_result=test_result,
                    failure_analysis=failure_analysis,
                )
            )

        except Exception as exc:

            repaired_solution = None

            logger.add(
                "recovery_failed",
                {
                    "error": (
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    ),
                    "traceback": traceback.format_exc(),
                },
            )

            print()
            print(
                "[Recovery Error]"
            )
            print(
                traceback.format_exc()
            )

        if repaired_solution is None:

            print(
                "[Recovery] Agent does not "
                "provide repair()."
            )

            result[
                "failure_type"
            ] = "recovery_not_implemented"

            logger.add(
                "recovery_not_implemented",
                {},
            )

            break

        result[
            "recovery_attempted"
        ] = True

        current_solution = (
            repaired_solution
        )

        logger.add(
            "recovery_completed",
            {
                "status": repaired_solution.get(
                    "status"
                ),
                "files": list(
                    repaired_solution.get(
                        "files",
                        {},
                    ).keys()
                ),
            },
        )

        print(
            "[Recovery] Status:",
            repaired_solution.get(
                "status"
            ),
        )

        print()
        print(
            "[Recovery] Applying repaired solution..."
        )

        try:

            repaired_files = (
                apply_agent_solution(
                    repo_path,
                    task_id,
                    repaired_solution,
                )
            )

            logger.add(
                "repaired_solution_applied",
                {
                    "files": repaired_files,
                },
            )

        except Exception as exc:

            result[
                "failure_type"
            ] = "repair_application_error"

            logger.add(
                "repair_application_failed",
                {
                    "error": (
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    ),
                    "traceback": traceback.format_exc(),
                },
            )

            print(
                "[Recovery Error]"
            )
            print(
                traceback.format_exc()
            )

            break

    # --------------------------------------------------------
    # Finalize
    # --------------------------------------------------------

    result["duration_seconds"] = round(
        time.perf_counter()
        - evaluation_start,
        4,
    )

    if result[
        "final_success"
    ]:

        result[
            "failure_type"
        ] = "success"

    logger.add(
        "evaluation_finished",
        {
            "final_success": result[
                "final_success"
            ],
            "attempts_used": result[
                "attempts_used"
            ],
            "failure_type": result[
                "failure_type"
            ],
        },
    )

    trajectory_path = (
        RESULTS_ROOT
        / f"trajectory_"
        f"{task_id}_"
        f"{agent}_"
        f"run_{run_number}.json"
    )

    logger.save(
        trajectory_path
    )

    append_final_result(
        result
    )

    return result


# ============================================================
# RUN ONE AGENT
# ============================================================

def run_agent(
    task_id: str,
    agent: str,
    run_number: int,
) -> dict[str, Any]:

    print()
    print("=" * 70)
    print(
        f"EVALUATION: {task_id} | "
        f"{agent} | run {run_number}"
    )
    print("=" * 70)

    workspace = create_clean_workspace(
        task_id,
        agent,
        run_number,
    )

    print(
        "Workspace:",
        workspace,
    )

    test_command = (
        discover_test_command(
            task_id
        )
    )

    print(
        "Test command:",
        test_command,
    )

    result = evaluate_with_retries(
        task_id=task_id,
        agent=agent,
        repo_path=workspace,
        test_command=test_command,
        run_number=run_number,
        max_attempts=MAX_ATTEMPTS,
    )

    print()
    print("-" * 70)
    print(
        f"[RESULT] {agent} run "
        f"{run_number}: "
        f"{'PASS' if result['final_success'] else 'FAIL'}"
    )

    print(
        "Failure Type:",
        result.get(
            "failure_type",
            "",
        ),
    )

    print(
        "Generation Success:",
        result.get(
            "generation_success",
            False,
        ),
    )

    print(
        "Tests Executed:",
        result.get(
            "tests_executed",
            False,
        ),
    )

    print(
        "Recovery Attempted:",
        result.get(
            "recovery_attempted",
            False,
        ),
    )

    print(
        "Recovery Success:",
        result.get(
            "recovery_success",
            False,
        ),
    )

    print(
        "Attempts Used:",
        result.get(
            "attempts_used",
            0,
        ),
    )

    print(
        "Duration:",
        result.get(
            "duration_seconds",
            0,
        ),
        "seconds",
    )

    print("-" * 70)

    if result.get("stdout"):
        print()
        print("Test Output:")
        print(
            result[
                "stdout"
            ]
        )

    if result.get("stderr"):
        print()
        print("Errors:")
        print(
            result[
                "stderr"
            ]
        )

    return result


# ============================================================
# EVALUATE ONE TASK
# ============================================================

def evaluate_task(
    task_id: str,
    agents: list[str],
    runs_per_agent: int,
) -> list[dict[str, Any]]:

    if task_id not in TASKS:
        raise ValueError(
            f"Unknown task: {task_id}"
        )

    results: list[dict[str, Any]] = []

    print()
    print("#" * 70)
    print(
        f"EVALUATING {task_id}"
    )
    print("#" * 70)

    for agent in agents:

        for run_number in range(
            1,
            runs_per_agent + 1,
        ):

            result = run_agent(
                task_id=task_id,
                agent=agent,
                run_number=run_number,
            )

            results.append(
                result
            )

    return results


# ============================================================
# SUMMARY
# ============================================================

def print_summary(
    results: list[dict[str, Any]],
) -> None:

    print()
    print("=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(
        f"{'Task':<10}"
        f"{'Agent':<15}"
        f"{'Runs':<8}"
        f"{'Success':<10}"
        f"{'Rate':<10}"
        f"{'Time':<10}"
    )

    print("-" * 70)

    grouped: dict[
        tuple[str, str],
        list[dict[str, Any]],
    ] = {}

    for result in results:

        key = (
            result["task_id"],
            result["agent"],
        )

        grouped.setdefault(
            key,
            [],
        ).append(result)

    for (
        task_id,
        agent,
    ), group in grouped.items():

        runs = len(group)

        successes = sum(
            1
            for item in group
            if item.get(
                "final_success",
                False,
            )
        )

        rate = (
            successes / runs * 100
            if runs
            else 0
        )

        total_time = sum(
            float(
                item.get(
                    "duration_seconds",
                    0,
                )
            )
            for item in group
        )

        avg_time = (
            total_time / runs
            if runs
            else 0
        )

        print(
            f"{task_id:<10}"
            f"{agent:<15}"
            f"{runs:<8}"
            f"{successes:<10}"
            f"{rate:>6.1f}%   "
            f"{avg_time:>7.2f}s"
        )

    print()
    print("=" * 70)
    print(
        f"Final results: "
        f"{RESULTS_CSV}"
    )
    print(
        f"Attempt results: "
        f"{ATTEMPTS_CSV}"
    )
    print("=" * 70)


# ============================================================
# RESET RESULTS
# ============================================================

def reset_results() -> None:

    removed = False

    for path in [
        RESULTS_CSV,
        ATTEMPTS_CSV,
    ]:

        if path.exists():
            path.unlink()
            removed = True

    if RESULTS_ROOT.exists():

        for path in RESULTS_ROOT.glob(
            "trajectory_*.json"
        ):
            try:
                path.unlink()
                removed = True
            except Exception:
                pass

    if removed:
        print(
            "[OK] Previous evaluation "
            "results removed."
        )
    else:
        print(
            "[OK] No previous results to remove."
        )


# ============================================================
# CLEAN WORKSPACES
# ============================================================

def clean_workspaces() -> None:

    if not WORKSPACES_ROOT.exists():
        return

    for path in WORKSPACES_ROOT.iterdir():

        if path.is_dir():

            try:
                shutil.rmtree(path)
            except Exception:
                pass


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    ensure_directories()

    parser = argparse.ArgumentParser(
        description=(
            "AI Agent Evaluation Benchmark"
        )
    )

    parser.add_argument(
        "--task",
        help=(
            "Run only a specific task, "
            "for example task_10"
        ),
    )

    parser.add_argument(
        "--agent",
        help=(
            "Run only a specific agent, "
            "for example agent_02"
        ),
    )

    parser.add_argument(
        "--runs",
        type=int,
        default=RUNS_PER_AGENT,
        help=(
            "Number of runs per agent"
        ),
    )

    parser.add_argument(
        "--skip-precheck",
        action="store_true",
        help=(
            "Skip task configuration pre-check"
        ),
    )

    parser.add_argument(
        "--reset-results",
        action="store_true",
        help=(
            "Delete previous results "
            "before evaluation"
        ),
    )

    parser.add_argument(
        "--clean-workspaces",
        action="store_true",
        help=(
            "Delete existing workspaces "
            "before evaluation"
        ),
    )

    args = parser.parse_args()

    # --------------------------------------------------------
    # Validate task argument
    # --------------------------------------------------------

    if args.task:

        if args.task not in TASKS:

            print()
            print(
                f"ERROR: Unknown task: "
                f"{args.task}"
            )

            print()
            print(
                "Available tasks:"
            )

            for task_id in TASKS:
                print(
                    f"  {task_id}"
                )

            sys.exit(1)

    # --------------------------------------------------------
    # Validate agent argument
    # --------------------------------------------------------

    selected_agents = AGENTS.copy()

    if args.agent:

        if args.agent not in AGENTS:

            print()
            print(
                f"ERROR: Unknown agent: "
                f"{args.agent}"
            )

            print()
            print(
                "Available agents:"
            )

            for agent in AGENTS:
                print(
                    f"  {agent}"
                )

            sys.exit(1)

        selected_agents = [
            args.agent
        ]

    # --------------------------------------------------------
    # Runs
    # --------------------------------------------------------

    if args.runs < 1:

        print(
            "ERROR: --runs must be >= 1"
        )

        sys.exit(1)

    # --------------------------------------------------------
    # Reset results
    # --------------------------------------------------------

    if args.reset_results:
        reset_results()

    # --------------------------------------------------------
    # Clean workspaces
    # --------------------------------------------------------

    if args.clean_workspaces:
        clean_workspaces()

    # --------------------------------------------------------
    # Banner
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print(
        "AI AGENT EVALUATION BENCHMARK"
    )
    print("=" * 70)

    print(
        "Project root:",
        PROJECT_ROOT,
    )

    print(
        "Tasks configured:",
        len(TASKS),
    )

    print(
        "Agents:",
        ", ".join(
            selected_agents
        ),
    )

    print(
        "Runs per agent:",
        args.runs,
    )

    print(
        "Maximum attempts:",
        MAX_ATTEMPTS,
    )

    print("=" * 70)

    # --------------------------------------------------------
    # Determine selected tasks
    # --------------------------------------------------------

    if args.task:
        selected_tasks = [
            args.task
        ]
    else:
        selected_tasks = list(
            TASKS.keys()
        )

    # --------------------------------------------------------
    # Validate configuration
    # --------------------------------------------------------

    if not args.skip_precheck:

        valid = validate_tasks(
            selected_tasks
        )

        if not valid:

            print()
            print(
                "=" * 70
            )
            print(
                "EVALUATION STOPPED"
            )
            print(
                "Fix the invalid task "
                "configuration first."
            )
            print(
                "=" * 70
            )

            sys.exit(1)

    else:

        print()
        print(
            "Skipping task pre-check."
        )

    # --------------------------------------------------------
    # Run benchmark
    # --------------------------------------------------------

    all_results: list[
        dict[str, Any]
    ] = []

    for task_id in selected_tasks:

        task_results = evaluate_task(
            task_id=task_id,
            agents=selected_agents,
            runs_per_agent=args.runs,
        )

        all_results.extend(
            task_results
        )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print_summary(
        all_results
    )

    print()
    print(
        "=" * 70
    )
    print(
        "EVALUATION FINISHED"
    )
    print(
        "=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
