"""Models for CustomerPulse data validation."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationIssue:
    """Description of one data validation issue."""

    name: str
    severity: str
    description: str
    affected_rows: int