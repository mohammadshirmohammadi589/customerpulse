import duckdb
import pandas as pd

from customerpulse.decision.priority import (
    build_customer_priority,
)


def test_build_customer_priority():
    connection = duckdb.connect(":memory:")

    segments = pd.DataFrame(
        {
            "customer_id": [
                "C001",
                "C002",
                "C003",
                "C004",
            ],
            "segment": [
                "High Value At Risk",
                "Champions",
                "Recent Customers",
                "Other",
            ],
        }
    )

    historical_value = pd.DataFrame(
        {
            "customer_id": [
                "C001",
                "C002",
                "C003",
                "C004",
            ],
            "historical_customer_value": [
                5000.0,
                4000.0,
                500.0,
                100.0,
            ],
        }
    )

    metrics = pd.DataFrame(
        {
            "customer_id": [
                "C001",
                "C002",
                "C003",
                "C004",
            ],
            "transaction_count": [10, 20, 2, 1],
            "first_transaction_date": pd.to_datetime(
                [
                    "2020-01-01",
                    "2020-01-01",
                    "2020-01-01",
                    "2020-01-01",
                ]
            ),
            "last_transaction_date": pd.to_datetime(
                [
                    "2020-06-01",
                    "2020-06-01",
                    "2020-06-01",
                    "2020-06-01",
                ]
            ),
        }
    )

    connection.register("segments_df", segments)
    connection.register("historical_value_df", historical_value)
    connection.register("metrics_df", metrics)

    connection.execute("""
        CREATE TABLE customer_segments AS
        SELECT * FROM segments_df
    """)

    connection.execute("""
        CREATE TABLE historical_customer_value AS
        SELECT * FROM historical_value_df
    """)

    connection.execute("""
        CREATE TABLE customer_metrics AS
        SELECT * FROM metrics_df
    """)

    connection.unregister("segments_df")
    connection.unregister("historical_value_df")
    connection.unregister("metrics_df")

    build_customer_priority(connection)

    result = connection.execute("""
        SELECT
            customer_id,
            segment,
            priority
        FROM customer_priority
        ORDER BY customer_id
    """).fetchall()

    assert result == [
        ("C001", "High Value At Risk", "HIGH"),
        ("C002", "Champions", "MEDIUM"),
        ("C003", "Recent Customers", "MEDIUM"),
        ("C004", "Other", "LOW"),
    ]

    connection.close()