CREATE OR REPLACE TABLE cohort_retention AS

WITH cohort_sizes AS (

    SELECT
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size

    FROM customer_cohort

    GROUP BY cohort_month
),

retained_customers AS (

    SELECT
        cohort_month,
        period_number,
        COUNT(DISTINCT customer_id) AS retained_customers

    FROM customer_cohort_periods

    GROUP BY
        cohort_month,
        period_number
)

SELECT
    rc.cohort_month,

    rc.period_number,

    cs.cohort_size,

    rc.retained_customers,

    CAST(rc.retained_customers AS DOUBLE)
        / cs.cohort_size AS retention_rate

FROM retained_customers AS rc

INNER JOIN cohort_sizes AS cs
    ON rc.cohort_month = cs.cohort_month

ORDER BY
    rc.cohort_month,
    rc.period_number;