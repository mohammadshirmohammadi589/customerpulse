import pandas as pd

from customerpulse.analytics.retention import (
    build_retention_matrix,
)
from customerpulse.database.connection import get_connection


def test_build_retention_matrix():
    connection = get_connection(":memory:")

    retention_data = pd.DataFrame(
        {
            "cohort_month": pd.to_datetime(
                [
                    "2024-01-01",
                    "2024-01-01",
                    "2024-01-01",
                    "2024-02-01",
                    "2024-02-01",
                ]
            ),
            "period_number": [
                0,
                1,
                2,
                0,
                1,
            ],
            "cohort_size": [
                100,
                100,
                100,
                50,
                50,
            ],
            "retained_customers": [
                100,
                60,
                40,
                50,
                25,
            ],
            "retention_rate": [
                1.0,
                0.6,
                0.4,
                1.0,
                0.5,
            ],
        }
    )

    connection.register(
        "retention_data",
        retention_data,
    )

    connection.execute(
        """
        CREATE OR REPLACE TABLE cohort_retention AS
        SELECT *
        FROM retention_data
        """
    )

    connection.unregister("retention_data")

    build_retention_matrix(connection)

    result = connection.execute(
        """
        SELECT
            cohort_month,
            month_0,
            month_1,
            month_2
        FROM retention_matrix
        ORDER BY cohort_month
        """
    ).fetchall()

    assert result[0][0] == pd.Timestamp("2024-01-01")
    assert result[0][1] == 1.0
    assert result[0][2] == 0.6
    assert result[0][3] == 0.4

    assert result[1][0] == pd.Timestamp("2024-02-01")
    assert result[1][1] == 1.0
    assert result[1][2] == 0.5
    assert result[1][3] is None

    connection.close()