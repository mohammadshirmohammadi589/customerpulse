import sys
from pathlib import Path

sys.path.insert(0, "src")

from customerpulse.database.connection import get_connection
from customerpulse.database.staging import load_standardized_transactions
from customerpulse.standardization.pipeline import standardize_single_file


result = standardize_single_file(
    "data/raw/OnlineRetail.csv"
)

connection = get_connection(":memory:")

load_standardized_transactions(
    connection,
    result.data,
)

for sql_file in [
    "sql/analytics/cohort.sql",
    "sql/analytics/cohort_activity.sql",
    "sql/analytics/cohort_periods.sql",
    "sql/analytics/cohort_retention.sql",
]:
    sql = Path(sql_file).read_text(
        encoding="utf-8"
    )

    connection.execute(sql)


result = connection.execute(
    """
    SELECT
        cohort_month,
        period_number,
        cohort_size,
        retained_customers,
        retention_rate
    FROM cohort_retention
    WHERE cohort_month = DATE '2010-12-01'
    ORDER BY period_number
    """
).fetchdf()


print(result)

connection.close()