CREATE OR REPLACE TABLE customer_recommendations AS
SELECT
    cpr.customer_id,
    cpr.segment,
    cpr.priority,

    cp.historical_customer_value,
    cp.transaction_count,
    cp.first_transaction_date,
    cp.last_transaction_date,

    cpr.priority_reason,

    CASE
        WHEN cpr.segment = 'High Value At Risk'
            THEN 'Win-back and retention outreach'

        WHEN cpr.segment = 'Champions'
            THEN 'Protect relationship and consider loyalty treatment'

        WHEN cpr.segment = 'Loyal Customers'
            THEN 'Retention and relevant upsell opportunities'

        WHEN cpr.segment = 'Recent Customers'
            THEN 'Onboarding and second-purchase engagement'

        ELSE
            'Monitor customer behavior'
    END AS recommended_action,

    CASE
        WHEN cpr.segment = 'High Value At Risk'
            THEN 'Prioritize retention because the customer has historically generated high value but shows weaker recency.'

        WHEN cpr.segment = 'Champions'
            THEN 'Protect a highly engaged customer relationship before inactivity emerges.'

        WHEN cpr.segment = 'Loyal Customers'
            THEN 'Encourage continued engagement and potentially broaden customer value.'

        WHEN cpr.segment = 'Recent Customers'
            THEN 'Focus on converting recent activity into repeat purchasing behavior.'

        ELSE
            'No strong behavioral signal currently justifies a specialized intervention.'
    END AS recommendation_rationale

FROM customer_priority_reasons AS cpr

INNER JOIN customer_priority AS cp
    ON cpr.customer_id = cp.customer_id;