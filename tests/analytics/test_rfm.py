import pandas as pd

from customerpulse.analytics.customer_metrics import (
    build_customer_metrics,
)
from customerpulse.analytics.rfm import build_rfm
from customerpulse.database.connection import get_connection
from customerpulse.database.staging import (
    load_standardized_transactions,
)


def test_build_rfm():
    df = pd.DataFrame(
        {
            "customer_id": [
                "C001",
                "C001",
                "C002",
            ],
            "transaction_id": [
                "T001",
                "T002",
                "T003",
            ],
            "transaction_date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-11",
                    "2024-01-05",
                ]
            ),
            "amount": [
                100.0,
                200.0,
                300.0,
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

    result = connection.execute(
        """
        SELECT
            customer_id,
            recency,
            frequency,
            monetary
        FROM customer_rfm
        ORDER BY customer_id
        """
    ).fetchall()

    assert result[0] == (
        "C001",
        0,
        2,
        300.0,
    )

    assert result[1] == (
        "C002",
        6,
        1,
        300.0,
    )

    connection.close()