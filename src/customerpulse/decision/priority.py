"""Customer priority engine."""

from pathlib import Path

import duckdb


def build_customer_priority(
    connection: duckdb.DuckDBPyConnection,
    sql_path: str | Path = "sql/analytics/customer_priority.sql",
) -> None:
    """Build transparent customer priority tiers."""

    file_path = Path(sql_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {file_path}"
        )

    sql = file_path.read_text(
        encoding="utf-8"
    )

    connection.execute(sql)