"""DuckDB connection utilities for CustomerPulse."""

from pathlib import Path

import duckdb


def get_connection(
    database_path: str | Path = "data/processed/customerpulse.duckdb",
) -> duckdb.DuckDBPyConnection:
    """Create a DuckDB connection."""

    db_path = Path(database_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    return duckdb.connect(str(db_path))