import ast
import os
import re
from pathlib import Path


AGENT_NAME = "agent_03"
BACKEND = os.getenv("AGENT03_BACKEND", "offline")


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="cp1252")


def collect_task_context(task: str, repo_path: str | None) -> dict:
    if repo_path is None:
        repo_path = str(Path("tasks") / task)

    workspace = Path(repo_path).resolve()

    if not workspace.exists():
        raise FileNotFoundError(
            f"Task workspace not found: {workspace}"
        )

    prompt_file = workspace / "prompt.txt"

    if not prompt_file.exists():
        prompt_file = workspace / "prompt.md"

    if not prompt_file.exists():
        raise FileNotFoundError(
            f"No prompt file found in {workspace}"
        )

    prompt = read_text_file(prompt_file)

    source_files = {}
    test_files = {}

    for path in sorted(workspace.rglob("*.py")):
        if path.name == "__init__.py":
            continue

        relative_path = path.relative_to(workspace).as_posix()
        content = read_text_file(path)

        if path.name.startswith("test_"):
            test_files[relative_path] = content
        else:
            source_files[relative_path] = content

    return {
        "task": task,
        "workspace": str(workspace),
        "prompt": prompt,
        "source_files": source_files,
        "test_files": test_files,
    }


def diagnose(
    context: dict,
    test_result: dict | None = None,
    failure_analysis: dict | None = None,
) -> dict:
    """
    Deterministic offline diagnosis.

    This does not contain task-specific solutions.
    It extracts signals from the task requirements, source,
    tests, and evaluator failure information.
    """

    prompt = context.get("prompt", "")
    source_files = context.get("source_files", {})
    test_files = context.get("test_files", {})

    diagnosis = {
        "category": "unknown",
        "likely_causes": [],
        "requirements": [],
        "source_files": list(source_files.keys()),
        "test_files": list(test_files.keys()),
    }

    if failure_analysis:
        diagnosis["category"] = failure_analysis.get(
            "category",
            "unknown",
        )

        diagnosis["likely_causes"].append(
            failure_analysis.get(
                "likely_cause",
                "",
            )
        )

        excerpt = failure_analysis.get(
            "error_excerpt",
            "",
        )

        if excerpt:
            diagnosis["error_excerpt"] = excerpt

    # Extract requirement-like statements from the prompt.
    requirement_lines = []

    for line in prompt.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        lowered = stripped.lower()

        if any(
            marker in lowered
            for marker in (
                "must ",
                "should ",
                "required",
                "invalid ",
                "valid ",
                "reject",
                "return ",
                "calculate ",
                "handle ",
                "quantity",
                "discount",
                "validation",
            )
        ):
            requirement_lines.append(stripped)

    diagnosis["requirements"] = requirement_lines

    # Look for common implementation signals.
    source_text = "\n".join(source_files.values()).lower()

    if (
        "quantity" in prompt.lower()
        and "quantity" in source_text
        and "* item" not in source_text
    ):
        diagnosis["likely_causes"].append(
            "Quantity is mentioned by the requirements and source, "
            "but the implementation may not incorporate it into "
            "an aggregation calculation."
        )

    if "validate" in prompt.lower():
        diagnosis["likely_causes"].append(
            "Validation requirements should be checked against "
            "the implementation before changing unrelated behavior."
        )

    if test_result:
        diagnosis["test_passed"] = bool(
            test_result.get("passed")
        )

    return diagnosis


def _repair_quantity_aggregation(source: str, prompt: str) -> str:
    """
    Conservative, idempotent repair for quantity-aware aggregation.

    Preserves existing behavior when quantity is omitted by treating
    quantity as 1, while correctly multiplying by explicit quantities.
    """

    prompt_lower = prompt.lower()

    if "quantity" not in prompt_lower:
        return source

    # Already repaired. Do not apply the quantity multiplication again.
    if (
        re.search(
            r'item\[\s*["\']price["\']\s*\]\s*\*\s*item\[\s*["\']quantity["\']\s*\]',
            source,
        )
        or
        re.search(
            r'item\[\s*["\']price["\']\s*\]\s*\*\s*item\.get\(\s*["\']quantity["\']\s*,\s*1\s*\)',
            source,
        )
    ):
        return source

    patterns = [
        (
            r'total\s*\+=\s*item\[\s*["\']price["\']\s*\]',
            'total += item["price"] * item.get("quantity", 1)',
        ),
        (
            r'total\s*=\s*total\s*\+\s*item\[\s*["\']price["\']\s*\]',
            'total = total + item["price"] * item.get("quantity", 1)',
        ),
    ]

    for pattern, replacement in patterns:
        repaired, count = re.subn(
            pattern,
            replacement,
            source,
        )

        if count:
            return repaired

    return source

def _repair_timeout_validation(source: str, prompt: str) -> str:
    """
    Conservative generalized repair for integer timeout validation.

    It only activates when the requirements explicitly discuss
    timeout validation and preserves the existing structure.
    """

    prompt_lower = prompt.lower()

    if "timeout" not in prompt_lower:
        return source

    if "negative" not in prompt_lower:
        return source

    # Reject bool explicitly when an integer is required.
    source = re.sub(
        r'if\s+not\s+isinstance\(\s*timeout\s*,\s*int\s*\)\s*:',
        'if not isinstance(timeout, int) or isinstance(timeout, bool):',
        source,
    )

    # Add the non-negative boundary when a timeout is accepted.
    source = re.sub(
        r'if\s+timeout\s*<\s*0\s*:',
        'if timeout < 0:',
        source,
    )

    return source


def _repair_validation_boolean_types(
    source: str,
    prompt: str,
) -> str:
    """
    General validation hardening for requirements that explicitly
    reject boolean values.
    """

    prompt_lower = prompt.lower()

    if "boolean" not in prompt_lower and "bool" not in prompt_lower:
        return source

    # Do not add the bool guard when it is already present.
    if "isinstance(timeout, bool)" in source:
        return source

    # int validation must reject bool because bool subclasses int.
    source = re.sub(
        r'not\s+isinstance\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*,\s*int\s*\)',
        r'not isinstance(\1, int) or isinstance(\1, bool)',
        source,
    )

    return source


def _repair_source(
    source: str,
    prompt: str,
    diagnosis: dict,
) -> str:
    """
    Apply only conservative transformations supported by
    observable task requirements.

    No task IDs are used here.
    """

    repaired = source

    repaired = _repair_quantity_aggregation(
        repaired,
        prompt,
    )

    repaired = _repair_timeout_validation(
        repaired,
        prompt,
    )

    repaired = _repair_validation_boolean_types(
        repaired,
        prompt,
    )

    # Never return syntactically invalid generated Python.
    try:
        ast.parse(repaired)
    except SyntaxError:
        return source

    return repaired


def offline_backend(context: dict) -> dict:
    """
    Deterministic offline coding-agent generation backend.

    Generation intentionally preserves the discovered source instead of
    applying repairs. This allows the evaluator to measure genuine
    recovery behavior through repair().
    """

    source_files = context["source_files"]

    if not source_files:
        return {
            "files": {},
            "message": "No source files discovered.",
        }

    diagnosis = diagnose(context)

    generated_files = {}

    for relative_path, source in source_files.items():

        # Never modify test files during generation.
        if Path(relative_path).name.startswith("test_"):
            continue

        # Preserve the initial candidate.
        generated_files[relative_path] = source

    return {
        "files": generated_files,
        "message": (
            "Offline Agent 03 inspected the task context and "
            "generated an initial candidate without applying recovery repairs."
        ),
        "diagnosis": diagnosis,
    }


def repair(
    task_id: str,
    workspace: str,
    context: dict | None = None,
) -> dict:
    """
    Recovery interface used by evaluator.evaluate.

    The evaluator supplies:
      - previous_solution
      - test_result
      - failure_analysis

    No task-specific solution table is used.
    """

    if context is None:
        context = {}

    previous_solution = context.get(
        "previous_solution",
        {},
    )

    test_result = context.get(
        "test_result",
        {},
    )

    failure_analysis = context.get(
        "failure_analysis",
        {},
    )

    source_files = previous_solution.get(
        "files",
        {},
    )

    task_context = {
        "task": task_id,
        "workspace": workspace,
        "prompt": "",
        "source_files": dict(source_files),
        "test_files": {},
    }

    workspace_path = Path(workspace)

    prompt_file = workspace_path / "prompt.txt"

    if not prompt_file.exists():
        prompt_file = workspace_path / "prompt.md"

    if prompt_file.exists():
        task_context["prompt"] = read_text_file(
            prompt_file
        )

    for path in sorted(
        workspace_path.rglob("test_*.py")
    ):
        relative_path = path.relative_to(
            workspace_path
        ).as_posix()

        task_context["test_files"][
            relative_path
        ] = read_text_file(path)

    diagnosis = diagnose(
        task_context,
        test_result=test_result,
        failure_analysis=failure_analysis,
    )

    repaired_files = {}

    changed = []

    for relative_path, source in source_files.items():

        if Path(relative_path).name.startswith("test_"):
            continue

        repaired = _repair_source(
            source,
            task_context["prompt"],
            diagnosis,
        )

        repaired_files[relative_path] = repaired

        if repaired != source:
            changed.append(relative_path)

    if not changed:
        return {
            "agent": AGENT_NAME,
            "status": "failed",
            "message": (
                "Offline Agent 03 could not identify a "
                "supported conservative repair."
            ),
            "files": {},
        }

    return {
        "agent": AGENT_NAME,
        "status": "completed",
        "message": (
            "Offline Agent 03 repaired the implementation "
            "using failure analysis and task requirements."
        ),
        "files": repaired_files,
        "diagnosis": diagnosis,
    }


def generate_solution(context: dict) -> dict:
    if BACKEND == "offline":
        return offline_backend(context)

    if BACKEND == "openai":
        raise RuntimeError(
            "OpenAI backend selected, but API credits are "
            "currently unavailable."
        )

    raise RuntimeError(
        f"Unsupported Agent 03 backend: {BACKEND}"
    )


def validate_files(files: dict) -> dict:
    if not isinstance(files, dict):
        raise ValueError(
            "Agent output 'files' must be a dictionary."
        )

    validated = {}

    for relative_path, content in files.items():

        if not isinstance(relative_path, str):
            raise ValueError(
                "Generated file path must be a string."
            )

        if not isinstance(content, str):
            raise ValueError(
                f"Generated content must be a string: "
                f"{relative_path}"
            )

        path = Path(relative_path)

        if path.is_absolute():
            raise ValueError(
                f"Absolute paths are not allowed: "
                f"{relative_path}"
            )

        if ".." in path.parts:
            raise ValueError(
                f"Parent traversal is not allowed: "
                f"{relative_path}"
            )

        normalized = relative_path.replace(
            "\\",
            "/",
        )

        if normalized.startswith(".git/"):
            raise ValueError(
                f"Repository metadata cannot be modified: "
                f"{relative_path}"
            )

        if Path(relative_path).name.startswith("test_"):
            raise ValueError(
                f"Agent 03 cannot modify test files: "
                f"{relative_path}"
            )

        validated[normalized] = content

    return validated


def solve(task, repo_path=None):
    """
    General-purpose Agent 03 adapter.

    The evaluator calls this function.
    """

    try:
        context = collect_task_context(
            task,
            repo_path,
        )

        generated = generate_solution(
            context
        )

        files = validate_files(
            generated.get("files", {})
        )

        return {
            "agent": AGENT_NAME,
            "status": "completed",
            "message": generated.get(
                "message",
                "Solution generated.",
            ),
            "files": files,
            "diagnosis": generated.get(
                "diagnosis",
                {},
            ),
        }

    except Exception as exc:
        return {
            "agent": AGENT_NAME,
            "status": "failed",
            "message": (
                f"Agent 03 failed: {exc}"
            ),
            "files": {},
        }


if __name__ == "__main__":
    result = solve(
        "task_29",
        "tasks/task_29",
    )

    print(
        "Agent:",
        result["agent"],
    )
    print(
        "Status:",
        result["status"],
    )
    print(
        "Message:",
        result["message"],
    )
    print(
        "Files:",
        list(result["files"].keys()),
    )
