"""Missing-value validation utilities."""

import pandas as pd

from customerpulse.config.data_contract import REQUIRED_FIELDS, OPTIONAL_FIELDS
from customerpulse.validation.models import ValidationIssue


def validate_missing_values(
    df: pd.DataFrame,
) -> list[ValidationIssue]:
    """Validate missing values in required and optional fields."""

    issues = []

    for field in REQUIRED_FIELDS:
        if field in df.columns:
            affected_rows = int(df[field].isna().sum())

            if affected_rows > 0:
                issues.append(
                    ValidationIssue(
                        name=f"missing_{field}",
                        severity="ERROR",
                        description=f"Required field '{field}' contains missing values.",
                        affected_rows=affected_rows,
                    )
                )

    for field in OPTIONAL_FIELDS:
        if field in df.columns:
            affected_rows = int(df[field].isna().sum())

            if affected_rows > 0:
                issues.append(
                    ValidationIssue(
                        name=f"missing_{field}",
                        severity="WARNING",
                        description=f"Optional field '{field}' contains missing values.",
                        affected_rows=affected_rows,
                    )
                )

    return issues