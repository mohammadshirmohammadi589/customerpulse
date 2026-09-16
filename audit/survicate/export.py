import duckdb

db = "audit/survicate/data/survicate_audit.duckdb"
output = "audit/survicate/data/survicate_customer_health.csv"

con = duckdb.connect(db, read_only=True)

con.execute(f"""
COPY (
    SELECT
        customer_id,
        previous_month_activity,
        current_month_activity,
        engagement_change_pct,
        nps_score,
        historical_customer_value,
        customer_health,
        priority,
        priority_reason,
        recommended_action
    FROM survicate_priority
    ORDER BY
        CASE priority
            WHEN 'HIGH' THEN 1
            WHEN 'MEDIUM' THEN 2
            ELSE 3
        END,
        historical_customer_value DESC
) TO '{output}' (HEADER, DELIMITER ',');
""")

print(f"Exported: {output}")

con.close()
