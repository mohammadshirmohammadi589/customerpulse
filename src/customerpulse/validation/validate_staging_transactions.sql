SELECT
    COUNT(*) AS row_count,
    COUNT(DISTINCT transaction_id) AS transaction_count,
    COUNT(DISTINCT customer_id) AS customer_count,
    SUM(amount) AS revenue,
    SUM(
        CASE
            WHEN customer_id IS NULL THEN 1
            ELSE 0
        END
    ) AS missing_customer_id,
    SUM(
        CASE
            WHEN transaction_id IS NULL THEN 1
            ELSE 0
        END
    ) AS missing_transaction_id,
    SUM(
        CASE
            WHEN transaction_date IS NULL THEN 1
            ELSE 0
        END
    ) AS missing_transaction_date,
    SUM(
        CASE
            WHEN amount IS NULL THEN 1
            ELSE 0
        END
    ) AS missing_amount,
    SUM(
        CASE
            WHEN amount <= 0 THEN 1
            ELSE 0
        END
    ) AS non_positive_amount
FROM staging_transactions;