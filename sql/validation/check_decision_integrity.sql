SELECT
    COUNT(*) AS customers,
    SUM(
        CASE
            WHEN priority NOT IN ('HIGH', 'MEDIUM', 'LOW')
            THEN 1
            ELSE 0
        END
    ) AS invalid_priorities,
    SUM(
        CASE
            WHEN priority = 'HIGH'
                 AND segment != 'High Value At Risk'
            THEN 1
            ELSE 0
        END
    ) AS invalid_high_priority_rules
FROM customer_priority;