from __future__ import annotations


def classify_failure(
    return_code: int,
    stdout: str = "",
    stderr: str = "",
    timed_out: bool = False,
) -> str:
    """
    Classify a test execution result into a useful failure category.
    """

    if timed_out:
        return "timeout"

    if return_code == 0:
        return "success"

    output = f"{stdout}\n{stderr}".lower()

    if "syntaxerror" in output:
        return "syntax_error"

    if "modulenotfounderror" in output:
        return "module_not_found"

    if "importerror" in output:
        return "import_error"

    if "assertionerror" in output:
        return "assertion_error"

    if "typeerror" in output:
        return "type_error"

    if "nameerror" in output:
        return "name_error"

    if "attributeerror" in output:
        return "attribute_error"

    if "filenotfounderror" in output:
        return "file_not_found"

    if "collected 0 items" in output:
        return "no_tests_collected"

    if "failed" in output or "error" in output:
        return "test_failure"

    return "unknown_failure"