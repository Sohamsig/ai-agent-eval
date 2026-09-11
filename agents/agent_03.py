import os
from pathlib import Path

from openai import OpenAI


MAX_AGENT_ITERATIONS = 5
TOOLS_DESCRIPTION = """
You are an autonomous software engineering agent.

You have four tools:

1. list_files(repo_path)
   - Lists files in the repository.

2. read_file(repo_path, relative_path)
   - Reads a source, test, or configuration file.
   - Only files inside the repository may be accessed.

3. write_file(repo_path, relative_path, content)
   - Creates or replaces a file inside the repository.
   - Never write outside the repository.

4. run_tests(repo_path)
   - Runs the repository test suite.
   - Use this after making changes to verify the implementation.

Workflow:
1. Understand the task.
2. Inspect relevant files.
3. Identify the root cause.
4. Make the smallest correct change.
5. Run tests.
6. If tests fail, inspect the failure and fix the implementation.
7. Repeat until the task is solved or the iteration limit is reached.
"""

MODEL = os.getenv("LLM_MODEL", "gpt-5.6")


def safe_path(repo_path, relative_path):
    """Return an absolute path only if it stays inside repo_path."""
    repo = Path(repo_path).resolve()
    target = (repo / relative_path).resolve()

    if os.path.commonpath([str(repo), str(target)]) != str(repo):
        raise ValueError(f"Path escapes repository: {relative_path}")

    return target


def list_files(repo_path):
    """List repository files available to the agent."""
    repo = Path(repo_path).resolve()
    files = []

    for path in repo.rglob("*"):
        if not path.is_file():
            continue

        if "__pycache__" in path.parts:
            continue

        if ".git" in path.parts:
            continue

        files.append(str(path.relative_to(repo)).replace("\\", "/"))

    return sorted(files)


def read_file(repo_path, relative_path, max_bytes=20000):
    """Safely read a text file inside the repository."""
    path = safe_path(repo_path, relative_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {relative_path}")

    if path.stat().st_size > max_bytes:
        raise ValueError(
            f"File too large to read: {relative_path}"
        )

    return path.read_text(encoding="utf-8")

import subprocess
import sys


def run_tests(repo_path):
    """Run the repository test suite and return the result."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=str(repo_path),
        capture_output=True,
        text=True,
        timeout=120,
    )

    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "passed": result.returncode == 0,
    }

def write_file(repo_path, relative_path, content):
    """Safely write a text file inside the repository."""
    path = safe_path(repo_path, relative_path)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    return str(path.relative_to(Path(repo_path).resolve())).replace("\\", "/")

def mock_llm_decision(iteration, test_result):
    """Temporary local decision function used without API credits."""
    if test_result["passed"]:
        return {
            "action": "finish",
            "reason": "All tests pass.",
        }

    if iteration == 0:
        return {
            "action": "inspect",
            "file": "actual_task_file.py",
            "reason": "Inspect the implementation.",
        }

    if iteration == 1:
        return {
            "action": "inspect",
            "file": "helpers.py",
            "reason": "Inspect helper logic.",
        }

    return {
        "action": "finish",
        "reason": "Mock iteration limit reached.",
    }

def load_prompt(task_id, repo_path):
    """Load the task prompt from the task repository."""
    candidates = [
        Path(repo_path) / "prompt.txt",
        Path(repo_path) / "prompt.md",
    ]

    for path in candidates:
        if path.is_file():
            return path.read_text(encoding="utf-8")

    raise FileNotFoundError(
        f"No prompt.txt or prompt.md found in {repo_path}"
    )


def run_agent_loop(task_id, repo_path):
    """Run the local SWE-agent loop using the mock decision function."""
    history = []

    for iteration in range(MAX_AGENT_ITERATIONS):
        test_result = run_tests(repo_path)

        history.append({
            "iteration": iteration,
            "test_result": test_result,
        })

        decision = mock_llm_decision(iteration, test_result)

        history[-1]["decision"] = decision

        if decision["action"] == "finish":
            return {
                "status": "finished",
                "iterations": iteration + 1,
                "history": history,
            }

        if decision["action"] == "inspect":
            file_name = decision.get("file")

            try:
                content = read_file(repo_path, file_name)
                history[-1]["inspection"] = {
                    "file": file_name,
                    "content": content,
                }
            except Exception as exc:
                history[-1]["inspection_error"] = str(exc)

    return {
        "status": "iteration_limit",
        "iterations": MAX_AGENT_ITERATIONS,
        "history": history,
    }

def solve(task_id, repo_path=None):
    """
    LLM-based SWE agent.
    """
    if repo_path is None:
        repo_path = os.path.join("tasks", task_id)

    try:
        prompt = load_prompt(task_id, repo_path)
        files = list_files(repo_path)
    except Exception as exc:
        return {
            "agent": "agent_03",
            "status": "failed",
            "message": str(exc),
            "files": {},
        }

    if not os.getenv("OPENAI_API_KEY"):
        return {
            "agent": "agent_03",
            "status": "failed",
            "message": "OPENAI_API_KEY is not set.",
            "files": {},
        }

    try:
        client = OpenAI()

        response = client.responses.create(
            model=MODEL,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert software engineer. "
                        "Analyze the repository task carefully and "
                        "produce a correct implementation."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        prompt
                        + "\n\nRepository files:\n"
                        + "\n".join(files)
                    ),
                },
            ],
        )

        output = response.output_text

        return {
            "agent": "agent_03",
            "status": "completed",
            "message": "LLM response generated successfully.",
            "files": {},
            "llm_output": output,
        }

    except Exception as exc:
        return {
            "agent": "agent_03",
            "status": "failed",
            "message": f"LLM request failed: {exc}",
            "files": {},
        }


if __name__ == "__main__":
    result = solve("task_32")
    print("Agent:", result["agent"])
    print("Status:", result["status"])
    print("Message:", result["message"])







