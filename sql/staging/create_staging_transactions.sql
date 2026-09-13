CREATE OR REPLACE TABLE staging_transactions AS
SELECT
    CAST(customer_id AS VARCHAR) AS customer_id,
    CAST(transaction_id AS VARCHAR) AS transaction_id,
    CAST(transaction_date AS TIMESTAMP) AS transaction_date,
    CAST(amount AS DOUBLE) AS amount
FROM standardized_transactions;