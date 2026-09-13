from customerpulse.standardization.pipeline import standardize_single_file


def test_standardize_single_file():
    result = standardize_single_file(
        "data/raw/OnlineRetail.csv"
    )

    assert result.input_rows == 541909
    assert result.qualified_rows == 397884
    assert result.standardized_rows == 18532

    assert list(result.data.columns) == [
        "customer_id",
        "transaction_id",
        "transaction_date",
        "amount",
    ]

    assert result.data["transaction_id"].is_unique
    assert result.data["customer_id"].notna().all()
    assert result.data["transaction_date"].notna().all()
    assert (result.data["amount"] > 0).all()