import duckdb
import pandas as pd

from customerpulse.decision.priority import (
    build_customer_priority,
)
from customerpulse.decision.pipeline import (
    build_decision_layer,
)


def test_decision_pipeline_integration():
    connection = duckdb.connect(":memory:")

    customer_metrics = pd.DataFrame(
        {
            "customer_id": ["C001", "C002", "C003"],
            "transaction_count": [10, 5, 1],
            "revenue": [5000.0, 2000.0, 100.0],
            "first_transaction_date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-01-01",
                ]
            ),
            "last_transaction_date": pd.to_datetime(
                [
                    "2024-06-01",
                    "2024-06-01",
                    "2024-06-01",
                ]
            ),
            "average_transaction_value": [
                500.0,
                400.0,
                100.0,
            ],
            "customer_active_days": [152, 152, 152],
        }
    )

    historical_value = pd.DataFrame(
        {
            "customer_id": ["C001", "C002", "C003"],
            "historical_customer_value": [
                5000.0,
                2000.0,
                100.0,
            ],
            "qualifying_transaction_count": [10, 5, 1],
            "first_transaction_date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-01-01",
                ]
            ),
            "last_transaction_date": pd.to_datetime(
                [
                    "2024-06-01",
                    "2024-06-01",
                    "2024-06-01",
                ]
            ),
        }
    )

    segments = pd.DataFrame(
        {
            "customer_id": ["C001", "C002", "C003"],
            "segment": [
                "High Value At Risk",
                "Champions",
                "Other",
            ],
        }
    )

    connection.register(
        "customer_metrics_df",
        customer_metrics,
    )

    connection.register(
        "historical_value_df",
        historical_value,
    )

    connection.register(
        "segments_df",
        segments,
    )

    connection.execute("""
        CREATE TABLE customer_metrics AS
        SELECT *
        FROM customer_metrics_df
    """)

    connection.execute("""
        CREATE TABLE historical_customer_value AS
        SELECT *
        FROM historical_value_df
    """)

    connection.execute("""
        CREATE TABLE customer_segments AS
        SELECT *
        FROM segments_df
    """)

    connection.unregister("customer_metrics_df")
    connection.unregister("historical_value_df")
    connection.unregister("segments_df")

    build_customer_priority(connection)

    build_decision_layer(connection)

    customer_count = connection.execute("""
        SELECT COUNT(*)
        FROM customer_recommendations
    """).fetchone()[0]

    transaction_count = connection.execute("""
        SELECT SUM(transaction_count)
        FROM customer_metrics
    """).fetchone()[0]

    priority_table_exists = connection.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'customer_priority'
    """).fetchone()[0] == 1

    recommendations_table_exists = connection.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'customer_recommendations'
    """).fetchone()[0] == 1

    assert customer_count == 3
    assert transaction_count == 16
    assert priority_table_exists
    assert recommendations_table_exists

    result = connection.execute("""
        SELECT
            customer_id,
            segment,
            priority
        FROM customer_recommendations
        ORDER BY customer_id
    """).fetchall()

    assert result == [
        (
            "C001",
            "High Value At Risk",
            "HIGH",
        ),
        (
            "C002",
            "Champions",
            "MEDIUM",
        ),
        (
            "C003",
            "Other",
            "LOW",
        ),
    ]

    connection.close()