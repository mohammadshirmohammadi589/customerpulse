"""Validation runner for CustomerPulse."""

import pandas as pd
from customerpulse.validation.currency import validate_currency
from customerpulse.validation.duplicates import validate_duplicate_transactions
from customerpulse.validation.amounts import validate_amounts
from customerpulse.validation.dates import validate_transaction_dates
from customerpulse.validation.ids import validate_identifiers
from customerpulse.validation.models import ValidationIssue
from customerpulse.validation.nulls import validate_missing_values
from customerpulse.validation.schema import validate_required_columns


def validate_data(df: pd.DataFrame) -> list[ValidationIssue]:
    """Run all available validation checks."""

    issues: list[ValidationIssue] = []

    issues.extend(validate_required_columns(df))

    if not all(
        field in df.columns
        for field in ("customer_id", "transaction_id")
    ):
        return issues

    issues.extend(validate_missing_values(df))

    if "transaction_date" in df.columns:
        issues.extend(validate_transaction_dates(df))

    if "amount" in df.columns:
        issues.extend(validate_amounts(df))

    issues.extend(validate_identifiers(df))
    issues.extend(validate_duplicate_transactions(df))
    issues.extend(validate_currency(df))
    return issues