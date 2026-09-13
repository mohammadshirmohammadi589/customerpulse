# CustomerPulse Architecture

## High-Level Architecture

```text
                    ┌─────────────────────┐
                    │      Input Data     │
                    │                     │
                    │ Single CSV          │
                    │ Two CSVs             │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Data Contract     │
                    │ Canonical Fields    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Ingestion       │
                    │ Load + Mapping      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Qualification &     │
                    │ Data Quality        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Standardization     │
                    │ Transaction Grain   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       DuckDB        │
                    │ Staging Layer       │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌──────────────────────────────────┐
              │          Analytical Layer        │
              │                                  │
              │ Customer Metrics                 │
              │ RFM                              │
              │ Cohort                           │
              │ Retention                        │
              │ Historical Customer Value        │
              │ Segmentation                     │
              └───────────────┬──────────────────┘
                              │
                              ▼
              ┌──────────────────────────────────┐
              │          Decision Layer          │
              │                                  │
              │ Priority                         │
              │ Reasons                          │
              │ Recommendations                  │
              └───────────────┬──────────────────┘
                              │
                              ▼
              ┌──────────────────────────────────┐
              │         Streamlit Dashboard      │
              │                                  │
              │ KPIs                             │
              │ Segments                         │
              │ Priority Customers               │
              │ Retention                        │
              │ Downloadable Output              │
              └──────────────────────────────────┘
```

## Design Principles

### 1. Source Independence

Different source formats map into the same canonical analytical model.

### 2. Separation of Concerns

Ingestion, validation, standardization, analytics, and decisioning are separate layers.

### 3. SQL for Analytical Transformations

DuckDB and SQL are used for customer metrics, RFM, cohort, retention, segmentation, and decision outputs.

### 4. Python for Orchestration

Python coordinates configuration, ingestion, validation, standardization, database execution, and pipeline control.

### 5. Explainability

Business-facing outputs use transparent rules.

### 6. Testability

Core modules and end-to-end pipeline behavior are validated through automated tests.

### 7. Reproducibility

Configuration, SQL, Python modules, tests, and documentation are stored in the repository.

---

## Technology Stack

* Python
* Pandas
* DuckDB
* SQL
* PyYAML
* pytest
* Streamlit
* Jupyter

---

## Why DuckDB?

DuckDB provides a lightweight analytical SQL engine that can operate directly on local analytical workflows without requiring a separate database server.

This makes it appropriate for a reproducible portfolio project while still allowing substantive SQL transformations.
