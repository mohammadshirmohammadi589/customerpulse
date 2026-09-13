# CustomerPulse

Customer Intelligence & Retention Analytics

CustomerPulse is an end-to-end analytics project designed to transform raw retail transaction data into customer-level behavioral insights, retention analytics, business priorities, and explainable recommendations.

## Project Objective

The project answers questions such as:

* How many customers and transactions do we have?
* Which customers generate the most historical value?
* Which customers are highly engaged?
* Which valuable customers show weaker recent activity?
* How does customer retention evolve by acquisition cohort?
* Which customers should receive higher business attention?
* What action can be recommended based on observed customer behavior?

## Architecture

```text
Input
  ↓
Data Contract
  ↓
Ingestion
  ↓
Qualification
  ↓
Data Quality
  ↓
Standardization
  ↓
DuckDB Staging
  ↓
SQL Analytics
  ↓
RFM / Cohort / Retention
  ↓
Historical Customer Value
  ↓
Segmentation
  ↓
Decision Layer
  ↓
Streamlit Dashboard
```

## Key Design Decisions

### Transaction-Level Analytical Grain

The source dataset contains retail line items.

CustomerPulse standardizes qualified line items into transaction-level records before calculating transaction and customer metrics.

### Qualification Before Analytical Validation

Raw data quality issues are reported first.

Row-level unusable records are excluded through an explicit qualification layer.

Blocking validation is then applied to the qualified analytical dataset.

### Explainable Segmentation

The MVP uses transparent RFM-based business rules instead of clustering.

This prioritizes interpretability and reproducibility.

### Historical Customer Value

Customer value represents observed historical realized revenue.

It is not predictive CLV.

### Decision Layer

Behavioral analytics and business decisions are separated.

The analytical layer produces signals.

The decision layer translates those signals into transparent priorities and recommended actions.

## Main Analytics

* Customer Metrics
* RFM Analysis
* RFM Scoring
* Customer Segmentation
* Cohort Analysis
* Retention Analysis
* Historical Customer Value
* Customer Priority
* Explainable Recommendations

## Data Quality

The pipeline evaluates:

* missing required fields
* invalid dates
* invalid amounts
* unusable identifiers
* duplicate records
* relationship issues
* currency availability
* optional field completeness

## Dashboard

The Streamlit dashboard provides:

* customer KPIs
* transaction KPIs
* revenue
* customer segments
* customer priorities
* recommendation reasons
* cohort retention
* downloadable priority table

## Run the Project

### Install Dependencies

```powershell
pip install -r requirements.txt
```

### Run Tests

```powershell
pytest -q
```

### Run the Analytical Pipeline

```powershell
python scripts/run_pipeline.py
```

### Export Customer Priority Table

```powershell
python scripts/export_customer_priority.py
```

### Run Dashboard

```powershell
streamlit run dashboard/app.py
```

## Project Structure

```text
customerpulse/
├── data/
├── notebooks/
├── src/
├── sql/
├── dashboard/
├── tests/
├── configs/
├── docs/
├── scripts/
├── README.md
└── requirements.txt
```

## Scope

### Included in MVP

* data contract
* ingestion
* schema mapping
* data quality validation
* standardization
* DuckDB
* SQL analytics
* customer metrics
* RFM
* cohort retention
* historical customer value
* segmentation
* customer priority
* explainable recommendations
* Streamlit dashboard
* automated tests
* documentation

### Explicitly Out of Scope

* predictive churn modeling
* predictive CLV
* next-purchase prediction
* advanced recommendation models
* market basket analysis
* real-time streaming
* CRM integration
* cloud deployment
* authentication
* Kubernetes
* LLM functionality

## Future Version

A future version can add:

* formal churn definition
* temporal feature engineering
* train/validation/test splitting
* leakage prevention
* churn prediction
* predictive CLV
* model evaluation
* threshold optimization
* PostgreSQL
* advanced decision optimization

## Dataset

The demonstration dataset is the UCI Online Retail dataset.

The project intentionally treats the dataset as a realistic imperfect source rather than assuming that the input is already analytics-ready.

## Analytical Disclaimer

CustomerPulse provides behavioral analytics and transparent rule-based recommendations.

It does not claim causal effects from recommended actions.

High priority does not mean predicted churn probability.

Historical Customer Value does not mean predictive Customer Lifetime Value.
