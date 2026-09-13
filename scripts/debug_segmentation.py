import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, "src")

from customerpulse.analytics.segmentation import (
    build_customer_segments,
)
from customerpulse.database.connection import get_connection


connection = get_connection(":memory:")

rfm_data = pd.DataFrame(
    {
        "customer_id": [
            "C001",
            "C002",
            "C003",
            "C004",
            "C005",
        ],
        "recency": [5, 20, 80, 5, 50],
        "frequency": [20, 15, 10, 2, 1],
        "monetary": [
            5000.0,
            3000.0,
            4000.0,
            500.0,
            100.0,
        ],
        "recency_score": [5, 4, 1, 5, 2],
        "frequency_score": [5, 5, 3, 1, 1],
        "monetary_score": [5, 4, 5, 2, 1],
        "rfm_score": [
            "555",
            "454",
            "135",
            "512",
            "211",
        ],
    }
)

connection.register(
    "rfm_data",
    rfm_data,
)

connection.execute(
    """
    CREATE OR REPLACE TABLE customer_rfm_scored AS
    SELECT *
    FROM rfm_data
    """
)

connection.unregister("rfm_data")

print("Before segmentation:")

print(
    connection.execute(
        """
        SELECT *
        FROM customer_rfm_scored
        """
    ).fetchdf()
)

build_customer_segments(connection)

print()
print("After segmentation:")

print(
    connection.execute(
        """
        SELECT
            customer_id,
            rfm_score,
            segment
        FROM customer_segments
        ORDER BY customer_id
        """
    ).fetchdf()
)

connection.close()