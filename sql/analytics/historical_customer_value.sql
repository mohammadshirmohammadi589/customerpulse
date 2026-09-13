CREATE OR REPLACE TABLE historical_customer_value AS

SELECT
    customer_id,

    SUM(amount) AS historical_customer_value,

    COUNT(DISTINCT transaction_id) AS qualifying_transaction_count,

    MIN(transaction_date) AS first_transaction_date,

    MAX(transaction_date) AS last_transaction_date

FROM staging_transactions

GROUP BY customer_id;