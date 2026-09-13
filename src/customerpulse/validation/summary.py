"""Validation summary utilities."""

from customerpulse.validation.models import ValidationIssue


def summarize_issues(
    issues: list[ValidationIssue],
) -> dict[str, int]:
    """Summarize validation issues by severity."""

    summary = {
        "ERROR": 0,
        "WARNING": 0,
        "INFORMATION": 0,
    }

    for issue in issues:
        if issue.severity in summary:
            summary[issue.severity] += 1

    return summary