"""Source-to-canonical column mapping utilities."""

from customerpulse.ingestion.models import SourceMapping


def get_mappings_from_config(config: dict) -> tuple[SourceMapping, ...]:
    """Build source-to-canonical mappings from configuration."""

    mapping_config = config["mapping"]

    return tuple(
        SourceMapping(
            source_column=source_column,
            canonical_field=canonical_field,
        )
        for canonical_field, source_column in mapping_config.items()
    )