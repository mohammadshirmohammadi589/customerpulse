from pathlib import Path

import pandas as pd

from customerpulse.ingestion.result import IngestionResult


def ingest_two_files(
    customers_path: str | Path,
    transactions_path: str | Path,
) -> IngestionResult:
    customers_file = Path(customers_path)
    transactions_file = Path(transactions_path)

    if not customers_file.exists():
        raise FileNotFoundError(
            f"Customers file not found: {customers_file}"
        )

    if not transactions_file.exists():
        raise FileNotFoundError(
            f"Transactions file not found: {transactions_file}"
        )

    customers = pd.read_csv(
        customers_file,
        encoding="latin1",
    )

    transactions = pd.read_csv(
        transactions_file,
        encoding="latin1",
    )

    required_customer_columns = {
        "customer_id",
    }

    required_transaction_columns = {
        "transaction_id",
        "customer_id",
        "transaction_date",
        "amount",
    }

    missing_customer = (
        required_customer_columns
        - set(customers.columns)
    )

    missing_transaction = (
        required_transaction_columns
        - set(transactions.columns)
    )

    if missing_customer:
        raise ValueError(
            "Missing customer columns: "
            f"{sorted(missing_customer)}"
        )

    if missing_transaction:
        raise ValueError(
            "Missing transaction columns: "
            f"{sorted(missing_transaction)}"
        )

    customer_ids = set(
        customers["customer_id"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    transactions = transactions.copy()

    transaction_customer_ids = (
        transactions["customer_id"]
        .astype(str)
        .str.strip()
    )

    transactions["customer_id"] = (
        transaction_customer_ids
    )

    transactions["transaction_date"] = pd.to_datetime(
        transactions["transaction_date"],
        errors="coerce",
    )

    orphan_mask = (
        transactions["customer_id"]
        .isin(customer_ids)
        .eq(False)
    )

    if orphan_mask.any():
        orphan_count = int(orphan_mask.sum())

        raise ValueError(
            "Transactions contain customer IDs "
            f"not found in customers.csv: {orphan_count}"
        )

    output_columns = [
        "customer_id",
        "transaction_id",
        "transaction_date",
        "amount",
    ]

    optional_columns = [
        "product_id",
        "product_name",
    ]

    output_columns.extend(
        column
        for column in optional_columns
        if column in transactions.columns
    )

    result = transactions[output_columns].copy()

    return IngestionResult(
        data=result,
        source_type="two_file",
        source_files=(
            str(customers_file),
            str(transactions_file),
        ),
    )