"""Customer segmentation analytics for CustomerPulse."""

from pathlib import Path

import duckdb


def build_customer_segments(
    connection: duckdb.DuckDBPyConnection,
    sql_path: str | Path = (
        "sql/analytics/customer_segments.sql"
    ),
) -> None:
    """Build transparent RFM-based customer segments."""

    file_path = Path(sql_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {file_path}"
        )

    sql = file_path.read_text(
        encoding="utf-8"
    )

    connection.execute(sql)