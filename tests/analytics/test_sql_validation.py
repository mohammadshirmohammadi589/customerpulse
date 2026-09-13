import pandas as pd

from customerpulse.database.connection import get_connection
from customerpulse.database.sql_runner import execute_sql_file
from customerpulse.database.staging import load_standardized_transactions


def test_staging_validation_sql():
    df = pd.DataFrame(
        {
            "customer_id": ["C001", "C001", "C002"],
            "transaction_id": ["T001", "T002", "T003"],
            "transaction_date": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-02",
                    "2024-01-03",
                ]
            ),
            "amount": [100.0, 150.0, 250.0],
        }
    )

    connection = get_connection(":memory:")

    load_standardized_transactions(
        connection,
        df,
    )

    result = execute_sql_file(
        connection,
        "sql/validation/validate_staging_transactions.sql",
    ).fetchone()

    assert result[0] == 3
    assert result[1] == 3
    assert result[2] == 2
    assert result[3] == 500.0
    assert result[4] == 0
    assert result[5] == 0
    assert result[6] == 0
    assert result[7] == 0
    assert result[8] == 0

    connection.close()