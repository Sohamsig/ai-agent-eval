"""Versioned result-record schema helpers.

This module never rewrites raw historical data. Normalization returns a
new mapping, retains unknown fields, and represents absent values as ``None``.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any, Iterable, Mapping
from uuid import uuid4


SCHEMA_VERSION = "2"


FINAL_RESULT_FIELDS = [
    "schema_version",
    "timestamp",
    "run_id",
    "task_id",
    "agent",
    "run_number",
    "generation_success",
    "tests_executed",
    "tests_passed",
    "tests_total",
    "tests_passed_count",
    "tests_failed_count",
    "tests_skipped_count",
    "final_success",
    "failure_type",
    "error_message",
    "exit_code",
    "timed_out",
    "stdout",
    "stderr",
    "recovery_attempted",
    "recovery_success",
    "attempts_used",
    "max_attempts",
    "duration_seconds",
]


ATTEMPT_RESULT_FIELDS = [
    "schema_version",
    "timestamp",
    "run_id",
    "attempt_id",
    "task_id",
    "agent",
    "run_number",
    "attempt_number",
    "generation_success",
    "tests_executed",
    "tests_passed",
    "tests_total",
    "tests_passed_count",
    "tests_failed_count",
    "tests_skipped_count",
    "failure_type",
    "error_message",
    "exit_code",
    "timed_out",
    "stdout",
    "stderr",
    "duration_seconds",
]


_NULL_STRINGS = {"", "null", "none", "unknown", "n/a"}


_FINAL_ALIASES = {
    "run": "run_number",
    "passed": "final_success",
    "return_code": "exit_code",
    "error": "error_message",
    "attempt": "attempt_number",
}


_ATTEMPT_ALIASES = {
    "run": "run_number",
    "attempt": "attempt_number",
    "passed": "tests_passed",
    "return_code": "exit_code",
    "error": "error_message",
}


@dataclass(frozen=True)
class ValidationIssue:
    field: str
    message: str


def new_run_id() -> str:
    """Return a globally unique identifier for one logical evaluation."""
    return str(uuid4())


def new_attempt_id() -> str:
    """Return a globally unique identifier for one recorded attempt."""
    return str(uuid4())


def nullable(value: Any) -> Any:
    """Convert explicit empty/unknown scalar values to None without guessing."""
    if value is None:
        return None

    if isinstance(value, str) and value.strip().lower() in _NULL_STRINGS:
        return None

    return value


def normalize_record(
    raw: Mapping[str, Any],
    *,
    record_type: str,
) -> dict[str, Any]:
    """Return a non-mutating canonical record while retaining unknown fields.

    Legacy aliases are used only when the canonical field is absent or null.
    Missing data remains ``None``; it is never converted to ``False`` or zero.
    """
    if record_type not in {"final", "attempt"}:
        raise ValueError("record_type must be 'final' or 'attempt'")

    fields = (
        FINAL_RESULT_FIELDS
        if record_type == "final"
        else ATTEMPT_RESULT_FIELDS
    )

    aliases = (
        _FINAL_ALIASES
        if record_type == "final"
        else _ATTEMPT_ALIASES
    )

    normalized = {
        key: nullable(value)
        for key, value in raw.items()
    }

    for legacy_name, canonical_name in aliases.items():
        if (
            normalized.get(canonical_name) is None
            and legacy_name in normalized
        ):
            normalized[canonical_name] = normalized[legacy_name]

    for field in fields:
        normalized.setdefault(field, None)

    if normalized["schema_version"] is None:
        normalized["schema_version"] = (
            SCHEMA_VERSION
            if normalized.get("run_id")
            else None
        )

    return normalized


def normalize_final_record(
    raw: Mapping[str, Any],
) -> dict[str, Any]:
    return normalize_record(raw, record_type="final")


def normalize_attempt_record(
    raw: Mapping[str, Any],
) -> dict[str, Any]:
    return normalize_record(raw, record_type="attempt")


def validate_final_record(
    record: Mapping[str, Any],
) -> list[ValidationIssue]:
    normalized = normalize_final_record(record)

    required = (
        "schema_version",
        "timestamp",
        "run_id",
        "task_id",
        "agent",
        "run_number",
    )

    issues = _validate_required(normalized, required)

    issues.extend(
        _validate_integer(
            normalized.get("run_number"),
            "run_number",
            minimum=1,
        )
    )

    issues.extend(
        _validate_integer(
            normalized.get("attempts_used"),
            "attempts_used",
            minimum=0,
            allow_none=True,
        )
    )

    issues.extend(
        _validate_number(
            normalized,
            "duration_seconds",
            allow_none=True,
        )
    )

    return issues


def validate_attempt_record(
    record: Mapping[str, Any],
) -> list[ValidationIssue]:
    normalized = normalize_attempt_record(record)

    required = (
        "schema_version",
        "timestamp",
        "run_id",
        "attempt_id",
        "task_id",
        "agent",
        "run_number",
        "attempt_number",
    )

    issues = _validate_required(normalized, required)

    issues.extend(
        _validate_integer(
            normalized.get("run_number"),
            "run_number",
            minimum=1,
        )
    )

    issues.extend(
        _validate_integer(
            normalized.get("attempt_number"),
            "attempt_number",
            minimum=1,
        )
    )

    issues.extend(
        _validate_number(
            normalized,
            "duration_seconds",
            allow_none=True,
        )
    )

    return issues


def _validate_required(
    record: Mapping[str, Any],
    fields: Iterable[str],
) -> list[ValidationIssue]:
    return [
        ValidationIssue(
            field=field,
            message="required value is missing",
        )
        for field in fields
        if record.get(field) is None
    ]


def _validate_integer(
    value: Any,
    field: str,
    minimum: int | None = None,
    maximum: int | None = None,
    allow_none: bool = False,
) -> list[ValidationIssue]:
    """Validate that a value is a strict integer."""

    issues: list[ValidationIssue] = []

    if value is None and allow_none:
        return issues

    if isinstance(value, bool) or not isinstance(value, int):
        issues.append(
            ValidationIssue(
                field=field,
                message="must be an integer",
            )
        )
        return issues

    if minimum is not None and value < minimum:
        issues.append(
            ValidationIssue(
                field=field,
                message=f"must be >= {minimum}",
            )
        )

    if maximum is not None and value > maximum:
        issues.append(
            ValidationIssue(
                field=field,
                message=f"must be <= {maximum}",
            )
        )

    return issues


def _validate_number(
    record: Mapping[str, Any],
    field: str,
    *,
    allow_none: bool,
) -> list[ValidationIssue]:
    value = record.get(field)

    if value is None and allow_none:
        return []

    if isinstance(value, bool):
        return [
            ValidationIssue(
                field=field,
                message="must be numeric",
            )
        ]

    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return [
            ValidationIssue(
                field=field,
                message="must be numeric",
            )
        ]

    if not isfinite(numeric_value):
        return [
            ValidationIssue(
                field=field,
                message="must be finite",
            )
        ]

    return []


def duplicate_keys(
    records: Iterable[Mapping[str, Any]],
    *,
    record_type: str,
) -> dict[
    tuple[Any, ...],
    list[dict[str, Any]],
]:
    """Return duplicate groups without removing, ordering, or selecting rows."""
    if record_type not in {"final", "attempt"}:
        raise ValueError("record_type must be 'final' or 'attempt'")

    normalizer = (
        normalize_final_record
        if record_type == "final"
        else normalize_attempt_record
    )

    groups: dict[
        tuple[Any, ...],
        list[dict[str, Any]],
    ] = {}

    for raw in records:
        row = normalizer(raw)
        key = _duplicate_key(row, record_type)
        groups.setdefault(key, []).append(row)

    return {
        key: rows
        for key, rows in groups.items()
        if len(rows) > 1
    }


def _duplicate_key(
    row: Mapping[str, Any],
    record_type: str,
) -> tuple[Any, ...]:
    if record_type == "final":
        if row.get("run_id"):
            return ("run_id", row["run_id"])

        return (
            row.get("task_id"),
            row.get("agent"),
            row.get("run_number"),
        )

    if row.get("attempt_id"):
        return ("attempt_id", row["attempt_id"])

    return (
        row.get("task_id"),
        row.get("agent"),
        row.get("run_number"),
        row.get("attempt_number"),
    )