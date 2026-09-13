"""RFM scoring analytics for CustomerPulse."""

from pathlib import Path

import duckdb


def build_rfm_scoring(
    connection: duckdb.DuckDBPyConnection,
    sql_path: str | Path = "sql/analytics/rfm_scoring.sql",
) -> None:
    """Build the scored RFM table."""

    file_path = Path(sql_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {file_path}"
        )

    sql = file_path.read_text(
        encoding="utf-8"
    )

    connection.execute(sql)