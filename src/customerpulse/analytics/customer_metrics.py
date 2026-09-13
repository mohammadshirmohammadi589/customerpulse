"""Customer-level analytical metrics for CustomerPulse."""

from pathlib import Path

import duckdb


def build_customer_metrics(
    connection: duckdb.DuckDBPyConnection,
    sql_path: str | Path = "sql/analytics/customer_metrics.sql",
) -> None:
    """Build the customer-level metrics table."""

    file_path = Path(sql_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {file_path}"
        )

    sql = file_path.read_text(
        encoding="utf-8"
    )

    connection.execute(sql)