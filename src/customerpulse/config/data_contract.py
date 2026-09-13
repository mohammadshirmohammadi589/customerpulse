"""Canonical CustomerPulse analytical data contract."""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class CanonicalField:
    """Machine-readable definition of one canonical analytical field."""

    name: str
    logical_type: str
    required: bool
    description: str
    expectation: str


# Canonical field definitions.
CANONICAL_SCHEMA: Final[tuple[CanonicalField, ...]] = (
    CanonicalField(
        name="customer_id",
        logical_type="string",
        required=True,
        description=(
            "Stable identifier for the customer associated with the transaction."
        ),
        expectation=(
            "Should identify a customer and should not be unusable."
        ),
    ),
    CanonicalField(
        name="transaction_id",
        logical_type="string",
        required=True,
        description="Stable identifier for the transaction.",
        expectation=(
            "Should identify a transaction and should not be unusable."
        ),
    ),
    CanonicalField(
        name="transaction_date",
        logical_type="datetime",
        required=True,
        description="Date or timestamp associated with the transaction.",
        expectation=(
            "Should represent a usable transaction date or timestamp."
        ),
    ),
    CanonicalField(
        name="amount",
        logical_type="numeric",
        required=True,
        description=(
            "Transaction amount supplied by the source after its business "
            "meaning has been established."
        ),
        expectation=(
            "Should be interpretable as a numeric transaction amount."
        ),
    ),
    CanonicalField(
        name="status",
        logical_type="string",
        required=False,
        description=(
            "Transaction or order status supplied by the source, when available."
        ),
        expectation=(
            "May be missing when the source does not provide transaction status."
        ),
    ),
    CanonicalField(
        name="product_id",
        logical_type="string",
        required=False,
        description=(
            "Identifier of the product associated with the transaction, "
            "when available."
        ),
        expectation=(
            "May be missing when product-level identifiers are unavailable."
        ),
    ),
    CanonicalField(
        name="product_name",
        logical_type="string",
        required=False,
        description=(
            "Product name or description associated with the transaction, "
            "when available."
        ),
        expectation=(
            "May be missing when product names are unavailable."
        ),
    ),
    CanonicalField(
        name="category",
        logical_type="string",
        required=False,
        description=(
            "Product or transaction category supplied by the source, "
            "when available."
        ),
        expectation=(
            "May be missing when category information is unavailable."
        ),
    ),
    CanonicalField(
        name="currency",
        logical_type="string",
        required=False,
        description=(
            "Currency associated with the transaction amount, when available."
        ),
        expectation=(
            "May be missing when currency information is unavailable."
        ),
    ),
    CanonicalField(
        name="discount",
        logical_type="numeric",
        required=False,
        description=(
            "Discount value supplied by the source, when available."
        ),
        expectation=(
            "May be missing when discount information is unavailable."
        ),
    ),
    CanonicalField(
        name="tax",
        logical_type="numeric",
        required=False,
        description=(
            "Tax value supplied by the source, when available."
        ),
        expectation=(
            "May be missing when tax information is unavailable."
        ),
    ),
    CanonicalField(
        name="shipping",
        logical_type="numeric",
        required=False,
        description=(
            "Shipping value supplied by the source, when available."
        ),
        expectation=(
            "May be missing when shipping information is unavailable."
        ),
    ),
    CanonicalField(
        name="payment_status",
        logical_type="string",
        required=False,
        description=(
            "Payment status supplied by the source, when available."
        ),
        expectation=(
            "May be missing when payment status is unavailable."
        ),
    ),
)


# Derived field groups kept as simple reusable interfaces.
REQUIRED_FIELDS: Final[tuple[str, ...]] = tuple(
    field.name for field in CANONICAL_SCHEMA if field.required
)

OPTIONAL_FIELDS: Final[tuple[str, ...]] = tuple(
    field.name for field in CANONICAL_SCHEMA if not field.required
)

CANONICAL_FIELDS: Final[tuple[str, ...]] = tuple(
    field.name for field in CANONICAL_SCHEMA
)

CANONICAL_FIELD_TYPES: Final[dict[str, str]] = {
    field.name: field.logical_type
    for field in CANONICAL_SCHEMA
}

CANONICAL_FIELD_DESCRIPTIONS: Final[dict[str, str]] = {
    field.name: field.description
    for field in CANONICAL_SCHEMA
}

CANONICAL_FIELD_EXPECTATIONS: Final[dict[str, str]] = {
    field.name: field.expectation
    for field in CANONICAL_SCHEMA
}


# Canonical analytical grain.
CANONICAL_GRAIN: Final[str] = "transaction"


def get_required_fields() -> tuple[str, ...]:
    """Return required canonical fields."""
    return REQUIRED_FIELDS


def get_optional_fields() -> tuple[str, ...]:
    """Return optional canonical fields."""
    return OPTIONAL_FIELDS


def get_canonical_fields() -> tuple[str, ...]:
    """Return all canonical fields in canonical order."""
    return CANONICAL_FIELDS


def get_canonical_schema() -> tuple[CanonicalField, ...]:
    """Return the complete machine-readable canonical schema."""
    return CANONICAL_SCHEMA