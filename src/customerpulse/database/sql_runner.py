"""SQL execution utilities for CustomerPulse."""

from pathlib import Path

import duckdb


def execute_sql_file(
    connection: duckdb.DuckDBPyConnection,
    sql_path: str | Path,
):
    """Execute a SQL file and return the query result."""

    file_path = Path(sql_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {file_path}"
        )

    sql = file_path.read_text(
        encoding="utf-8"
    )

    return connection.execute(sql)