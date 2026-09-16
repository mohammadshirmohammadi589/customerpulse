CREATE OR REPLACE TABLE survicate_engagement AS
SELECT
    customer_id,
    previous_month_activity,
    current_month_activity,
    ROUND(
        100.0 * (current_month_activity - previous_month_activity)
        / NULLIF(previous_month_activity, 0),
        2
    ) AS engagement_change_pct,
    survey_count_previous,
    survey_count_current,
    response_count_previous,
    response_count_current,
    nps_score,
    historical_customer_value
FROM read_csv(
    'audit/survicate/data/customer_engagement.csv',
    delim=',',
    header=true
);
