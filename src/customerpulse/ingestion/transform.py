"""Transformation utilities for CustomerPulse ingestion."""

import pandas as pd


def add_amount_column(
    df: pd.DataFrame,
    quantity_column: str,
    unit_price_column: str,
) -> pd.DataFrame:
    """Add transaction amount using quantity multiplied by unit price."""

    result = df.copy()

    result["amount"] = (
        result[quantity_column] * result[unit_price_column]
    )

    return result