from customerpulse.pipeline import run_pipeline


def test_pipeline_invariants():
    connection = run_pipeline(
        "configs/default.yaml"
    )

    staging = connection.execute(
        """
        SELECT
            COUNT(*) AS rows,
            COUNT(DISTINCT transaction_id) AS transactions,
            COUNT(DISTINCT customer_id) AS customers,
            COUNT(*) FILTER (
                WHERE customer_id IS NULL
            ) AS null_customers,
            COUNT(*) FILTER (
                WHERE transaction_id IS NULL
            ) AS null_transactions,
            COUNT(*) FILTER (
                WHERE transaction_date IS NULL
            ) AS null_dates,
            COUNT(*) FILTER (
                WHERE amount <= 0
            ) AS non_positive_amounts
        FROM staging_transactions
        """
    ).fetchone()

    assert staging[0] > 0
    assert staging[1] == staging[0]
    assert staging[2] > 0
    assert staging[3] == 0
    assert staging[4] == 0
    assert staging[5] == 0
    assert staging[6] == 0

    invalid_priorities = connection.execute(
        """
        SELECT COUNT(*)
        FROM customer_recommendations
        WHERE priority NOT IN (
            'HIGH',
            'MEDIUM',
            'LOW'
        )
        """
    ).fetchone()[0]

    assert invalid_priorities == 0

    connection.close()