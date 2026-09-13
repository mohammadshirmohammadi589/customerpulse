"""Duplicate validation utilities."""

import pandas as pd

from customerpulse.validation.models import ValidationIssue


def validate_duplicate_transactions(
    df: pd.DataFrame,
) -> list[ValidationIssue]:
    """Validate exact duplicate transaction records."""

    issues = []

    duplicate_rows = int(df.duplicated().sum())

    if duplicate_rows > 0:
        issues.append(
            ValidationIssue(
                name="duplicate_transaction_records",
                severity="WARNING",
                description=(
                    "Exact duplicate transaction records are present."
                ),
                affected_rows=duplicate_rows,
            )
        )

    return issues