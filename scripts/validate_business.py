from pathlib import Path
import sys

sys.path.insert(0, "src")

from customerpulse.database.connection import get_connection


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "customerpulse.duckdb"
)


def main():
    connection = get_connection(
        DATABASE_PATH
    )

    staging = connection.execute("""
        SELECT
            COUNT(*) AS rows,
            COUNT(DISTINCT transaction_id) AS transactions,
            COUNT(DISTINCT customer_id) AS customers,
            SUM(
                CASE
                    WHEN customer_id IS NULL THEN 1
                    ELSE 0
                END
            ) AS null_customers,
            SUM(
                CASE
                    WHEN transaction_id IS NULL THEN 1
                    ELSE 0
                END
            ) AS null_transactions,
            SUM(
                CASE
                    WHEN amount <= 0 THEN 1
                    ELSE 0
                END
            ) AS non_positive_amounts
        FROM staging_transactions
    """).fetchone()

    rfm = connection.execute("""
        SELECT
            COUNT(*) AS customers,
            SUM(
                CASE
                    WHEN recency < 0 THEN 1
                    ELSE 0
                END
            ) AS negative_recency,
            SUM(
                CASE
                    WHEN frequency <= 0 THEN 1
                    ELSE 0
                END
            ) AS invalid_frequency,
            SUM(
                CASE
                    WHEN monetary <= 0 THEN 1
                    ELSE 0
                END
            ) AS invalid_monetary
        FROM customer_rfm
    """).fetchone()

    decision = connection.execute("""
        SELECT
            COUNT(*) AS customers,
            SUM(
                CASE
                    WHEN priority NOT IN (
                        'HIGH',
                        'MEDIUM',
                        'LOW'
                    )
                    THEN 1
                    ELSE 0
                END
            ) AS invalid_priorities,
            SUM(
                CASE
                    WHEN priority = 'HIGH'
                         AND segment != 'High Value At Risk'
                    THEN 1
                    ELSE 0
                END
            ) AS invalid_high_priority_rules
        FROM customer_priority
    """).fetchone()

    connection.close()

    assert staging[0] == staging[1], (
        "Transaction row count does not match "
        "distinct transaction count."
    )

    assert staging[3] == 0
    assert staging[4] == 0
    assert staging[5] == 0

    assert rfm[1] == 0
    assert rfm[2] == 0
    assert rfm[3] == 0

    assert decision[1] == 0
    assert decision[2] == 0

    print("Business validation passed")
    print(f"Transactions: {staging[0]}")
    print(f"Customers: {staging[2]}")
    print("Staging validation: passed")
    print("RFM validation: passed")
    print("Decision validation: passed")


if __name__ == "__main__":
    main()