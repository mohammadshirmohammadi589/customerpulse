import pandas as pd

from customerpulse.analytics.customer_metrics import (
    build_customer_metrics,
)
from customerpulse.analytics.rfm import build_rfm
from customerpulse.analytics.rfm_scoring import (
    build_rfm_scoring,
)
from customerpulse.database.connection import get_connection
from customerpulse.database.staging import (
    load_standardized_transactions,
)


def test_build_rfm_scoring():
    df = pd.DataFrame(
        {
            "customer_id": [
                "C001",
                "C001",
                "C002",
                "C003",
                "C004",
            ],
            "transaction_id": [
                "T001",
                "T002",
                "T003",
                "T004",
                "T005",
            ],
            "transaction_date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-10",
                    "2024-01-08",
                    "2024-01-09",
                    "2024-01-10",
                ]
            ),
            "amount": [
                100.0,
                200.0,
                300.0,
                400.0,
                500.0,
            ],
        }
    )

    connection = get_connection(":memory:")

    load_standardized_transactions(
        connection,
        df,
    )

    build_customer_metrics(connection)
    build_rfm(connection)
    build_rfm_scoring(connection)

    result = connection.execute(
        """
        SELECT
            customer_id,
            recency_score,
            frequency_score,
            monetary_score,
            rfm_score
        FROM customer_rfm_scored
        """
    ).fetchdf()

    assert len(result) == 4

    assert result["recency_score"].between(1, 5).all()
    assert result["frequency_score"].between(1, 5).all()
    assert result["monetary_score"].between(1, 5).all()

    assert result["rfm_score"].str.len().eq(3).all()

    connection.close()