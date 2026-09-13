"""Transaction qualification rules for CustomerPulse."""

import pandas as pd


def qualify_transactions(
    df: pd.DataFrame,
    exclude_transaction_id_prefixes: tuple[str, ...] = (),
) -> pd.DataFrame:
    """Return rows that satisfy the configured qualifying transaction rules."""

    result = df.copy()

    customer_id_valid = (
        result["customer_id"].notna()
        & (result["customer_id"].astype(str).str.strip() != "")
    )

    transaction_id_valid = (
        result["transaction_id"].notna()
        & (result["transaction_id"].astype(str).str.strip() != "")
    )

    transaction_date_valid = (
        pd.to_datetime(
            result["transaction_date"],
            format="%m/%d/%y %H:%M",
            errors="coerce",
        ).notna()
    )

    amount_valid = result["amount"] > 0

    transaction_id_text = (
        result["transaction_id"]
        .astype(str)
        .str.strip()
    )

    cancellation_valid = ~transaction_id_text.str.startswith(
        exclude_transaction_id_prefixes
    )

    qualified = (
        customer_id_valid
        & transaction_id_valid
        & transaction_date_valid
        & amount_valid
        & cancellation_valid
    )

    return result.loc[qualified].copy()