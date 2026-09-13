CREATE OR REPLACE TABLE customer_priority_reasons AS

SELECT
    customer_id,
    segment,
    priority,

    CASE
        WHEN segment = 'High Value At Risk'
            THEN 'High historical value combined with at-risk recency'

        WHEN segment = 'Champions'
            THEN 'Highly recent, frequent, and high-value customer'

        WHEN segment = 'Loyal Customers'
            THEN 'Frequent customer with strong recent activity'

        WHEN segment = 'Recent Customers'
            THEN 'Recent customer with limited purchase history'

        ELSE
            'No immediate high-priority behavioral signal'
    END AS priority_reason

FROM customer_priority;
