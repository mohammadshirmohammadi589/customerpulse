SELECT
    cp.customer_id,
    cp.segment,
    cp.priority,
    cp.historical_customer_value,
    cp.transaction_count,
    rfm.recency
FROM customer_priority AS cp
INNER JOIN customer_rfm AS rfm
    ON cp.customer_id = rfm.customer_id
WHERE cp.priority = 'HIGH'
ORDER BY cp.historical_customer_value DESC
LIMIT 10;