import os


def solve(task, repo_path=None):
    """
    Agent 03:
    Local deterministic agent used for testing the evaluator
    without consuming OpenAI API credits.
    """

    if task == "task_32":
        solution = {
            "helpers.py": """def parse_config(config):
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

    if not isinstance(timeout, int) or isinstance(timeout, bool):
        return None

    if timeout < 0:
        return None

    return {
        "host": host,
        "port": port,
        "timeout": timeout,
    }


def get_timeout(config):
    return config["timeout"]
""",

            "actual_task_file.py": """from helpers import parse_config, get_timeout


def create_client(config):
    parsed = parse_config(config)

    if parsed is None:
        return None

    timeout = get_timeout(parsed)

    if timeout is None:
        return None

    return {
        "host": parsed["host"],
        "port": parsed["port"],
        "timeout": timeout,
    }
""",
        }

        return {
            "agent": "agent_03",
            "status": "completed",
            "message": "Local deterministic solution generated.",
            "files": solution,
        }

    return {
        "agent": "agent_03",
        "status": "failed",
        "message": f"Unsupported task: {task}",
        "files": {},
    }


if __name__ == "__main__":
    result = solve("task_32")

    print("Agent:", result["agent"])
    print("Status:", result["status"])
    print("Message:", result["message"])
    print("Files:", list(result["files"].keys()))