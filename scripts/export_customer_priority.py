import sys
from pathlib import Path

sys.path.insert(0, "src")

from customerpulse.database.connection import get_connection


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "customerpulse.duckdb"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "customer_priority.csv"
)

def main() -> None:
    connection = get_connection(DATABASE_PATH)

    result = connection.execute(
    """
    SELECT
    customer_id,
    segment,
    priority,
    historical_customer_value,
    transaction_count,
    first_transaction_date,
    last_transaction_date,
    priority_reason,
    recommended_action,
    recommendation_rationale
FROM customer_recommendations
ORDER BY
    CASE priority
        WHEN 'HIGH' THEN 1
        WHEN 'MEDIUM' THEN 2
        WHEN 'LOW' THEN 3
    END,
    historical_customer_value DESC
    """
).fetchdf()

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    connection.close()

    print(f"Exported {len(result)} customers")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()