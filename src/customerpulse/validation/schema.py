"""Schema validation utilities for CustomerPulse."""

import pandas as pd

from customerpulse.config.data_contract import REQUIRED_FIELDS
from customerpulse.validation.models import ValidationIssue


def validate_required_columns(
    df: pd.DataFrame,
) -> list[ValidationIssue]:
    """Validate that all required canonical columns are present."""

    issues = []

    missing_fields = [
        field for field in REQUIRED_FIELDS
        if field not in df.columns
    ]

    if missing_fields:
        issues.append(
            ValidationIssue(
                name="missing_required_columns",
                severity="ERROR",
                description=(
                    f"Missing required columns: {missing_fields}"
                ),
                affected_rows=len(df),
            )
        )

    return issues