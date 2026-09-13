"""Standardization pipeline for CustomerPulse."""

from pathlib import Path

from customerpulse.config.loader import load_config
from customerpulse.ingestion.single_file import ingest_single_file
from customerpulse.standardization.identifiers import normalize_customer_id
from customerpulse.standardization.qualification import qualify_transactions
from customerpulse.standardization.result import StandardizationResult
from customerpulse.standardization.schema import validate_standardized_schema
from customerpulse.standardization.transactions import aggregate_to_transaction_level


def standardize_single_file(
    path: str | Path,
    config_path: str | Path = "configs/default.yaml",
) -> StandardizationResult:
    """Standardize a single source file."""

    config = load_config(config_path)

    ingestion_result = ingest_single_file(
        path,
        config_path=config_path,
    )

    input_rows = len(ingestion_result.data)

    prefixes = tuple(
        config.get("qualification", {}).get(
            "exclude_transaction_id_prefixes",
            [],
        )
    )

    qualified = qualify_transactions(
        ingestion_result.data,
        exclude_transaction_id_prefixes=prefixes,
    )

    qualified["customer_id"] = normalize_customer_id(
        qualified["customer_id"]
    )

    qualified_rows = len(qualified)

    transactions = aggregate_to_transaction_level(
        qualified
    )

    schema_issues = validate_standardized_schema(
        transactions
    )

    if schema_issues:
        raise ValueError(
            "Standardized schema validation failed: "
            f"{schema_issues}"
        )

    return StandardizationResult(
        data=transactions,
        source_type=ingestion_result.source_type,
        input_rows=input_rows,
        qualified_rows=qualified_rows,
        standardized_rows=len(transactions),
    )
