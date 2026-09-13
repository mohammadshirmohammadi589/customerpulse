CREATE OR REPLACE TABLE customer_cohort AS

SELECT
    customer_id,

    MIN(transaction_date) AS first_transaction_date,

    DATE_TRUNC(
        'month',
        MIN(transaction_date)
    ) AS cohort_month

FROM staging_transactions

GROUP BY customer_id;