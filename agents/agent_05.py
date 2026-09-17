def solve(task, repo_path=None):
    if task != "task_32":
        return {
            "agent": "agent_05",
            "status": "failed",
            "message": f"Unsupported task: {task}",
            "files": {},
        }

    return {
        "agent": "agent_05",
        "status": "completed",
        "message": "Generated intentionally broken solution.",
        "files": {
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

    return {
        "host": host,
        "port": port,
        "timeout": config.get("timeout", 30),
    }


def get_timeout(config):
    return config.get("timeout", 30)
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
        },
    }


def repair(task_id, workspace, context=None):
    raise RuntimeError(
        "Agent 05 repair failed intentionally."
    )


if __name__ == "__main__":
    result = solve("task_32")
    print("Agent:", result["agent"])
    print("Status:", result["status"])
    print("Message:", result["message"])
    print("Files:", list(result["files"].keys()))