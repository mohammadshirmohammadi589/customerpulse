# CustomerPulse — Customer Intelligence & Retention Analytics

## Executive Summary

CustomerPulse is an end-to-end customer analytics project that transforms transactional data into validated customer-level behavioral insights and explainable business priorities.

The pipeline covers:

- data ingestion
- data contract validation
- data quality checks
- transaction qualification
- standardization
- DuckDB analytical modeling
- customer metrics
- RFM analysis
- cohort retention
- historical customer value
- customer segmentation
- customer prioritization
- explainable recommendations
- Streamlit dashboard delivery

The project intentionally focuses on descriptive and diagnostic analytics rather than predictive churn or predictive CLV.

---

## Business Problem

Transactional systems often contain large amounts of customer purchase data but do not directly answer business questions such as:

- Which customers are most valuable?
- Which customers show weaker recent activity?
- How well are customer cohorts retained?
- Which customers deserve immediate attention?
- What type of action could be considered for different customer segments?

CustomerPulse addresses these questions through a reproducible analytical pipeline.

---

## Dataset

The project uses the UCI Online Retail dataset.

The raw dataset is line-item transactional data.

Important source-quality characteristics include:

- missing customer identifiers
- cancelled transactions
- non-positive quantities or prices
- duplicate line-level transaction records
- unavailable currency information

These issues are explicitly handled through validation and qualification rather than silently ignored.

---

## Analytical Architecture

```text
Raw CSV
   ↓
Data Contract
   ↓
Data Quality Validation
   ↓
Transaction Qualification
   ↓
Identifier Normalization
   ↓
Transaction-Level Standardization
   ↓
DuckDB Staging
   ↓
Customer Metrics
   ↓
RFM
   ↓
Cohort & Retention
   ↓
Historical Customer Value
   ↓
Segmentation
   ↓
Customer Priority
   ↓
Recommendations
   ↓
Streamlit Dashboard