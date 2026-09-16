CREATE OR REPLACE TABLE survicate_opportunity_summary AS
SELECT
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (WHERE priority = 'HIGH') AS high_priority_customers,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE priority = 'HIGH') / COUNT(*),
        2
    ) AS high_priority_pct,
    ROUND(
        SUM(historical_customer_value)
        FILTER (WHERE priority = 'HIGH'),
        2
    ) AS high_priority_historical_value,
    ROUND(SUM(historical_customer_value), 2)
        AS total_historical_value,
    ROUND(
        100.0
        * SUM(historical_customer_value)
          FILTER (WHERE priority = 'HIGH')
        / NULLIF(SUM(historical_customer_value), 0),
        2
    ) AS high_priority_value_pct
FROM survicate_priority;
