"""Result models for CustomerPulse standardization."""

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class StandardizationResult:
    """Result returned by a standardization operation."""

    data: pd.DataFrame
    source_type: str
    input_rows: int
    qualified_rows: int
    standardized_rows: int