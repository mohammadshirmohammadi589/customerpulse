CREATE OR REPLACE TABLE survicate_customer_health AS
SELECT
    *,
    CASE
        WHEN engagement_change_pct <= -50
             AND historical_customer_value >= 8000
        THEN 'HIGH_RISK_SIGNAL'

        WHEN engagement_change_pct <= -30
             OR nps_score < 30
        THEN 'WATCH'

        ELSE 'HEALTHY'
    END AS customer_health
FROM survicate_engagement;
