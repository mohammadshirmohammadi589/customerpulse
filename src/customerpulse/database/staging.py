"""DuckDB staging layer for CustomerPulse."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

STAGING_SQL_PATH = (
    PROJECT_ROOT
    / "sql"
    / "staging"
    / "create_staging_transactions.sql"
)


def load_standardized_transactions(
    connection,
    df: pd.DataFrame,
) -> None:
    """Load standardized transactions into DuckDB staging."""

    connection.register(
        "standardized_transactions",
        df,
    )

    sql = STAGING_SQL_PATH.read_text(
        encoding="utf-8",
    )

    connection.execute(sql)

    connection.unregister(
        "standardized_transactions",
    )