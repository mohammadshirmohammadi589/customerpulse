"""Data health reporting utilities for CustomerPulse."""

import pandas as pd

from customerpulse.validation.models import ValidationIssue
from customerpulse.validation.runner import validate_data
from customerpulse.validation.summary import summarize_issues


def build_data_health_report(
    df: pd.DataFrame,
) -> dict:
    """Build a compact data health report."""

    issues: list[ValidationIssue] = validate_data(df)

    summary = summarize_issues(issues)

    report = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "customer_count": (
            df["customer_id"].nunique(dropna=True)
            if "customer_id" in df.columns
            else 0
        ),
        "transaction_count": (
            df["transaction_id"].nunique(dropna=True)
            if "transaction_id" in df.columns
            else 0
        ),
        "duplicate_transaction_record_count": int(df.duplicated().sum()),
        "missing_customer_id": (
            int(df["customer_id"].isna().sum())
            if "customer_id" in df.columns
            else 0
        ),
        "missing_amount": (
            int(df["amount"].isna().sum())
            if "amount" in df.columns
            else 0
        ),
        "issue_summary": summary,
        "issues": issues,
    }

    if "transaction_date" in df.columns:
        dates = pd.to_datetime(
            df["transaction_date"],
            errors="coerce",
        )

        valid_dates = dates.dropna()

        if not valid_dates.empty:
            report["min_transaction_date"] = str(valid_dates.min())
            report["max_transaction_date"] = str(valid_dates.max())

    return report