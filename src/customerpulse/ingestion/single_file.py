"""Single-file ingestion for CustomerPulse."""

from pathlib import Path

import pandas as pd

from customerpulse.config.loader import load_config
from customerpulse.ingestion.loader import load_csv
from customerpulse.ingestion.mapping import get_mappings_from_config
from customerpulse.ingestion.result import IngestionResult
from customerpulse.ingestion.transform import add_amount_column


def ingest_single_file(
    path: str | Path,
    config_path: str | Path = "configs/default.yaml",
) -> IngestionResult:
    """Load, map, transform, and return a single-file ingestion result."""

    config = load_config(config_path)

    df = load_csv(path)

    mappings = get_mappings_from_config(config)

    result = pd.DataFrame()

    for mapping in mappings:
        result[mapping.canonical_field] = df[mapping.source_column]

    quantity_column = config["amount"]["quantity_column"]
    unit_price_column = config["amount"]["unit_price_column"]

    result[quantity_column] = df[quantity_column]
    result[unit_price_column] = df[unit_price_column]

    result = add_amount_column(
        result,
        quantity_column=quantity_column,
        unit_price_column=unit_price_column,
    )

    result = result[
        [
            "customer_id",
            "transaction_id",
            "transaction_date",
            "amount",
            "product_id",
            "product_name",
        ]
    ]

    return IngestionResult(
        data=result,
        source_type="single_file",
        source_files=(str(path),),
    )