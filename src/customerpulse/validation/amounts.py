"""Amount validation utilities."""

import pandas as pd

from customerpulse.validation.models import ValidationIssue


def validate_amounts(
    df: pd.DataFrame,
) -> list[ValidationIssue]:
    """Validate transaction amounts."""

    issues = []

    missing_amounts = int(df["amount"].isna().sum())

    if missing_amounts > 0:
        issues.append(
            ValidationIssue(
                name="missing_amount",
                severity="ERROR",
                description="Transaction amount contains missing values.",
                affected_rows=missing_amounts,
            )
        )

    non_positive_amounts = int((df["amount"] <= 0).sum())

    if non_positive_amounts > 0:
        issues.append(
            ValidationIssue(
                name="non_positive_amount",
                severity="WARNING",
                description="Transaction amount is zero or negative.",
                affected_rows=non_positive_amounts,
            )
        )

    return issues