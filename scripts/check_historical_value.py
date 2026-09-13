import sys
from pathlib import Path

sys.path.insert(0, "src")

from customerpulse.analytics.historical_value import (
    build_historical_customer_value,
)
from customerpulse.database.connection import get_connection
from customerpulse.database.staging import (
    load_standardized_transactions,
)
from customerpulse.standardization.pipeline import (
    standardize_single_file,
)


result = standardize_single_file(
    "data/raw/OnlineRetail.csv"
)

connection = get_connection(":memory:")

load_standardized_transactions(
    connection,
    result.data,
)

sql_files = [
    "sql/analytics/historical_customer_value.sql",
]

for sql_file in sql_files:
    sql = Path(sql_file).read_text(
        encoding="utf-8"
    )

    connection.execute(sql)


result = connection.execute(
    """
    SELECT
        customer_id,
        historical_customer_value,
        qualifying_transaction_count,
        first_transaction_date,
        last_transaction_date
    FROM historical_customer_value
    ORDER BY historical_customer_value DESC
    LIMIT 10
    """
).fetchdf()

print(result)

connection.close()