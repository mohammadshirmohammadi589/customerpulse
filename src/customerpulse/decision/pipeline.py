"""Decision layer pipeline for CustomerPulse."""

from pathlib import Path

import duckdb

from customerpulse.decision.priority import build_customer_priority


def _execute_sql_file(
    connection: duckdb.DuckDBPyConnection,
    sql_path: str | Path,
) -> None:
    """Execute one SQL file against the active DuckDB connection."""

    file_path = Path(sql_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {file_path}"
        )

    sql = file_path.read_text(
        encoding="utf-8"
    )

    connection.execute(sql)


def build_decision_layer(
    connection: duckdb.DuckDBPyConnection,
) -> None:
    """Build the complete customer decision layer."""

    build_customer_priority(
        connection
    )

    _execute_sql_file(
        connection,
        "sql/analytics/customer_priority_reasons.sql",
    )

    _execute_sql_file(
        connection,
        "sql/analytics/customer_recommendations.sql",
    )