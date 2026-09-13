"""Canonical schema validation for standardized transactions."""

import pandas as pd

from customerpulse.config.data_contract import REQUIRED_FIELDS
from customerpulse.validation.models import ValidationIssue


def validate_standardized_schema(
    df: pd.DataFrame,
) -> list[ValidationIssue]:
    """Validate the schema of standardized transaction-level data."""

    issues = []

    missing_fields = [
        field for field in REQUIRED_FIELDS
        if field not in df.columns
    ]

    if missing_fields:
        issues.append(
            ValidationIssue(
                name="missing_canonical_fields",
                severity="ERROR",
                description=(
                    f"Standardized data is missing required fields: "
                    f"{missing_fields}"
                ),
                affected_rows=len(df),
            )
        )

    return issues