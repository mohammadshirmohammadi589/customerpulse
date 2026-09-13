import pandas as pd

from customerpulse.standardization.qualification import (
    qualify_transactions,
)


def make_transaction(
    customer_id="12345",
    transaction_id="10001",
    transaction_date="12/1/10 8:26",
    amount=10.0,
):
    return {
        "customer_id": customer_id,
        "transaction_id": transaction_id,
        "transaction_date": transaction_date,
        "amount": amount,
    }


def test_missing_customer_is_excluded():
    df = pd.DataFrame([
        make_transaction(customer_id=None),
    ])

    result = qualify_transactions(df)

    assert len(result) == 0


def test_non_positive_amount_is_excluded():
    df = pd.DataFrame([
        make_transaction(amount=0),
        make_transaction(
            transaction_id="10002",
            amount=-5,
        ),
    ])

    result = qualify_transactions(df)

    assert len(result) == 0


def test_cancellation_is_excluded():
    df = pd.DataFrame([
        make_transaction(
            transaction_id="C10001",
        ),
    ])

    result = qualify_transactions(
        df,
        exclude_transaction_id_prefixes=("C",),
    )

    assert len(result) == 0


def test_invalid_date_is_excluded():
    df = pd.DataFrame([
        make_transaction(
            transaction_date="not-a-date",
        ),
    ])

    result = qualify_transactions(df)

    assert len(result) == 0


def test_valid_transaction_is_included():
    df = pd.DataFrame([
        make_transaction(),
    ])

    result = qualify_transactions(df)

    assert len(result) == 1