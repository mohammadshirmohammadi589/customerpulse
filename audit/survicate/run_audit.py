import duckdb

DB_PATH = "audit/survicate/data/survicate_audit.duckdb"

con = duckdb.connect(DB_PATH)

sql_files = [
    "audit/survicate/sql/engagement.sql",
    "audit/survicate/sql/customer_health.sql",
    "audit/survicate/sql/priority.sql",
    "audit/survicate/sql/opportunity.sql",
]

for sql_file in sql_files:
    with open(sql_file, "r", encoding="utf-8") as f:
        con.execute(f.read())

print("Survicate audit SQL completed.")
print()

df = con.execute("""
    SELECT
        customer_id,
        engagement_change_pct,
        nps_score,
        historical_customer_value,
        customer_health,
        priority
    FROM survicate_priority
    ORDER BY
        CASE priority
            WHEN 'HIGH' THEN 1
            WHEN 'MEDIUM' THEN 2
            ELSE 3
        END,
        historical_customer_value DESC
""").fetchdf()

print(df.to_string(index=False))

print()
print("Opportunity Summary")
print(
    con.execute("""
        SELECT *
        FROM survicate_opportunity_summary
    """).fetchdf().to_string(index=False)
)

con.close()
