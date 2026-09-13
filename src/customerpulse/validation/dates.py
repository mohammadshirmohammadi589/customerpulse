"""Date validation utilities."""

import pandas as pd

from customerpulse.validation.models import ValidationIssue


def validate_transaction_dates(
    df: pd.DataFrame,
) -> list[ValidationIssue]:
    """Validate transaction dates."""

    issues = []

    dates = pd.to_datetime(
        df["transaction_date"],
        format="%m/%d/%y %H:%M",
        errors="coerce",
    )

    invalid_dates = int(dates.isna().sum())

    if invalid_dates > 0:
        issues.append(
            ValidationIssue(
                name="invalid_transaction_date",
                severity="ERROR",
                description=(
                    "Transaction date contains invalid or unusable values."
                ),
                affected_rows=invalid_dates,
            )
        )

    return issues