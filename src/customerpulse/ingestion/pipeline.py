"""Unified ingestion pipeline for CustomerPulse."""

from customerpulse.ingestion.result import IngestionResult
from customerpulse.ingestion.single_file import ingest_single_file
from customerpulse.ingestion.two_file import ingest_two_files


def ingest_from_config(
    config: dict,
    config_path: str = "configs/default.yaml",
) -> IngestionResult:
    """Ingest data according to the configured source type."""

    source_type = config["source"]["type"]

    if source_type == "single_file":
        return ingest_single_file(
            config["source"]["path"],
            config_path=config_path,
        )

    if source_type == "two_file":
        return ingest_two_files(
            customers_path=config["source"]["customers_path"],
            transactions_path=config["source"]["transactions_path"],
        )

    raise ValueError(
        f"Unsupported source type: {source_type}"
    )