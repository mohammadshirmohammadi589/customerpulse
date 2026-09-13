import sys


sys.path.insert(0, "src")

from customerpulse.config.data_contract import (
    CANONICAL_FIELD_DESCRIPTIONS,
    CANONICAL_FIELD_EXPECTATIONS,
    CANONICAL_FIELD_TYPES,
    CANONICAL_FIELDS,
    CANONICAL_GRAIN,
    CANONICAL_SCHEMA,
    OPTIONAL_FIELDS,
    REQUIRED_FIELDS,
)


def test_canonical_field_count():
    """The canonical model must contain exactly 13 fields."""
    assert len(CANONICAL_SCHEMA) == 13


def test_required_fields():
    """The canonical model must contain exactly four required fields."""
    assert REQUIRED_FIELDS == (
        "customer_id",
        "transaction_id",
        "transaction_date",
        "amount",
    )


def test_optional_fields():
    """The canonical model must contain exactly nine optional fields."""
    assert len(OPTIONAL_FIELDS) == 9


def test_required_optional_separation():
    """Required and optional fields must not overlap."""
    assert not set(REQUIRED_FIELDS) & set(OPTIONAL_FIELDS)


def test_canonical_field_names_are_consistent():
    """Schema field names must match the canonical field list."""
    schema_fields = tuple(field.name for field in CANONICAL_SCHEMA)

    assert schema_fields == CANONICAL_FIELDS


def test_all_fields_have_types():
    """Every canonical field must have a logical type."""
    assert set(CANONICAL_FIELDS) == set(CANONICAL_FIELD_TYPES)

    for field in CANONICAL_SCHEMA:
        assert field.logical_type


def test_all_fields_have_documentation():
    """Every canonical field must have description and expectation metadata."""
    assert set(CANONICAL_FIELDS) == set(CANONICAL_FIELD_DESCRIPTIONS)
    assert set(CANONICAL_FIELDS) == set(CANONICAL_FIELD_EXPECTATIONS)

    for field in CANONICAL_SCHEMA:
        assert field.description
        assert field.expectation


def test_canonical_grain():
    """The canonical analytical grain must remain transaction-level."""
    assert CANONICAL_GRAIN == "transaction"