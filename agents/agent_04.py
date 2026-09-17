import os


def solve(task, repo_path=None):
    """
    Agent 04 intentionally generates a broken solution
    so the evaluator can test recovery behavior.
    """

    if task != "task_32":
        return {
            "agent": "agent_04",
            "status": "failed",
            "message": f"Unsupported task: {task}",
            "files": {},
        }

    return {
        "agent": "agent_04",
        "status": "completed",
        "message": "Intentionally broken solution generated.",
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
    # Intentionally broken:
    # bool and string values are accepted incorrectly.
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
            "test_task_32.py": """from actual_task_file import create_client


def test_negative_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": -5,
    }) is None


def test_string_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": "10",
    }) is None


def test_boolean_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": True,
    }) is None


def test_none_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": None,
    }) is None


def test_zero_timeout_is_valid():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": 0,
    }) == {
        "host": "localhost",
        "port": 8080,
        "timeout": 0,
    }


def test_missing_timeout_uses_default():
    assert create_client({
        "host": "localhost",
        "port": 8080,
    }) == {
        "host": "localhost",
        "port": 8080,
        "timeout": 30,
    }
""",
        },
    }


def repair(task_id, workspace, context=None):
    """
    Repair the intentionally broken timeout validation.
    """

    if task_id != "task_32":
        return {
            "agent": "agent_04",
            "status": "failed",
            "message": f"Unsupported repair task: {task_id}",
            "files": {},
        }

    return {
        "agent": "agent_04",
        "status": "completed",
        "message": "Repaired timeout validation.",
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
    timeout = config.get("timeout", 30)

    if isinstance(timeout, bool) or not isinstance(timeout, int):
        return None

    if timeout < 0:
        return None

    return timeout
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
            "test_task_32.py": """from actual_task_file import create_client


def test_negative_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": -5,
    }) is None


def test_string_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": "10",
    }) is None


def test_boolean_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": True,
    }) is None


def test_none_timeout_rejected():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": None,
    }) is None


def test_zero_timeout_is_valid():
    assert create_client({
        "host": "localhost",
        "port": 8080,
        "timeout": 0,
    }) == {
        "host": "localhost",
        "port": 8080,
        "timeout": 0,
    }


def test_missing_timeout_uses_default():
    assert create_client({
        "host": "localhost",
        "port": 8080,
    }) == {
        "host": "localhost",
        "port": 8080,
        "timeout": 30,
    }
""",
        },
    }


if __name__ == "__main__":
    result = solve("task_32")

    print("Agent:", result["agent"])
    print("Status:", result["status"])
    print("Message:", result["message"])
    print("Files:", list(result["files"].keys()))