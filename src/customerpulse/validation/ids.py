"""Identifier validation utilities."""

import pandas as pd

from customerpulse.validation.models import ValidationIssue


def validate_identifiers(
    df: pd.DataFrame,
) -> list[ValidationIssue]:
    """Validate customer and transaction identifiers."""

    issues = []

    for field in ("customer_id", "transaction_id"):
        if field not in df.columns:
            continue

        invalid_ids = int(
            (
                df[field].notna()
                & (df[field].astype(str).str.strip() == "")
            ).sum()
        )

        if invalid_ids > 0:
            issues.append(
                ValidationIssue(
                    name=f"invalid_{field}",
                    severity="ERROR",
                    description=(
                        f"Identifier '{field}' contains unusable values."
                    ),
                    affected_rows=invalid_ids,
                )
            )

    return issues