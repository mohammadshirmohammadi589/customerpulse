import duckdb

from customerpulse.pipeline import run_pipeline


def test_end_to_end_pipeline():
    connection = run_pipeline(
        "configs/default.yaml"
    )

    tables = connection.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'main'
        """
    ).fetchdf()

    table_names = set(
        tables["table_name"].tolist()
    )

    required_tables = {
        "staging_transactions",
        "customer_metrics",
        "customer_rfm",
        "customer_rfm_scored",
        "customer_cohort",
        "customer_cohort_activity",
        "customer_cohort_periods",
        "cohort_retention",
        "retention_matrix",
        "historical_customer_value",
        "customer_segments",
        "customer_priority",
        "customer_priority_reasons",
        "customer_recommendations",
    }

    assert required_tables.issubset(
        table_names
    )

    staging_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM staging_transactions
        """
    ).fetchone()[0]

    customer_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM customer_metrics
        """
    ).fetchone()[0]

    recommendation_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM customer_recommendations
        """
    ).fetchone()[0]

    assert staging_count == 18532
    assert customer_count == 4338
    assert recommendation_count == 4338

    connection.close()