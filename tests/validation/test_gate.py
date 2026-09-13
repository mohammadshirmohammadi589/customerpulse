from customerpulse.validation.gate import has_blocking_errors
from customerpulse.validation.models import ValidationIssue


def test_error_blocks_pipeline():
    issues = [
        ValidationIssue(
            name="missing_customer_id",
            severity="ERROR",
            description="Customer ID is missing.",
            affected_rows=10,
        )
    ]

    assert has_blocking_errors(issues) is True


def test_warning_does_not_block_pipeline():
    issues = [
        ValidationIssue(
            name="missing_product_name",
            severity="WARNING",
            description="Product name is missing.",
            affected_rows=10,
        )
    ]

    assert has_blocking_errors(issues) is False


def test_no_issues_does_not_block_pipeline():
    issues = []

    assert has_blocking_errors(issues) is False