import pandas as pd

from customerpulse.database.connection import get_connection
from customerpulse.database.staging import load_standardized_transactions


def test_load_standardized_transactions():
    df = pd.DataFrame(
        {
            "customer_id": ["C001", "C002"],
            "transaction_id": ["T001", "T002"],
            "transaction_date": pd.to_datetime(
                ["2024-01-01", "2024-01-02"]
            ),
            "amount": [100.0, 250.0],
        }
    )

    connection = get_connection(":memory:")

    load_standardized_transactions(
        connection,
        df,
    )

    result = connection.execute(
        """
        SELECT
            COUNT(*) AS row_count,
            COUNT(DISTINCT transaction_id) AS transaction_count,
            SUM(amount) AS revenue
        FROM staging_transactions
        """
    ).fetchone()

    assert result[0] == 2
    assert result[1] == 2
    assert result[2] == 350.0

    connection.close()