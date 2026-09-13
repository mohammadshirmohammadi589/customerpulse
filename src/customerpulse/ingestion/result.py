"""Result models for CustomerPulse ingestion."""

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class IngestionResult:
    """Result returned by an ingestion operation."""

    data: pd.DataFrame
    source_type: str
    source_files: tuple[str, ...]