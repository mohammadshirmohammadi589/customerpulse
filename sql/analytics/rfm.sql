CREATE OR REPLACE TABLE customer_rfm AS
WITH analysis_date AS (
    SELECT MAX(transaction_date) AS analysis_date
    FROM staging_transactions
)

SELECT
    cm.customer_id,

    DATE_DIFF(
        'day',
        cm.last_transaction_date,
        ad.analysis_date
    ) AS recency,

    cm.transaction_count AS frequency,

    cm.revenue AS monetary

FROM customer_metrics AS cm
CROSS JOIN analysis_date AS ad;