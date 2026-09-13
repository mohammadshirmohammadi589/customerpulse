import pandas as pd

from customerpulse.analytics.historical_value import (
    build_historical_customer_value,
)
from customerpulse.database.connection import get_connection
from customerpulse.database.staging import (
    load_standardized_transactions,
)


def test_build_historical_customer_value():
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
                    "2024-01-10",
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

    build_historical_customer_value(
        connection
    )

    result = connection.execute(
        """
        SELECT
            customer_id,
            historical_customer_value,
            qualifying_transaction_count
        FROM historical_customer_value
        ORDER BY customer_id
        """
    ).fetchall()

    assert result[0] == (
        "C001",
        300.0,
        2,
    )

    assert result[1] == (
        "C002",
        300.0,
        1,
    )

    connection.close()