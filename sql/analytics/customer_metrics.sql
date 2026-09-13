CREATE OR REPLACE TABLE customer_metrics AS
SELECT
    customer_id,

    COUNT(DISTINCT transaction_id) AS transaction_count,

    SUM(amount) AS revenue,

    MIN(transaction_date) AS first_transaction_date,

    MAX(transaction_date) AS last_transaction_date,

    AVG(amount) AS average_transaction_value,

    DATE_DIFF(
        'day',
        MIN(transaction_date),
        MAX(transaction_date)
    ) AS customer_active_days

FROM staging_transactions

GROUP BY customer_id;