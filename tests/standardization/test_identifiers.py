import pandas as pd

from customerpulse.standardization.identifiers import (
    normalize_customer_id,
)


def test_customer_id_decimal_suffix_is_removed():
    series = pd.Series(["12345.0"])

    result = normalize_customer_id(series)

    assert result.iloc[0] == "12345"


def test_blank_customer_id_becomes_null():
    series = pd.Series(["   "])

    result = normalize_customer_id(series)

    assert pd.isna(result.iloc[0])


def test_valid_customer_id_is_preserved():
    series = pd.Series(["12345"])

    result = normalize_customer_id(series)

    assert result.iloc[0] == "12345"