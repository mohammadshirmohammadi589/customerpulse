import duckdb

DB_PATH = "audit/survicate/data/survicate_audit.duckdb"

c = duckdb.connect(DB_PATH, read_only=True)

total = c.execute(
    "SELECT COUNT(*) FROM survicate_priority"
).fetchone()[0]

high = c.execute(
    "SELECT COUNT(*) FROM survicate_priority WHERE priority='HIGH'"
).fetchone()[0]

medium = c.execute(
    "SELECT COUNT(*) FROM survicate_priority WHERE priority='MEDIUM'"
).fetchone()[0]

low = c.execute(
    "SELECT COUNT(*) FROM survicate_priority WHERE priority='LOW'"
).fetchone()[0]

assert total == 20
assert high + medium + low == total

assert c.execute("""
    SELECT COUNT(*)
    FROM survicate_priority
    WHERE priority = 'HIGH'
      AND customer_health != 'HIGH_RISK_SIGNAL'
""").fetchone()[0] == 0

assert c.execute("""
    SELECT COUNT(*)
    FROM survicate_priority
    WHERE engagement_change_pct IS NULL
""").fetchone()[0] == 0

summary = c.execute("""
    SELECT *
    FROM survicate_opportunity_summary
""").fetchone()

assert summary[0] == total
assert summary[1] == high

print("Survicate audit validation passed.")
print(f"Customers: {total}")
print(f"HIGH: {high}")
print(f"MEDIUM: {medium}")
print(f"LOW: {low}")
print(f"HIGH %: {summary[2]}")
print(f"HIGH historical value %: {summary[5]}")

c.close()
