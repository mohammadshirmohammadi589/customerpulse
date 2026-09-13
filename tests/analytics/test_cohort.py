import pandas as pd

from customerpulse.database.connection import get_connection
from customerpulse.database.staging import (
    load_standardized_transactions,
)


def test_cohort_and_retention():
    df = pd.DataFrame(
        {
            "customer_id": [
                "C001",
                "C001",
                "C002",
                "C002",
                "C003",
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
                    "2024-01-10",
                    "2024-02-10",
                    "2024-01-20",
                    "2024-03-20",
                    "2024-02-15",
                ]
            ),
            "amount": [
                100.0,
                100.0,
                200.0,
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

    connection.execute(
        """
        CREATE OR REPLACE TABLE customer_cohort AS
        SELECT
            customer_id,
            MIN(transaction_date) AS first_transaction_date,
            DATE_TRUNC(
                'month',
                MIN(transaction_date)
            ) AS cohort_month
        FROM staging_transactions
        GROUP BY customer_id
        """
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE customer_cohort_activity AS
        SELECT DISTINCT
            customer_id,
            DATE_TRUNC(
                'month',
                transaction_date
            ) AS activity_month
        FROM staging_transactions
        """
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE customer_cohort_periods AS
        SELECT
            ca.customer_id,
            cc.cohort_month,
            ca.activity_month,
            DATE_DIFF(
                'month',
                cc.cohort_month,
                ca.activity_month
            ) AS period_number
        FROM customer_cohort_activity AS ca
        INNER JOIN customer_cohort AS cc
            ON ca.customer_id = cc.customer_id
        """
    )

    result = connection.execute(
        """
        SELECT
            customer_id,
            cohort_month
        FROM customer_cohort
        ORDER BY customer_id
        """
    ).fetchall()

    assert result == [
        ("C001", pd.Timestamp("2024-01-01")),
        ("C002", pd.Timestamp("2024-01-01")),
        ("C003", pd.Timestamp("2024-02-01")),
    ]

    periods = connection.execute(
        """
        SELECT
            customer_id,
            period_number
        FROM customer_cohort_periods
        ORDER BY customer_id, period_number
        """
    ).fetchall()

    assert periods == [
        ("C001", 0),
        ("C001", 1),
        ("C002", 0),
        ("C002", 2),
        ("C003", 0),
    ]

    connection.close()