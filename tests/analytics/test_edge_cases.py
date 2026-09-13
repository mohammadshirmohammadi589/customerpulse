import pandas as pd

from customerpulse.standardization.identifiers import (
    normalize_customer_id,
)
from customerpulse.standardization.qualification import (
    qualify_transactions,
)
from customerpulse.standardization.transactions import (
    aggregate_to_transaction_level,
)


def test_customer_id_normalization_removes_float_suffix():
    series = pd.Series(
        ["12345.0", "67890", None, ""]
    )

    result = normalize_customer_id(series)

    assert result.iloc[0] == "12345"
    assert result.iloc[1] == "67890"
    assert pd.isna(result.iloc[2])
    assert pd.isna(result.iloc[3])


def test_non_positive_amounts_are_excluded():
    df = pd.DataFrame(
        {
            "customer_id": ["1", "2", "3"],
            "transaction_id": ["A", "B", "C"],
            "transaction_date": [
                "12/01/10 08:26",
                "12/01/10 08:27",
                "12/01/10 08:28",
            ],
            "amount": [100.0, 0.0, -10.0],
        }
    )

    result = qualify_transactions(df)

    assert len(result) == 1
    assert result.iloc[0]["transaction_id"] == "A"


def test_duplicate_line_items_are_aggregated_to_transaction():
    df = pd.DataFrame(
        {
            "customer_id": ["1", "1"],
            "transaction_id": ["INV1", "INV1"],
            "transaction_date": [
                "12/01/10 08:26",
                "12/01/10 08:26",
            ],
            "amount": [10.0, 20.0],
        }
    )

    result = aggregate_to_transaction_level(df)

    assert len(result) == 1
    assert result.iloc[0]["transaction_id"] == "INV1"
    assert result.iloc[0]["amount"] == 30.0