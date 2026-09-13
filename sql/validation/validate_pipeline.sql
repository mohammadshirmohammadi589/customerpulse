SELECT
    'staging_transactions' AS table_name,
    COUNT(*) AS row_count,
    COUNT(DISTINCT transaction_id) AS distinct_transactions,
    COUNT(DISTINCT customer_id) AS distinct_customers,
    COUNT(*) FILTER (
        WHERE customer_id IS NULL
    ) AS null_customer_ids,
    COUNT(*) FILTER (
        WHERE transaction_id IS NULL
    ) AS null_transaction_ids,
    COUNT(*) FILTER (
        WHERE transaction_date IS NULL
    ) AS null_dates,
    COUNT(*) FILTER (
        WHERE amount <= 0
    ) AS invalid_values
FROM staging_transactions

UNION ALL

SELECT
    'customer_metrics' AS table_name,
    COUNT(*) AS row_count,
    COUNT(DISTINCT customer_id) AS distinct_transactions,
    COUNT(DISTINCT customer_id) AS distinct_customers,
    COUNT(*) FILTER (
        WHERE customer_id IS NULL
    ) AS null_customer_ids,
    NULL AS null_transaction_ids,
    NULL AS null_dates,
    COUNT(*) FILTER (
        WHERE revenue <= 0
    ) AS invalid_values
FROM customer_metrics

UNION ALL

SELECT
    'customer_rfm' AS table_name,
    COUNT(*) AS row_count,
    COUNT(DISTINCT customer_id) AS distinct_transactions,
    COUNT(DISTINCT customer_id) AS distinct_customers,
    COUNT(*) FILTER (
        WHERE customer_id IS NULL
    ) AS null_customer_ids,
    NULL AS null_transaction_ids,
    NULL AS null_dates,
    COUNT(*) FILTER (
        WHERE frequency <= 0
        OR monetary <= 0
    ) AS invalid_values
FROM customer_rfm

UNION ALL

SELECT
    'customer_recommendations' AS table_name,
    COUNT(*) AS row_count,
    COUNT(DISTINCT customer_id) AS distinct_transactions,
    COUNT(DISTINCT customer_id) AS distinct_customers,
    COUNT(*) FILTER (
        WHERE customer_id IS NULL
    ) AS null_customer_ids,
    NULL AS null_transaction_ids,
    NULL AS null_dates,
    COUNT(*) FILTER (
        WHERE priority NOT IN (
            'HIGH',
            'MEDIUM',
            'LOW'
        )
    ) AS invalid_values
FROM customer_recommendations;