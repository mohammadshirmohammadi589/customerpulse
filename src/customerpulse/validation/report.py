"""Data quality report generation for CustomerPulse."""

from pathlib import Path

import pandas as pd


def build_data_quality_report(
    raw_df: pd.DataFrame,
    qualified_df: pd.DataFrame,
    validation_issues,
) -> pd.DataFrame:
    """Build a compact data quality report."""

    errors = sum(
        issue.severity == "ERROR"
        for issue in validation_issues
    )

    warnings = sum(
        issue.severity == "WARNING"
        for issue in validation_issues
    )

    report = pd.DataFrame([
        {
            "metric": "input_rows",
            "value": len(raw_df),
        },
        {
            "metric": "qualified_rows",
            "value": len(qualified_df),
        },
        {
            "metric": "excluded_rows",
            "value": len(raw_df) - len(qualified_df),
        },
        {
            "metric": "customers",
            "value": qualified_df["customer_id"].nunique(),
        },
        {
            "metric": "transactions",
            "value": qualified_df["transaction_id"].nunique(),
        },
        {
            "metric": "validation_errors",
            "value": errors,
        },
        {
            "metric": "validation_warnings",
            "value": warnings,
        },
    ])

    return report


def save_data_quality_report(
    report: pd.DataFrame,
    output_path: str | Path,
) -> None:
    """Save the data quality report as CSV."""

    output = Path(output_path)
    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report.to_csv(
        output,
        index=False,
    )