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
            WHEN amount <= 0 THEN 1
            ELSE 0
        END
    ) AS non_positive_amounts
FROM staging_transactions;