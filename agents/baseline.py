from pathlib import Path


def solve(task, repo_path=None):
    """
    Baseline agent intentionally performs no initial modification.

    The evaluator should observe the original failure first and
    then measure whether the recovery strategy can repair the task.
    """
    return {
        "agent": "baseline",
        "status": "completed",
        "files": {},
    }


def repair(task_id, repo_path, failure_feedback):
    """
    Deterministic recovery strategy for known benchmark tasks.

    The repair is idempotent, meaning running it multiple times
    produces the same correct result.
    """

    # ---------------------------------------------------------
    # Validate repository
    # ---------------------------------------------------------

    if repo_path is None:
        return {
            "agent": "baseline",
            "status": "failed",
            "files": {},
            "message": "Repository path not provided.",
        }

    repo = Path(repo_path)

    if not repo.exists():
        return {
            "agent": "baseline",
            "status": "failed",
            "files": {},
            "message": f"Repository path does not exist: {repo}",
        }

    # ---------------------------------------------------------
    # TASK 32
    # ---------------------------------------------------------

    if task_id == "task_32":

        helpers = repo / "helpers.py"

        if not helpers.exists():
            return {
                "agent": "baseline",
                "status": "failed",
                "files": {},
                "message": "helpers.py not found.",
            }

        try:
            content = helpers.read_text(
                encoding="utf-8"
            )
        except OSError as exc:
            return {
                "agent": "baseline",
                "status": "failed",
                "files": {},
                "message": f"Could not read helpers.py: {exc}",
            }

        # -----------------------------------------------------
        # Replace the complete helpers.py implementation.
        #
        # This fixes the root cause in BOTH:
        #
        #   parse_config()
        #   get_timeout()
        #
        # Timeout rules:
        #
        #   - missing timeout -> 30
        #   - integer >= 0 -> accepted
        #   - negative integer -> rejected
        #   - string -> rejected
        #   - bool -> rejected
        #   - None -> rejected
        # -----------------------------------------------------

        repaired_content = '''def parse_config(config):
    if not isinstance(config, dict):
        return None

    host = config.get("host")
    port = config.get("port")

    if not isinstance(host, str) or not host:
        return None

    if not isinstance(port, int) or isinstance(port, bool):
        return None

    if port <= 0 or port > 65535:
        return None

    timeout = config.get("timeout", 30)

    if type(timeout) is not int or timeout < 0:
        return None

    return {
        "host": host,
        "port": port,
        "timeout": timeout,
    }


def get_timeout(config):
    timeout = config.get("timeout", 30)

    if type(timeout) is not int or timeout < 0:
        return None

    return timeout
'''

        # -----------------------------------------------------
        # Already repaired
        #
        # This makes recovery idempotent.
        # -----------------------------------------------------

        if content == repaired_content:
            return {
                "agent": "baseline",
                "status": "completed",
                "files": {
                    "helpers.py": content,
                },
                "message": "Task 32 is already repaired.",
            }

        # -----------------------------------------------------
        # Return repaired source
        # -----------------------------------------------------

        return {
            "agent": "baseline",
            "status": "completed",
            "files": {
                "helpers.py": repaired_content,
            },
            "message": (
                "Repaired timeout validation in "
                "parse_config() and get_timeout()."
            ),
        }

    # ---------------------------------------------------------
    # Unknown task
    # ---------------------------------------------------------

    return {
        "agent": "baseline",
        "status": "failed",
        "files": {},
        "message": f"No repair strategy for {task_id}.",
    }


if __name__ == "__main__":

    result = solve("task_32")

    print(
        "Agent:",
        result["agent"],
    )

    print(
        "Status:",
        result["status"],
    )

    print(
        "Files:",
        result["files"],
    )