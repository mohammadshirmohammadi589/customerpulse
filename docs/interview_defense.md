# CustomerPulse Interview Defense

## 1. Business Problem

CustomerPulse analyzes customer purchasing behavior and translates observed behavior into transparent retention and customer-priority signals.

The goal is to help a business understand customer value, engagement, retention patterns, and which customers deserve attention.

---

## 2. Why DuckDB?

DuckDB was selected because the project is analytical rather than transactional.

It provides a lightweight SQL engine, supports analytical queries efficiently, and keeps the project reproducible without unnecessary infrastructure.

---

## 3. Why SQL?

SQL is used for the core analytical transformations because customer metrics, RFM, cohorts, retention, segmentation, and decision rules are naturally expressed as relational operations.

Keeping these transformations in SQL also makes the logic auditable and easy to inspect.

---

## 4. Why Python?

Python is primarily used for orchestration, ingestion, validation, standardization, configuration, testing, and dashboard integration.

The separation keeps analytical SQL distinct from application logic.

---

## 5. Why Transaction-Level Grain?

The source dataset is line-item based.

Multiple rows can belong to the same invoice, so counting source rows as transactions would overstate transaction counts.

CustomerPulse therefore aggregates qualified line items into a canonical transaction-level representation before downstream analytics.

---

## 6. How Are Invalid Transactions Handled?

Transactions are qualified using explicit rules.

Rows with missing customer IDs, missing transaction IDs, invalid dates, non-positive amounts, or configured cancellation prefixes are excluded from downstream customer analytics.

The raw validation layer still reports data-quality problems rather than silently hiding them.

---

## 7. Why RFM?

RFM provides an interpretable framework based on:

- Recency
- Frequency
- Monetary value

It is easy to explain to business stakeholders and provides a strong descriptive segmentation baseline.

---

## 8. Why NTILE?

NTILE provides relative scoring across the customer population.

Recency is scored in the opposite direction because lower recency is better, while frequency and monetary value receive higher scores for larger values.

The approach is simple, transparent, and reproducible.

---

## 9. Why Not Clustering?

Clustering could be explored later, but the MVP prioritizes interpretability and reproducibility.

Rule-based RFM segments allow business stakeholders to understand exactly why a customer belongs to a segment.

---

## 10. What Does Retention Mean?

Retention represents the percentage of customers from a cohort who remain active in later observed periods.

The CustomerPulse retention analysis uses distinct customer activity by month.

It is customer retention, not transaction retention.

---

## 11. Why Are Future Cohort Cells NULL?

A NULL future cohort cell means that the period has not yet been observed for that cohort.

It should not be interpreted as zero retention.

Zero would mean the period was observed and no customers were retained.

---

## 12. Is Historical Customer Value Predictive CLV?

No.

Historical Customer Value represents observed realized revenue from qualifying historical transactions.

It does not predict future customer value.

Predictive CLV is outside the MVP scope.

---

## 13. Is HIGH Priority a Churn Probability?

No.

HIGH is a transparent business-priority tier.

In the current framework it primarily identifies High Value At Risk customers.

It is not a probability and should not be interpreted as a churn score.

---

## 14. Why Separate Analytics and Decision Layers?

The analytical layer produces behavioral signals.

The decision layer translates those signals into business priorities and recommended actions.

This separation allows business rules to evolve without changing the underlying analytical metrics.

---

## 15. Are Recommendations Causal?

No.

Recommendations are hypothesis-driven actions based on observed behavioral signals.

The project does not claim that an action will cause a particular business outcome.

Those claims would require controlled experiments or other causal methods.

---

## 16. How Is the Pipeline Tested?

The project contains unit tests, integration tests, regression tests, and business validation.

The pipeline also validates important invariants such as:

- unique transaction IDs at transaction grain
- no null customer IDs in standardized transactions
- positive transaction amounts
- valid RFM metrics
- valid priority values
- valid HIGH-priority rules

---

## 17. Why No Machine Learning?

The MVP first establishes a reliable analytical foundation.

Predictive modeling would require additional decisions around target definition, observation windows, temporal feature construction, leakage prevention, train/validation/test splitting, and model evaluation.

These are intentionally deferred to V2.

---

## 18. How Would Churn Prediction Be Built in V2?

A future churn model would require:

1. A formal churn definition.
2. A prediction horizon.
3. Historical observation windows.
4. Point-in-time feature construction.
5. Temporal train/validation/test splits.
6. Leakage prevention.
7. Model evaluation.
8. Threshold selection.
9. Business validation.

---

## 19. Main Limitation

The analysis is based on observed historical behavior.

It does not establish causality and does not predict future customer behavior.

Results also depend on the quality and business meaning of the source transaction data.

---

## 20. Main Design Principle

CustomerPulse prioritizes:

- correctness
- transparency
- reproducibility
- explainability
- business usefulness

over unnecessary technical complexity.