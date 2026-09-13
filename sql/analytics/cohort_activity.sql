CREATE OR REPLACE TABLE customer_cohort_activity AS

SELECT DISTINCT
    customer_id,

    DATE_TRUNC(
        'month',
        transaction_date
    ) AS activity_month

FROM staging_transactions;