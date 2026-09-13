"""Models for CustomerPulse data ingestion."""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class SourceFile:
    """Description of one source file used by the ingestion layer."""

    path: str
    role: str


@dataclass(frozen=True)
class SourceMapping:
    """Mapping from a source column to a canonical field."""

    source_column: str
    canonical_field: str


SINGLE_FILE_ROLE: Final[str] = "single_file"
CUSTOMERS_FILE_ROLE: Final[str] = "customers"
TRANSACTIONS_FILE_ROLE: Final[str] = "transactions"