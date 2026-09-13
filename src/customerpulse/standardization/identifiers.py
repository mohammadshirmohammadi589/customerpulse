"""Identifier normalization utilities."""

import pandas as pd


def normalize_customer_id(
    series: pd.Series,
) -> pd.Series:
    """
    Normalize customer identifiers without changing
    their logical identity.
    """

    result = (
        series
        .astype("string")
        .str.strip()
    )

    result = result.str.replace(
        r"\.0$",
        "",
        regex=True,
    )

    result = result.replace(
        {
            "": pd.NA,
            "nan": pd.NA,
            "None": pd.NA,
            "<NA>": pd.NA,
        }
    )

    return result