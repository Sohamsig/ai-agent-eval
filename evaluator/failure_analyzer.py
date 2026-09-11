from dataclasses import dataclass
from typing import Optional


@dataclass
class FailureAnalysis:
    task_id: str
    attempt: int
    status: str
    failure_type: str
    error: str
    likely_cause: str
    suggested_strategy: list[str]


def analyze_failure(
    task_id: str,
    attempt: int,
    error: str,
    failure_type: Optional[str] = None,
) -> FailureAnalysis:

    error_lower = error.lower()

    # Classify common failure patterns
    if "assertionerror" in error_lower:
        category = "Test Failure"
        cause = "Implementation does not satisfy the expected behavior."
        strategy = [
            "inspect the failing test",
            "inspect the relevant implementation",
            "identify the behavior mismatch",
            "make the smallest required fix",
            "rerun the failing test",
        ]

    elif "typeerror" in error_lower:
        category = "Type Error"
        cause = "The implementation uses an unexpected or invalid data type."
        strategy = [
            "inspect the failing input",
            "trace the value causing the error",
            "check type validation and conversions",
            "apply the smallest fix",
            "rerun the tests",
        ]

    elif "keyerror" in error_lower:
        category = "Missing Key"
        cause = "The implementation expects a dictionary key that is missing."
        strategy = [
            "inspect the input structure",
            "identify the missing key",
            "check validation and defaults",
            "fix the access safely",
            "rerun the tests",
        ]

    elif "indexerror" in error_lower:
        category = "Index Error"
        cause = "The implementation accesses an invalid list or sequence index."
        strategy = [
            "inspect sequence boundaries",
            "identify the invalid index",
            "handle empty or short inputs",
            "rerun the tests",
        ]

    elif "timeout" in error_lower:
        category = "Timeout"
        cause = "The operation exceeded the allowed execution time."
        strategy = [
            "inspect potentially slow operations",
            "identify unnecessary work",
            "check loops and blocking operations",
            "optimize the implementation",
            "rerun the tests",
        ]

    elif "modulenotfounderror" in error_lower:
        category = "Missing Dependency"
        cause = "A required module or package cannot be imported."
        strategy = [
            "inspect imports",
            "verify the dependency exists",
            "check the project environment",
            "fix the import or dependency",
            "rerun the tests",
        ]

    else:
        category = failure_type or "Unknown"
        cause = "The failure requires inspection of the test output and repository."
        strategy = [
            "inspect the failure output",
            "inspect the relevant repository files",
            "identify the root cause",
            "apply a targeted fix",
            "rerun the tests",
        ]

    return FailureAnalysis(
        task_id=task_id,
        attempt=attempt,
        status="FAILED",
        failure_type=category,
        error=error,
        likely_cause=cause,
        suggested_strategy=strategy,
    )


def print_analysis(analysis: FailureAnalysis):
    print()
    print("=" * 70)
    print("FAILURE ANALYSIS")
    print("=" * 70)

    print(f"Task:          {analysis.task_id}")
    print(f"Attempt:       {analysis.attempt}")
    print(f"Status:        {analysis.status}")
    print(f"Category:      {analysis.failure_type}")
    print(f"Error:         {analysis.error}")
    print(f"Likely Cause:  {analysis.likely_cause}")

    print("Suggested strategy:")

    for index, step in enumerate(analysis.suggested_strategy, start=1):
        print(f"  {index}. {step}")

    print("=" * 70)


if __name__ == "__main__":
    analysis = analyze_failure(
        task_id="task_32",
        attempt=1,
        error="AssertionError: expected timeout validation",
    )

    print_analysis(analysis)