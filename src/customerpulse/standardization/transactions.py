"""Transaction-level standardization utilities."""

import pandas as pd


def aggregate_to_transaction_level(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate qualified line items to transaction-level records."""

    result = df.copy()

    result["transaction_date"] = pd.to_datetime(
        result["transaction_date"],
        format="%m/%d/%y %H:%M",
        errors="coerce",
    )

    transactions = (
        result.groupby(
            "transaction_id",
            as_index=False,
        )
        .agg(
            customer_id=("customer_id", "first"),
            transaction_date=("transaction_date", "first"),
            amount=("amount", "sum"),
        )
    )

    return transactions[
        [
            "customer_id",
            "transaction_id",
            "transaction_date",
            "amount",
        ]
    ]