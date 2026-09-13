SELECT
    COUNT(*) AS customers,
    SUM(
        CASE
            WHEN recency < 0 THEN 1
            ELSE 0
        END
    ) AS negative_recency,
    SUM(
        CASE
            WHEN frequency <= 0 THEN 1
            ELSE 0
        END
    ) AS invalid_frequency,
    SUM(
        CASE
            WHEN monetary <= 0 THEN 1
            ELSE 0
        END
    ) AS invalid_monetary
FROM customer_rfm;