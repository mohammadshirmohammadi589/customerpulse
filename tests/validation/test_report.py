import pandas as pd

from customerpulse.validation.report import (
    build_data_quality_report,
)


def test_data_quality_report_contains_expected_metrics():
    raw_df = pd.DataFrame({
        "customer_id": ["1", None, "2"],
        "transaction_id": ["A", "B", "C"],
    })

    qualified_df = pd.DataFrame({
        "customer_id": ["1", "2"],
        "transaction_id": ["A", "C"],
    })

    issues = []

    report = build_data_quality_report(
        raw_df,
        qualified_df,
        issues,
    )

    metrics = set(report["metric"])

    assert "input_rows" in metrics
    assert "qualified_rows" in metrics
    assert "excluded_rows" in metrics
    assert "customers" in metrics
    assert "transactions" in metrics