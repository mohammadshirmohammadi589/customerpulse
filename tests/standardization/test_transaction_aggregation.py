import pandas as pd

from customerpulse.standardization.transactions import (
    aggregate_to_transaction_level,
)


def test_line_items_are_aggregated_to_one_transaction():
    df = pd.DataFrame([
        {
            "customer_id": "12345",
            "transaction_id": "10001",
            "transaction_date": "12/1/10 8:26",
            "amount": 10.0,
        },
        {
            "customer_id": "12345",
            "transaction_id": "10001",
            "transaction_date": "12/1/10 8:26",
            "amount": 20.0,
        },
    ])

    result = aggregate_to_transaction_level(df)

    assert len(result) == 1
    assert result.iloc[0]["transaction_id"] == "10001"
    assert result.iloc[0]["amount"] == 30.0