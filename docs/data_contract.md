# CustomerPulse Data Contract

## 1. Purpose

The CustomerPulse Data Contract defines the canonical analytical representation
used by the CustomerPulse pipeline.

The contract creates a stable interface between source datasets and downstream
analytics.

Source datasets may use different column names, structures, or optional fields.
They must be mapped into the canonical model before downstream analytical
processing.

The canonical analytical model is designed to support customer intelligence,
transaction analysis, RFM analysis, cohort analysis, retention analysis,
historical customer value, segmentation, customer prioritization, and
explainable recommendations.

---

## 2. Canonical Analytical Grain

The canonical analytical grain is:

**One row represents one transaction.**

The transaction-level grain is the foundation for downstream customer-level
aggregation and analytical metrics.

Customer-level metrics must be derived from the canonical transaction-level
representation rather than being treated as the primary source grain.

---

## 3. Required Fields

The following fields are required in the canonical model.

| Field | Logical Type | Required | Business Meaning | Basic Expectation |
|---|---|---:|---|---|
| `customer_id` | string | Yes | Stable identifier for the customer associated with the transaction. | Should identify a customer and should not be unusable. |
| `transaction_id` | string | Yes | Stable identifier for the transaction. | Should identify a transaction and should not be unusable. |
| `transaction_date` | datetime | Yes | Date or timestamp associated with the transaction. | Should represent a usable transaction date or timestamp. |
| `amount` | numeric | Yes | Transaction amount supplied by the source after its business meaning has been established. | Should be interpretable as a numeric transaction amount. |

---

## 4. Optional Fields

The following fields are optional in the canonical model.

| Field | Logical Type | Required | Business Meaning | Basic Expectation |
|---|---|---:|---|---|
| `status` | string | No | Transaction or order status supplied by the source, when available. | May be missing when the source does not provide transaction status. |
| `product_id` | string | No | Identifier of the product associated with the transaction, when available. | May be missing when product-level identifiers are unavailable. |
| `product_name` | string | No | Product name or description associated with the transaction, when available. | May be missing when product names are unavailable. |
| `category` | string | No | Product or transaction category supplied by the source, when available. | May be missing when category information is unavailable. |
| `currency` | string | No | Currency associated with the transaction amount, when available. | May be missing when currency information is unavailable. |
| `discount` | numeric | No | Discount value supplied by the source, when available. | May be missing when discount information is unavailable. |
| `tax` | numeric | No | Tax value supplied by the source, when available. | May be missing when tax information is unavailable. |
| `shipping` | numeric | No | Shipping value supplied by the source, when available. | May be missing when shipping information is unavailable. |
| `payment_status` | string | No | Payment status supplied by the source, when available. | May be missing when payment status is unavailable. |

---

## 5. Complete Canonical Field List

The canonical field order is:

1. `customer_id`
2. `transaction_id`
3. `transaction_date`
4. `amount`
5. `status`
6. `product_id`
7. `product_name`
8. `category`
9. `currency`
10. `discount`
11. `tax`
12. `shipping`
13. `payment_status`

The canonical model therefore contains:

- 4 required fields
- 9 optional fields
- 13 total canonical fields

---

## 6. Source-to-Canonical Mapping

CustomerPulse supports multiple source formats by mapping source-specific
columns into the canonical analytical model.

For example, a source dataset may contain:

| Source Field | Canonical Field |
|---|---|
| `client_id` | `customer_id` |
| `order_number` | `transaction_id` |
| `order_date` | `transaction_date` |
| `net_amount` | `amount` |

Another dataset may use:

| Source Field | Canonical Field |
|---|---|
| `customer_number` | `customer_id` |
| `invoice_id` | `transaction_id` |
| `purchase_timestamp` | `transaction_date` |
| `total_value` | `amount` |

These mappings are examples only. Actual source mappings must be established
from the semantics and structure of the input dataset.

Downstream analytical logic must operate on canonical field names rather than
source-specific field names.

---

## 7. Field Semantics

### `customer_id`

Identifies the customer associated with the transaction.

The identifier should be stable enough to support customer-level aggregation
across transactions.

An unusable customer identifier prevents reliable customer-level analysis.

### `transaction_id`

Identifies the transaction.

The identifier should support transaction-level counting and duplicate
detection.

### `transaction_date`

Represents the date or timestamp associated with the transaction.

It is required for time-based analysis such as:

- recency
- cohort assignment
- retention
- activity windows
- historical analysis periods

### `amount`

Represents the transaction amount supplied by the source after its business
meaning has been established.

CustomerPulse does not assume a universal revenue formula at the contract
level.

Fields such as `discount`, `tax`, and `shipping` are preserved separately
when available so that their treatment can be defined according to source
semantics and business rules.

---

## 8. Business Semantics and Revenue

The Data Contract defines the meaning and structure of `amount`, but it does
not by itself define every revenue business rule.

Revenue treatment may depend on source-specific information such as:

- transaction status
- refunds
- cancellations
- discounts
- taxes
- shipping
- currency
- payment status

These rules must be established during later analytical processing based on
the available source data and documented assumptions.

CustomerPulse must not silently invent financial semantics that are not
supported by the source data.

---

## 9. Required vs Optional Fields

Required fields are necessary for the core transaction-level analytical model.

The required fields are:

- `customer_id`
- `transaction_id`
- `transaction_date`
- `amount`

Optional fields provide additional analytical context but are not universally
available across all source datasets.

Missing optional fields should not automatically make a dataset unusable.

However, the absence of optional fields may limit specific analyses or business
interpretations.

---

## 10. Assumptions

The canonical model assumes that:

1. Each canonical row represents one transaction.
2. `customer_id` can be used to associate transactions with customers.
3. `transaction_id` can be used to identify transactions.
4. `transaction_date` can be interpreted as a valid date or timestamp.
5. `amount` can be interpreted as a numeric transaction amount.
6. Source-specific column names may differ from canonical field names.
7. Source-specific mappings must be established before downstream analytics.
8. Optional fields may be absent.
9. Financial semantics must be based on available source information.
10. Canonical field names provide the stable interface for downstream analytics.

---

## 11. Limitations

The Data Contract does not guarantee that source data is valid.

It defines the expected analytical structure and field semantics.

Actual data quality problems such as:

- missing required values
- invalid dates
- invalid amounts
- duplicate transactions
- unusable identifiers
- inconsistent status values
- currency inconsistencies
- suspicious records

must be detected by the later data validation layer.

The contract also does not define predictive customer behavior.

In particular, the contract does not imply:

- churn prediction
- predictive customer lifetime value
- next-purchase prediction
- recommendation models

These are outside the scope of the canonical data contract and, where
applicable, outside the MVP scope.

---

## 12. Contract Boundary

The Data Contract defines:

- canonical field names
- logical data types
- required vs optional fields
- business meanings
- basic expectations
- analytical grain
- source-to-canonical interface
- assumptions
- limitations

The Data Contract does not implement:

- CSV ingestion
- dataset validation
- data cleaning
- standardization transformations
- database loading
- SQL analytics
- RFM calculation
- cohort calculation
- retention calculation
- customer prioritization
- recommendations
- dashboard logic

These responsibilities belong to later components of the CustomerPulse
architecture.

---

## 13. Design Principle

The canonical data contract acts as a stable interface between heterogeneous
source datasets and downstream analytics.

This separation allows the analytical logic to remain reusable when a new
dataset is introduced.

Ideally, adding a new compatible dataset should require changes to source
mapping and configuration rather than rewriting the core analytical logic.