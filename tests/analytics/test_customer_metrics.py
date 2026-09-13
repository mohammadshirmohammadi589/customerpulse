import pandas as pd

from customerpulse.analytics.customer_metrics import (
    build_customer_metrics,
)
from customerpulse.database.connection import get_connection
from customerpulse.database.staging import (
    load_standardized_transactions,
)


def test_build_customer_metrics():
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

    result = connection.execute(
        """
        SELECT
            customer_id,
            transaction_count,
            revenue,
            average_transaction_value,
            customer_active_days
        FROM customer_metrics
        ORDER BY customer_id
        """
    ).fetchall()

    assert result[0][0] == "C001"
    assert result[0][1] == 2
    assert result[0][2] == 300.0
    assert result[0][3] == 150.0
    assert result[0][4] == 10

    assert result[1][0] == "C002"
    assert result[1][1] == 1
    assert result[1][2] == 300.0
    assert result[1][3] == 300.0
    assert result[1][4] == 0

    connection.close()