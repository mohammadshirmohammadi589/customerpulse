from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "customerpulse.duckdb"
)


def get_connection():
    return duckdb.connect(
        str(DATABASE_PATH),
        read_only=True,
    )


def get_kpis():
    connection = get_connection()

    result = connection.execute(
        """
        SELECT
            COUNT(*) AS customer_count,
            SUM(transaction_count) AS transaction_count,
            SUM(revenue) AS total_revenue,
            AVG(revenue) AS average_customer_revenue
        FROM customer_metrics
        """
    ).fetchdf()

    connection.close()

    return result

def get_data_health():
    connection = get_connection()

    result = connection.execute("""
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
    """).fetchdf()

    connection.close()

    return result


def get_customer_segments():
    connection = get_connection()

    result = connection.execute(
        """
        SELECT
            segment,
            COUNT(*) AS customer_count
        FROM customer_segments
        GROUP BY segment
        ORDER BY customer_count DESC
        """
    ).fetchdf()

    connection.close()

    return result


def get_priority_customers():
    connection = get_connection()

    result = connection.execute(
        """
        SELECT
            cr.customer_id,
            cr.segment,
            hcv.historical_customer_value,
            hcv.qualifying_transaction_count AS transaction_count,
            cr.priority,
            cr.priority_reason,
            cr.recommended_action,
            cr.recommendation_rationale
        FROM customer_recommendations AS cr
        INNER JOIN historical_customer_value AS hcv
            ON cr.customer_id = hcv.customer_id
        ORDER BY
            CASE cr.priority
                WHEN 'HIGH' THEN 1
                WHEN 'MEDIUM' THEN 2
                WHEN 'LOW' THEN 3
            END,
            hcv.historical_customer_value DESC
        """
    ).fetchdf()

    connection.close()

    return result


def get_retention_matrix():
    connection = get_connection()

    result = connection.execute(
        """
        SELECT *
        FROM retention_matrix
        ORDER BY cohort_month
        """
    ).fetchdf()

    connection.close()

    return result