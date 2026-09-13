CREATE OR REPLACE TABLE customer_priority AS

SELECT
    cs.customer_id,
    cs.segment,
    hcv.historical_customer_value,
    cm.transaction_count,
    cm.first_transaction_date,
    cm.last_transaction_date,

    CASE
        WHEN cs.segment = 'High Value At Risk'
            THEN 'HIGH'

        WHEN cs.segment IN (
            'Champions',
            'Loyal Customers',
            'Recent Customers'
        )
            THEN 'MEDIUM'

        ELSE 'LOW'
    END AS priority

FROM customer_segments AS cs

INNER JOIN historical_customer_value AS hcv
    ON cs.customer_id = hcv.customer_id

INNER JOIN customer_metrics AS cm
    ON cs.customer_id = cm.customer_id;