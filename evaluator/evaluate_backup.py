import subprocess
import time
import csv
import os
import shutil
import importlib.util
import sys
import argparse
from pathlib import Path

from trajectory import TrajectoryLogger


# ============================================================
# TASK CONFIGURATION
# ============================================================

TASKS = {
    "task_01": {
        "repo_path": "tasks/task_01",
        "test_command": "python -m pytest test_calculator.py",
    },

    "task_02": {
        "repo_path": "tasks/task_02",
        "test_command": "python -m pytest test_string_utils.py",
    },

    "task_03": {
        "repo_path": "tasks/task_03",
        "test_command": "python -m pytest test_data_utils.py",
    },

    "task_04": {
        "repo_path": "tasks/task_04",
        "test_command": "python -m pytest test_json_utils.py",
    },

    "task_05": {
        "repo_path": "tasks/task_05",
        "test_command": "python -m pytest test_discount.py",
    },

    "task_06": {
        "repo_path": "tasks/task_06",
        "test_command": "python -m pytest test_list_utils.py",
    },

    "task_07": {
        "repo_path": "tasks/task_07",
        "test_command": "python -m pytest test_dict_utils.py",
    },

    "task_08": {
        "repo_path": "tasks/task_08",
        "test_command": "python -m pytest test_text_utils.py",
    },

    "task_09": {
        "repo_path": "tasks/task_09",
        "test_command": "python -m pytest test_url_utils.py",
    },

    "task_10": {
        "repo_path": "tasks/task_10",
        "test_command": "python -m pytest test_csv_utils.py",
    },

    "task_11": {
        "repo_path": "tasks/task_11",
        "test_command": "python -m pytest test_file_utils.py",
    },

    "task_12": {
        "repo_path": "tasks/task_12",
        "test_command": "python -m pytest test_config_utils.py",
    },

    "task_13": {
        "repo_path": "tasks/task_13",
        "test_command": "python -m pytest test_validation_utils.py",
    },

    "task_14": {
        "repo_path": "tasks/task_14",
        "test_command": "python -m pytest test_string_utils.py",
    },

    "task_15": {
        "repo_path": "tasks/task_15",
        "test_command": "python -m pytest test_sql_utils.py",
    },

    "task_16": {
        "repo_path": "tasks/task_16",
        "test_command": "python -m pytest test_auth_utils.py",
    },

    "task_17": {
        "repo_path": "tasks/task_17",
        "test_command": "python -m pytest test_retry_utils.py",
    },

    "task_18": {
        "repo_path": "tasks/task_18",
        "test_command": "python -m pytest test_cache_utils.py",
    },

    "task_19": {
        "repo_path": "tasks/task_19",
        "test_command": "python -m pytest test_bug_utils.py",
    },

    "task_20": {
        "repo_path": "tasks/task_20",
        "test_command": "python -m pytest test_feature.py",
    },

    "task_21": {
        "repo_path": "tasks/task_21",
        "test_command": "python -m pytest test_text_utils.py",
    },

    "task_22": {
        "repo_path": "tasks/task_22",
        "test_command": (
            "python -m pytest "
            "test_cache_utils.py "
            "test_config_utils.py"
        ),
    },

    "task_23": {
        "repo_path": "tasks/task_23",
        "test_command": "python -m pytest test_file_utils.py",
    },

    "task_24": {
        "repo_path": "tasks/task_24",
        "test_command": "python -m pytest test_json_utils.py",
    },

    "task_25": {
        "repo_path": "tasks/task_25",
        "test_command": "python -m pytest test_date_utils.py",
    },

    "task_26": {
        "repo_path": "tasks/task_26",
        "test_command": "python -m pytest test_price_utils.py",
    },

    "task_27": {
        "repo_path": "tasks/task_27",
        "test_command": "python -m pytest test_user_utils.py",
    },

    "task_28": {
        "repo_path": "tasks/task_28",
        "test_command": "python -m pytest test_number_utils.py",
    },

    "task_29": {
        "repo_path": "tasks/task_29",
        "test_command": "python -m pytest test_task_29.py",
    },

    "task_30": {
        "repo_path": "tasks/task_30",
        "test_command": "python -m pytest test_order.py",
    },

    "task_31": {
        "repo_path": "tasks/task_31",
        "test_command": "python -m pytest test_user_utils.py",
    },

    "task_32": {
        "repo_path": "tasks/task_32",
        "test_command": "python -m pytest test_client.py",
    },
}


# ============================================================
# AGENTS
# ============================================================

AGENTS = [
    "baseline",
    "agent_02",
]


# ============================================================
# EVALUATION SETTINGS
# ============================================================

RUNS_PER_AGENT = 5
MAX_ATTEMPTS = 3


# ============================================================
# LOAD AGENT
# ============================================================

def load_agent(agent_name):
    """
    Dynamically load an agent module.
    """

    agent_path = os.path.join(
        "agents",
        f"{agent_name}.py",
    )

    if not os.path.exists(agent_path):
        raise FileNotFoundError(
            f"Agent not found: {agent_path}"
        )

    spec = importlib.util.spec_from_file_location(
        agent_name,
        agent_path,
    )

    if spec is None or spec.loader is None:
        raise ImportError(
            f"Could not load agent: {agent_path}"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[agent_name] = module

    spec.loader.exec_module(module)

    return module


# ============================================================
# HIDDEN TEST LAUNCHER
# ============================================================

def run_hidden_tests(
    hidden_test_path,
    workspace_path,
):
    """
    Run hidden tests in an isolated workspace.
    """

    workspace_abs = os.path.abspath(
        workspace_path
    )

    hidden_test_abs = os.path.abspath(
        hidden_test_path
    )

    env = os.environ.copy()

    existing_pythonpath = env.get(
        "PYTHONPATH",
        "",
    )

    if existing_pythonpath:
        env["PYTHONPATH"] = (
            workspace_abs
            + os.pathsep
            + existing_pythonpath
        )
    else:
        env["PYTHONPATH"] = workspace_abs

    for cache_dir in Path(
        workspace_abs
    ).rglob("__pycache__"):

        shutil.rmtree(
            cache_dir,
            ignore_errors=True,
        )

    launcher = (
        "import sys; "
        "sys.path.insert(0, "
        + repr(workspace_abs)
        + "); "
        "import pytest; "
        "raise SystemExit("
        "pytest.main(["
        + repr(hidden_test_abs)
        + ", "
        "'--confcutdir', "
        + repr(workspace_abs)
        + "])"
        ")"
    )

    return subprocess.run(
        [
            sys.executable,
            "-c",
            launcher,
        ],
        cwd=workspace_abs,
        capture_output=True,
        text=True,
        env=env,
    )


# ============================================================
# RUN TESTS
# ============================================================

def run_tests(
    repo_path,
    test_command,
    task_id=None,
    include_hidden=False,
):
    """
    Run visible and optional hidden tests in an isolated
    workspace.
    """

    start = time.time()

    workspace_abs = os.path.abspath(
        repo_path
    )

    env = os.environ.copy()

    existing_pythonpath = env.get(
        "PYTHONPATH",
        "",
    )

    if existing_pythonpath:
        env["PYTHONPATH"] = (
            workspace_abs
            + os.pathsep
            + existing_pythonpath
        )
    else:
        env["PYTHONPATH"] = workspace_abs

    for cache_dir in Path(
        workspace_abs
    ).rglob("__pycache__"):

        shutil.rmtree(
            cache_dir,
            ignore_errors=True,
        )

    visible_command = test_command

    if isinstance(
        visible_command,
        str,
    ):

        if "pytest" in visible_command:

            if "--confcutdir" not in visible_command:

                visible_command = (
                    visible_command
                    + ' --confcutdir "'
                    + workspace_abs
                    + '"'
                )

    commands = [
        visible_command
    ]

    if (
        include_hidden
        and task_id
    ):

        hidden_test = os.path.join(
            "evaluator",
            "hidden_tests",
            f"test_{task_id}_hidden.py",
        )

        if os.path.exists(
            hidden_test
        ):

            hidden_test_abs = os.path.abspath(
                hidden_test
            )

            commands.append(
                (
                    "HIDDEN_TEST",
                    hidden_test_abs,
                )
            )

    outputs = []
    errors = []
    returncodes = []

    all_passed = True
    tests_executed = True

    for command in commands:

        if (
            isinstance(
                command,
                tuple,
            )
            and command[0] == "HIDDEN_TEST"
        ):

            result = run_hidden_tests(
                command[1],
                repo_path,
            )

        else:

            result = subprocess.run(
                command,
                cwd=workspace_abs,
                shell=True,
                capture_output=True,
                text=True,
                env=env,
            )

        returncodes.append(
            result.returncode
        )

        if result.stdout:
            outputs.append(
                result.stdout
            )

        if result.stderr:
            errors.append(
                result.stderr
            )

        if result.returncode != 0:
            all_passed = False

    elapsed = time.time() - start

    failed_returncode = next(
        (
            code
            for code in returncodes
            if code != 0
        ),
        0,
    )

    combined_output = "\n".join(
        outputs + errors
    )

    # --------------------------------------------------------
    # Detect test/evaluator errors
    # --------------------------------------------------------

    evaluator_error = False

    evaluator_error_patterns = [
        "ModuleNotFoundError",
        "ImportError",
        "SyntaxError",
        "conftest.py",
        "pytest internal error",
        "INTERNALERROR",
    ]

    for pattern in evaluator_error_patterns:

        if pattern in combined_output:

            evaluator_error = True
            break

    failure_type = ""

    if all_passed:

        failure_type = "success"

    elif evaluator_error:

        failure_type = "evaluator_error"

    else:

        failure_type = "test_failure"

    return {
        "passed": all_passed,
        "duration_seconds": round(
            elapsed,
            2,
        ),
        "stdout": "\n".join(
            outputs
        ),
        "stderr": "\n".join(
            errors
        ),
        "returncode": (
            0
            if all_passed
            else failed_returncode
        ),
        "tests_executed": tests_executed,
        "failure_type": failure_type,
    }


# ============================================================
# CREATE CLEAN WORKSPACE
# ============================================================

def create_clean_workspace(
    task_id,
    agent,
    run_number,
):
    """
    Create a completely fresh workspace for one
    agent/task/run combination.
    """

    source = TASKS[
        task_id
    ][
        "repo_path"
    ]

    workspace_root = "workspaces"

    os.makedirs(
        workspace_root,
        exist_ok=True,
    )

    workspace = os.path.join(
        workspace_root,
        f"{task_id}_{agent}_{run_number}",
    )

    if os.path.exists(
        workspace
    ):

        shutil.rmtree(
            workspace
        )

    shutil.copytree(
        source,
        workspace,
    )

    return workspace


# ============================================================
# APPLY AGENT SOLUTION
# ============================================================

def apply_agent_solution(
    repo_path,
    solution,
):
    """
    Write files generated by an agent into the isolated
    workspace.
    """

    if not isinstance(
        solution,
        dict,
    ):

        print(
            "Invalid solution returned by agent."
        )

        return

    files = solution.get(
        "files",
        {},
    )

    if not files:

        print(
            "No files generated by agent."
        )

        return

    absolute_repo = os.path.abspath(
        repo_path
    )

    for filename, content in files.items():

        file_path = os.path.join(
            repo_path,
            filename,
        )

        absolute_file = os.path.abspath(
            file_path
        )

        print(
            "Writing:",
            file_path,
        )

        try:

            common_path = os.path.commonpath(
                [
                    absolute_repo,
                    absolute_file,
                ]
            )

        except ValueError:

            raise ValueError(
                f"Invalid file path: {filename}"
            )

        if common_path != absolute_repo:

            raise ValueError(
                f"Invalid file path: {filename}"
            )

        parent = os.path.dirname(
            file_path
        )

        os.makedirs(
            parent,
            exist_ok=True,
        )

        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                content
            )


# ============================================================
# SAVE RESULT
# ============================================================

def save_result(
    result,
    task_id,
    agent,
    run_number,
    attempt,
):
    """
    Append one evaluation attempt to results.csv.
    """

    os.makedirs(
        "results",
        exist_ok=True,
    )

    file_path = os.path.join(
        "results",
        "results.csv",
    )

    file_exists = os.path.exists(
        file_path
    )

    with open(
        file_path,
        "a",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(
            file
        )

        if not file_exists:

            writer.writerow(
                [
                    "task_id",
                    "agent",
                    "run",
                    "attempt",
                    "passed",
                    "duration_seconds",
                    "failure_type",
                    "tests_executed",
                    "recovery_attempted",
                    "recovery_success",
                    "final_success",
                    "attempts_used",
                ]
            )

        writer.writerow(
            [
                task_id,
                agent,
                run_number,
                attempt,
                result.get(
                    "passed",
                    False,
                ),
                result.get(
                    "duration_seconds",
                    0,
                ),
                result.get(
                    "failure_type",
                    "",
                ),
                result.get(
                    "tests_executed",
                    "",
                ),
                result.get(
                    "recovery_attempted",
                    False,
                ),
                result.get(
                    "recovery_success",
                    "",
                ),
                result.get(
                    "final_success",
                    result.get(
                        "passed",
                        False,
                    ),
                ),
                result.get(
                    "attempts_used",
                    attempt,
                ),
            ]
        )


# ============================================================
# EVALUATE WITH RETRIES
# ============================================================

def evaluate_with_retries(
    task_id,
    agent,
    repo_path,
    test_command,
    run_number,
    max_attempts=3,
):
    """
    Evaluate an agent with recovery attempts.
    """

    logger = TrajectoryLogger()

    recovery_attempted = False
    recovery_success = False
    generation_success = False
    attempts_used = 0

    # --------------------------------------------------------
    # Protect benchmark tests
    # --------------------------------------------------------

    logger.log_event(
        "benchmark_tests_protected",
        {
            "task_id": task_id,
            "agent": agent,
            "run": run_number,
        },
    )

    # --------------------------------------------------------
    # Load agent
    # --------------------------------------------------------

    try:

        agent_module = load_agent(
            agent
        )

    except Exception as exc:

        print()
        print(
            "❌ Failed to load agent:"
        )
        print(
            str(exc)
        )

        return {
            "passed": False,
            "duration_seconds": 0,
            "stdout": "",
            "stderr": str(exc),
            "returncode": 1,
            "tests_executed": False,
            "failure_type": "generation_error",
            "recovery_attempted": False,
            "recovery_success": False,
            "final_success": False,
            "attempts_used": 0,
        }

    # --------------------------------------------------------
    # Generate initial solution
    # --------------------------------------------------------

    print()
    print(
        "Generating solution..."
    )

    try:

        solution = agent_module.solve(
            task_id,
            repo_path,
        )

        generation_success = True

    except TypeError:

        try:

            solution = agent_module.solve(
                task_id
            )

            generation_success = True

        except Exception as exc:

            print()
            print(
                "❌ Agent crashed while generating solution:"
            )
            print(
                str(exc)
            )

            logger.log_event(
                "solution_generation_failed",
                {
                    "task_id": task_id,
                    "agent": agent,
                    "run": run_number,
                    "error": str(exc),
                },
            )

            return {
                "passed": False,
                "duration_seconds": 0,
                "stdout": "",
                "stderr": str(exc),
                "returncode": 1,
                "tests_executed": False,
                "failure_type": "generation_error",
                "recovery_attempted": False,
                "recovery_success": False,
                "final_success": False,
                "attempts_used": 0,
            }

    except Exception as exc:

        print()
        print(
            "❌ Agent crashed while generating solution:"
        )
        print(
            str(exc)
        )

        logger.log_event(
            "solution_generation_failed",
            {
                "task_id": task_id,
                "agent": agent,
                "run": run_number,
                "error": str(exc),
            },
        )

        return {
            "passed": False,
            "duration_seconds": 0,
            "stdout": "",
            "stderr": str(exc),
            "returncode": 1,
            "tests_executed": False,
            "failure_type": "generation_error",
            "recovery_attempted": False,
            "recovery_success": False,
            "final_success": False,
            "attempts_used": 0,
        }

    print(
        "Agent status:",
        solution.get(
            "status"
        ),
    )

    logger.log_event(
        "solution_generated",
        {
            "task_id": task_id,
            "agent": agent,
            "run": run_number,
            "status": solution.get(
                "status"
            ),
            "files": list(
                solution.get(
                    "files",
                    {},
                ).keys()
            ),
        },
    )

    # --------------------------------------------------------
    # Check agent status
    # --------------------------------------------------------

    if solution.get(
        "status"
    ) != "completed":

        message = solution.get(
            "message",
            "Agent failed to generate solution.",
        )

        print()
        print(
            "❌ Agent failed to generate solution."
        )
        print(
            message
        )

        return {
            "passed": False,
            "duration_seconds": 0,
            "stdout": "",
            "stderr": message,
            "returncode": 1,
            "tests_executed": False,
            "failure_type": "agent_not_implemented",
            "recovery_attempted": False,
            "recovery_success": False,
            "final_success": False,
            "attempts_used": 0,
        }

    # --------------------------------------------------------
    # Apply initial solution
    # --------------------------------------------------------

    print()
    print(
        "Applying agent solution..."
    )

    try:

        apply_agent_solution(
            repo_path,
            solution,
        )

    except Exception as exc:

        print(
            "❌ Failed to apply agent solution:"
        )
        print(
            str(exc)
        )

        return {
            "passed": False,
            "duration_seconds": 0,
            "stdout": "",
            "stderr": str(exc),
            "returncode": 1,
            "tests_executed": False,
            "failure_type": "generation_error",
            "recovery_attempted": False,
            "recovery_success": False,
            "final_success": False,
            "attempts_used": 0,
        }

    logger.log_event(
        "solution_applied",
        {
            "files": list(
                solution.get(
                    "files",
                    {},
                ).keys()
            ),
        },
    )

    # --------------------------------------------------------
    # Attempt loop
    # --------------------------------------------------------

    result = None

    for attempt in range(
        1,
        max_attempts + 1,
    ):

        attempts_used = attempt

        print()
        print(
            f"Attempt {attempt}/{max_attempts}"
        )

        logger.log_event(
            "attempt_started",
            {
                "task_id": task_id,
                "agent": agent,
                "run": run_number,
                "attempt": attempt,
            },
        )

        print(
            "Running tests..."
        )

        result = run_tests(
            repo_path=repo_path,
            test_command=test_command,
            task_id=task_id,
            include_hidden=True,
        )

        print(
            "Passed:",
            result["passed"],
        )

        print(
            "Duration:",
            result["duration_seconds"],
            "seconds",
        )

        # ----------------------------------------------------
        # Attach evaluation metadata
        # ----------------------------------------------------

        result["recovery_attempted"] = recovery_attempted
        result["recovery_success"] = recovery_success
        result["final_success"] = result["passed"]
        result["attempts_used"] = attempt
        result["generation_success"] = generation_success

        # ----------------------------------------------------
        # Save result
        # ----------------------------------------------------

        save_result(
            result,
            task_id,
            agent,
            run_number,
            attempt,
        )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if result["passed"]:

            if recovery_attempted:
                recovery_success = True

            result["recovery_attempted"] = recovery_attempted
            result["recovery_success"] = recovery_success
            result["final_success"] = True
            result["attempts_used"] = attempt

            logger.log_event(
                "attempt_passed",
                {
                    "attempt": attempt,
                    "duration_seconds":
                        result[
                            "duration_seconds"
                        ],
                },
            )

            logger.log_event(
                "task_completed",
                {
                    "attempts_used": attempt,
                    "passed": True,
                },
            )

            trajectory_path = os.path.join(
                "results",
                (
                    f"trajectory_"
                    f"{task_id}_"
                    f"{agent}_"
                    f"run_{run_number}.json"
                ),
            )

            logger.save(
                trajectory_path
            )

            return result

        # ----------------------------------------------------
        # FAILURE
        # ----------------------------------------------------

        logger.log_event(
            "attempt_failed",
            {
                "attempt": attempt,
                "passed": False,
                "stdout": result[
                    "stdout"
                ],
                "stderr": result[
                    "stderr"
                ],
                "returncode": result[
                    "returncode"
                ],
            },
        )

        # ----------------------------------------------------
        # Evaluator error
        # ----------------------------------------------------

        if result.get(
            "failure_type"
        ) == "evaluator_error":

            print()
            print(
                "⚠️ Evaluator error detected."
            )

            result["final_success"] = False

            break

        # ----------------------------------------------------
        # No more attempts
        # ----------------------------------------------------

        if attempt >= max_attempts:

            break

        # ----------------------------------------------------
        # Recovery
        # --------------------------------------------------------

        print()
        print(
            "Test failed."
        )

        if not hasattr(
            agent_module,
            "repair",
        ):

            print(
                "Agent does not implement repair()."
            )

            logger.log_event(
                "recovery_failed",
                {
                    "attempt": attempt,
                    "reason":
                        "repair() not implemented",
                },
            )

            result["failure_type"] = (
                "recovery_failure"
            )

            break

        recovery_attempted = True

        print(
            "Starting recovery..."
        )

        failure_feedback = {
            "task_id": task_id,
            "agent": agent,
            "run": run_number,
            "attempt": attempt,
            "passed": result[
                "passed"
            ],
            "stdout": result[
                "stdout"
            ],
            "stderr": result[
                "stderr"
            ],
            "returncode": result[
                "returncode"
            ],
        }

        logger.log_event(
            "recovery_started",
            failure_feedback,
        )

        try:

            repaired_solution = (
                agent_module.repair(
                    task_id,
                    repo_path,
                    failure_feedback,
                )
            )

        except TypeError:

            try:

                repaired_solution = (
                    agent_module.repair(
                        task_id,
                        failure_feedback,
                    )
                )

            except Exception as exc:

                print(
                    "Recovery failed:",
                    str(exc),
                )

                logger.log_event(
                    "recovery_failed",
                    {
                        "attempt": attempt,
                        "error": str(exc),
                    },
                )

                result["failure_type"] = (
                    "recovery_failure"
                )

                break

        except Exception as exc:

            print(
                "Recovery failed:",
                str(exc),
            )

            logger.log_event(
                "recovery_failed",
                {
                    "attempt": attempt,
                    "error": str(exc),
                },
            )

            result["failure_type"] = (
                "recovery_failure"
            )

            break

        # ----------------------------------------------------
        # Validate repair response
        # ----------------------------------------------------

        if not isinstance(
            repaired_solution,
            dict,
        ):

            print(
                "Recovery returned invalid response."
            )

            logger.log_event(
                "recovery_failed",
                {
                    "attempt": attempt,
                    "reason":
                        "invalid repair response",
                },
            )

            result["failure_type"] = (
                "recovery_failure"
            )

            break

        repair_status = repaired_solution.get(
            "status"
        )

        print(
            "Recovery status:",
            repair_status,
        )

        if repair_status != "completed":

            message = repaired_solution.get(
                "message",
                "Recovery failed.",
            )

            print(
                message
            )

            logger.log_event(
                "recovery_failed",
                {
                    "attempt": attempt,
                    "reason": message,
                },
            )

            result["failure_type"] = (
                "recovery_failure"
            )

            break

        solution = repaired_solution

        logger.log_event(
            "recovery_completed",
            {
                "attempt": attempt,
                "status": repair_status,
                "files": list(
                    repaired_solution.get(
                        "files",
                        {},
                    ).keys()
                ),
            },
        )

        print(
            "Applying repaired solution..."
        )

        apply_agent_solution(
            repo_path,
            repaired_solution,
        )

        logger.log_event(
            "repaired_solution_applied",
            {
                "attempt": attempt,
                "files": list(
                    repaired_solution.get(
                        "files",
                        {},
                    ).keys()
                ),
            },
        )

    # --------------------------------------------------------
    # Final failure
    # --------------------------------------------------------

    if result is None:

        result = {
            "passed": False,
            "duration_seconds": 0,
            "stdout": "",
            "stderr": "",
            "returncode": 1,
            "tests_executed": False,
            "failure_type": "generation_error",
        }

    result["recovery_attempted"] = recovery_attempted
    result["recovery_success"] = False
    result["final_success"] = False
    result["attempts_used"] = attempts_used
    result["generation_success"] = generation_success

    logger.log_event(
        "task_completed",
        {
            "attempts_used": attempts_used,
            "passed": False,
            "max_attempts_reached": True,
        },
    )

    trajectory_path = os.path.join(
        "results",
        (
            f"trajectory_"
            f"{task_id}_"
            f"{agent}_"
            f"run_{run_number}.json"
        ),
    )

    logger.save(
        trajectory_path
    )

    return result


# ============================================================
# RUN ONE AGENT
# ============================================================

def run_agent(
    task_id,
    agent,
    run_number,
):
    """
    Run one agent on one task for one benchmark run.
    """

    print()
    print(
        "=" * 60
    )

    print(
        "Running agent:",
        agent,
    )

    print(
        "Task:",
        task_id,
    )

    print(
        "Run:",
        run_number,
    )

    print(
        "=" * 60
    )

    workspace = create_clean_workspace(
        task_id,
        agent,
        run_number,
    )

    print(
        "Workspace:",
        workspace,
    )

    task = TASKS[
        task_id
    ]

    result = evaluate_with_retries(
        task_id=task_id,
        agent=agent,
        repo_path=workspace,
        test_command=task[
            "test_command"
        ],
        run_number=run_number,
        max_attempts=MAX_ATTEMPTS,
    )

    print()
    print(
        "-" * 60
    )

    print(
        "Agent:",
        agent,
    )

    print(
        "Task:",
        task_id,
    )

    print(
        "Run:",
        run_number,
    )

    print(
        "Passed:",
        result["passed"],
    )

    print(
        "Failure Type:",
        result.get(
            "failure_type",
            "",
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
        result[
            "duration_seconds"
        ],
        "seconds",
    )

    print(
        "-" * 60
    )

    print()
    print(
        "Test Output:"
    )

    print(
        result[
            "stdout"
        ]
    )

    if result[
        "stderr"
    ]:

        print()
        print(
            "Errors:"
        )

        print(
            result[
                "stderr"
            ]
        )

    return result


# ============================================================
# PRE-CHECK ALL TASKS
# ============================================================

def validate_tasks(
    task_filter=None,
):
    """
    Validate task repositories one at a time using isolated
    workspaces.

    Only visible tests are used during pre-check.
    """

    print()
    print(
        "=" * 70
    )

    print(
        "PRE-CHECKING TASKS (ISOLATED)"
    )

    print(
        "=" * 70
    )

    if task_filter:

        if task_filter not in TASKS:

            print()
            print(
                f"ERROR: Unknown task: {task_filter}"
            )

            print()
            print(
                "Available tasks:"
            )

            for task_id in TASKS:

                print(
                    f"  {task_id}"
                )

            return False

        tasks_to_check = {
            task_filter:
                TASKS[
                    task_filter
                ]
        }

    else:

        tasks_to_check = TASKS

    all_passed = True

    for task_id, task in (
        tasks_to_check.items()
    ):

        print()
        print(
            "-" * 70
        )

        print(
            f"Checking {task_id}"
        )

        print(
            "-" * 70
        )

        source_repo = task[
            "repo_path"
        ]

        test_command = task[
            "test_command"
        ]

        if not os.path.isdir(
            source_repo
        ):

            print(
                "ERROR: Repository not found:",
                source_repo,
            )

            all_passed = False

            continue

        workspace = create_clean_workspace(
            task_id,
            "precheck",
            1,
        )

        print(
            "Repository:",
            source_repo,
        )

        print(
            "Isolated workspace:",
            workspace,
        )

        print(
            "Test command:",
            test_command,
        )

        print()
        print(
            "Running tests..."
        )

        result = run_tests(
            repo_path=workspace,
            test_command=test_command,
            task_id=task_id,
            include_hidden=False,
        )

        print()
        print(
            "Passed:",
            result[
                "passed"
            ],
        )

        print(
            "Duration:",
            result[
                "duration_seconds"
            ],
            "seconds",
        )

        print()
        print(
            "Test Output:"
        )

        print(
            result[
                "stdout"
            ]
        )

        if result[
            "stderr"
        ]:

            print()
            print(
                "Errors:"
            )

            print(
                result[
                    "stderr"
                ]
            )

        if result[
            "passed"
        ]:

            print(
                f"✅ {task_id} PRE-CHECK PASSED"
            )

        else:

            print(
                f"❌ {task_id} PRE-CHECK FAILED"
            )

            all_passed = False

        try:

            shutil.rmtree(
                workspace
            )

        except OSError as exc:

            print(
                "WARNING: Could not remove workspace:",
                exc,
            )

    print()
    print(
        "=" * 70
    )

    if all_passed:

        print(
            "✅ ALL TASK PRE-CHECKS PASSED"
        )

    else:

        print(
            "❌ ONE OR MORE TASK PRE-CHECKS FAILED"
        )

    print(
        "=" * 70
    )

    print()

    return all_passed


# ============================================================
# EVALUATE ONE TASK
# ============================================================

def evaluate_task(
    task_id,
):
    """
    Evaluate one task against all configured agents.
    """

    if task_id not in TASKS:

        raise ValueError(
            f"Unknown task: {task_id}"
        )

    print()
    print(
        "#" * 70
    )

    print(
        f"EVALUATING TASK: {task_id}"
    )

    print(
        "#" * 70
    )

    for agent in AGENTS:

        for run_number in range(
            1,
            RUNS_PER_AGENT + 1,
        ):

            run_agent(
                task_id,
                agent,
                run_number,
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="AI Agent Evaluation"
    )

    parser.add_argument(
        "--task",
        help=(
            "Run only a specific task, "
            "e.g. task_10"
        ),
    )

    parser.add_argument(
        "--skip-precheck",
        action="store_true",
        help="Skip task pre-check",
    )

    args = parser.parse_args()

    if (
        args.task
        and args.task not in TASKS
    ):

        print()
        print(
            f"ERROR: Unknown task: {args.task}"
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

    print()
    print(
        "=" * 70
    )

    print(
        "AI AGENT EVALUATION"
    )

    print(
        "=" * 70
    )

    print(
        "Tasks:",
        len(TASKS),
    )

    print(
        "Agents:",
        len(AGENTS),
    )

    print(
        "Runs per agent:",
        RUNS_PER_AGENT,
    )

    print(
        "Maximum attempts:",
        MAX_ATTEMPTS,
    )

    if args.task:

        print(
            "Selected task:",
            args.task,
        )

    else:

        print(
            "Selected task: ALL"
        )

    print(
        "=" * 70
    )

    if not args.skip_precheck:

        if not validate_tasks(
            args.task
        ):

            print()
            print(
                "Evaluation stopped."
            )

            print(
                "Fix the failing task first."
            )

            sys.exit(1)

    if args.task:

        evaluate_task(
            args.task
        )

    else:

        for task_id in TASKS:

            evaluate_task(
                task_id
            )

    print()
    print(
        "=" * 70
    )

    print(
        "ALL TASKS AND AGENTS EVALUATED"
    )

    print(
        "=" * 70
    )

    print()

    print(
        "Results saved to:"
    )

    print(
        "results/results.csv"
    )

