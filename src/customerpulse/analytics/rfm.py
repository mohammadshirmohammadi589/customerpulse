"""RFM analytics for CustomerPulse."""

from pathlib import Path

import duckdb


def build_rfm(
    connection: duckdb.DuckDBPyConnection,
    sql_path: str | Path = "sql/analytics/rfm.sql",
) -> None:
    """Build the customer-level RFM table."""

    file_path = Path(sql_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {file_path}"
        )

    sql = file_path.read_text(
        encoding="utf-8"
    )

    connection.execute(sql)