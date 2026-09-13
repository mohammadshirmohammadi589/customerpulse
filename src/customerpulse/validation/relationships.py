import pandas as pd


def find_orphan_customer_ids(
    customers: pd.DataFrame,
    transactions: pd.DataFrame,
) -> pd.Series:
    customer_ids = set(
        customers["customer_id"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    transaction_customer_ids = (
        transactions["customer_id"]
        .astype(str)
        .str.strip()
    )

    return transaction_customer_ids[
        ~transaction_customer_ids.isin(customer_ids)
    ]