"""Retention analytics for CustomerPulse."""

from pathlib import Path

import duckdb


def build_retention_matrix(
    connection: duckdb.DuckDBPyConnection,
    sql_path: str | Path = "sql/analytics/retention_matrix.sql",
) -> None:
    """Build the cohort retention matrix."""

    file_path = Path(sql_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {file_path}"
        )

    sql = file_path.read_text(
        encoding="utf-8"
    )

    connection.execute(sql)