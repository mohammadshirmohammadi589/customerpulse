"""Validation gate utilities."""

from customerpulse.validation.models import ValidationIssue


def has_blocking_errors(
    issues: list[ValidationIssue],
) -> bool:
    """Return True when at least one ERROR exists."""

    return any(issue.severity == "ERROR" for issue in issues)