CREATE OR REPLACE TABLE retention_matrix AS

SELECT
    cohort_month,

    MAX(
        CASE
            WHEN period_number = 0
            THEN retention_rate
        END
    ) AS month_0,

    MAX(
        CASE
            WHEN period_number = 1
            THEN retention_rate
        END
    ) AS month_1,

    MAX(
        CASE
            WHEN period_number = 2
            THEN retention_rate
        END
    ) AS month_2,

    MAX(
        CASE
            WHEN period_number = 3
            THEN retention_rate
        END
    ) AS month_3,

    MAX(
        CASE
            WHEN period_number = 4
            THEN retention_rate
        END
    ) AS month_4,

    MAX(
        CASE
            WHEN period_number = 5
            THEN retention_rate
        END
    ) AS month_5,

    MAX(
        CASE
            WHEN period_number = 6
            THEN retention_rate
        END
    ) AS month_6,

    MAX(
        CASE
            WHEN period_number = 7
            THEN retention_rate
        END
    ) AS month_7,

    MAX(
        CASE
            WHEN period_number = 8
            THEN retention_rate
        END
    ) AS month_8,

    MAX(
        CASE
            WHEN period_number = 9
            THEN retention_rate
        END
    ) AS month_9,

    MAX(
        CASE
            WHEN period_number = 10
            THEN retention_rate
        END
    ) AS month_10,

    MAX(
        CASE
            WHEN period_number = 11
            THEN retention_rate
        END
    ) AS month_11

FROM cohort_retention

GROUP BY cohort_month

ORDER BY cohort_month;