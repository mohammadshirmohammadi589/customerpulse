CREATE OR REPLACE TABLE customer_segments AS

SELECT
    customer_id,

    recency,
    frequency,
    monetary,

    recency_score,
    frequency_score,
    monetary_score,

    rfm_score,

    CASE
        WHEN
            recency_score >= 5
            AND frequency_score >= 4
            AND monetary_score >= 4
        THEN 'Champions'

        WHEN
            frequency_score >= 4
            AND recency_score >= 3
        THEN 'Loyal Customers'

        WHEN
            monetary_score >= 4
            AND recency_score <= 2
        THEN 'High Value At Risk'

        WHEN
            recency_score >= 4
            AND frequency_score <= 2
        THEN 'Recent Customers'

        ELSE 'Other'
    END AS segment

FROM customer_rfm_scored;