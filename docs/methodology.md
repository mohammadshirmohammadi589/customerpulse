# CustomerPulse Methodology

## 1. Data Source

CustomerPulse uses the UCI Online Retail dataset as its primary demonstration dataset.

The raw dataset contains retail invoice line items rather than already-aggregated transactions.

---

## 2. Canonical Analytical Grain

The canonical analytical grain is transaction-level.

The source dataset may contain multiple rows for the same invoice because each row can represent a product line.

Therefore raw row count is not treated as transaction count.

Qualified line items are aggregated by `transaction_id` before downstream customer analytics.

---

## 3. Transaction Qualification

A transaction is considered analytically qualifying when:

* customer ID is usable
* transaction ID is usable
* transaction date is valid
* amount is positive
* configured cancellation rules are satisfied

For the UCI dataset, invoice IDs beginning with `C` are excluded according to configuration.

---

## 4. Identifier Normalization

Customer identifiers are normalized before analytical processing.

For example, numeric-looking customer identifiers such as `12345.0` are normalized to their logical identifier representation rather than being treated as a different customer.

The goal is normalization without changing customer identity.

---

## 5. Data Quality

Data quality is separated into:

* ERROR
* WARNING
* INFORMATION

Raw validation provides a diagnostic view of source quality.

Row-level unusable records can be removed by the qualification layer.

Blocking validation is then applied to the qualified analytical dataset.

This prevents expected dirty source rows from blocking the entire analytical pipeline when sufficient usable data remains.

---

## 6. Customer Metrics

Customer-level metrics are calculated from the standardized transaction table.

Core metrics include:

* transaction count
* revenue
* first transaction date
* last transaction date
* average transaction value
* customer active days

---

## 7. RFM Analysis

RFM analysis summarizes customer behavior through:

* Recency
* Frequency
* Monetary value

Relative quintile scoring is used for the MVP.

This approach was selected because it is:

* transparent
* reproducible
* easy to explain
* easy to validate
* appropriate for an initial portfolio implementation

---

## 8. Cohort Retention

Customers are assigned to a monthly cohort based on their first qualifying purchase.

Customer activity is then measured by month.

Retention is calculated as:

`retained customers / cohort size`

The analysis measures customer retention based on observed purchase activity.

---

## 9. Historical Customer Value

Historical Customer Value represents observed realized revenue during the available historical period.

It is intentionally not treated as predictive CLV.

Predictive CLV is outside the MVP scope.

---

## 10. Segmentation

The MVP uses transparent RFM-based business rules instead of unsupervised clustering.

The primary segments are:

* Champions
* Loyal Customers
* High Value At Risk
* Recent Customers
* Other

The objective is interpretability rather than maximum algorithmic complexity.

---

## 11. Customer Priority

The decision layer converts behavioral segments into transparent priority tiers.

Priority rules are:

* High Value At Risk → HIGH
* Champions → MEDIUM
* Loyal Customers → MEDIUM
* Recent Customers → MEDIUM
* Other → LOW

These are business prioritization rules, not predictive probabilities.

---

## 12. Recommendations

Recommendations follow:

`Signal → Interpretation → Action → Rationale`

Recommendations are directional and behavioral.

They do not imply causal effectiveness.

For example, a High Value At Risk customer may receive a recommended win-back action, but the pipeline does not claim that the action will cause retention.

---

## 13. Limitations

The MVP does not include:

* predictive churn modeling
* predictive CLV
* next-purchase prediction
* causal inference
* advanced recommendation models
* market basket analysis
* real-time data
* multi-currency conversion without explicit configuration
* CRM integration

These areas are candidates for future versions.
