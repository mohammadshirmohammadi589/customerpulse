"""Currency validation utilities."""

import pandas as pd

from customerpulse.validation.models import ValidationIssue


def validate_currency(
    df: pd.DataFrame,
) -> list[ValidationIssue]:
    """Validate currency availability and consistency."""

    issues = []

    if "currency" not in df.columns:
        issues.append(
            ValidationIssue(
                name="currency_not_available",
                severity="WARNING",
                description=(
                    "Currency information is not available in the source data."
                ),
                affected_rows=len(df),
            )
        )
        return issues

    unique_currencies = (
        df["currency"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )

    if len(unique_currencies) > 1:
        issues.append(
            ValidationIssue(
                name="multiple_currencies",
                severity="WARNING",
                description=(
                    "Multiple currencies are present without a conversion rule."
                ),
                affected_rows=len(df),
            )
        )

    return issues