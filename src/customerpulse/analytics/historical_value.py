"""Historical customer value analytics for CustomerPulse."""

from pathlib import Path

import duckdb


def build_historical_customer_value(
    connection: duckdb.DuckDBPyConnection,
    sql_path: str | Path = (
        "sql/analytics/historical_customer_value.sql"
    ),
) -> None:
    """Build historical realized customer value."""

    file_path = Path(sql_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {file_path}"
        )

    sql = file_path.read_text(
        encoding="utf-8"
    )

    connection.execute(sql)