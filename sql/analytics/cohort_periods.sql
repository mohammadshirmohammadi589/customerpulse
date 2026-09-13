CREATE OR REPLACE TABLE customer_cohort_periods AS

SELECT
    ca.customer_id,

    cc.cohort_month,

    ca.activity_month,

    DATE_DIFF(
        'month',
        cc.cohort_month,
        ca.activity_month
    ) AS period_number

FROM customer_cohort_activity AS ca

INNER JOIN customer_cohort AS cc
    ON ca.customer_id = cc.customer_id;