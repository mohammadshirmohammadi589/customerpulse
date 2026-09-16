CREATE OR REPLACE TABLE survicate_priority AS
SELECT
    *,
    CASE
        WHEN customer_health = 'HIGH_RISK_SIGNAL'
        THEN 'HIGH'
        WHEN customer_health = 'WATCH'
        THEN 'MEDIUM'
        ELSE 'LOW'
    END AS priority,

    CASE
        WHEN customer_health = 'HIGH_RISK_SIGNAL'
        THEN 'High-value customer with significant engagement decline'
        WHEN customer_health = 'WATCH'
        THEN 'Customer shows declining engagement or weak feedback signal'
        ELSE 'Customer engagement is currently stable'
    END AS priority_reason,

    CASE
        WHEN customer_health = 'HIGH_RISK_SIGNAL'
        THEN 'Customer Success review and targeted feedback follow-up'
        WHEN customer_health = 'WATCH'
        THEN 'Monitor engagement and investigate customer experience'
        ELSE 'Continue normal customer engagement'
    END AS recommended_action

FROM survicate_customer_health;
