# CustomerPulse Case Study

## Business Problem

Businesses need to understand which customers are valuable, engaged, becoming inactive, and deserving of retention attention.

CustomerPulse provides an analytical pipeline that transforms transaction data into customer metrics, RFM segments, cohort retention analysis, historical customer value, transparent customer priorities, and recommended actions.

## Dataset

The project uses the UCI Online Retail dataset.

The raw dataset contains line-item transaction records.

## Analytical Architecture

The pipeline follows:

Input
→ Data Contract
→ Data Quality
→ Standardization
→ Transaction-Level Model
→ DuckDB
→ SQL Analytics
→ RFM
→ Cohort Retention
→ Historical Customer Value
→ Segmentation
→ Customer Priority
→ Recommendations
→ Dashboard

## Data Quality

The raw data contains missing customer identifiers, cancellation transactions, non-positive quantities or prices, and other quality issues.

CustomerPulse explicitly validates these conditions and qualifies usable transactions before downstream customer analytics.

## Customer Metrics

The analytical layer calculates:

- customer count
- transaction count
- revenue
- first transaction date
- last transaction date
- average transaction value
- customer active days

## RFM Analysis

Customers are evaluated using:

- Recency
- Frequency
- Monetary value

Relative quintile scores are used to create interpretable behavioral signals.

## Cohort Retention

Customers are assigned to a monthly cohort based on their first qualifying transaction.

Monthly customer activity is then used to calculate cohort retention.

## Historical Customer Value

Historical Customer Value is calculated from observed qualifying revenue.

It is explicitly not predictive CLV.

## Segmentation

Customer segments are created using transparent RFM rules.

The MVP includes:

- Champions
- Loyal Customers
- High Value At Risk
- Recent Customers
- Other

## Customer Priority

Customer behavior is translated into three business attention tiers:

- HIGH
- MEDIUM
- LOW

HIGH priority currently identifies High Value At Risk customers.

## Recommendations

Each customer receives an explainable recommendation based on the behavioral segment.

Recommendations are hypotheses rather than causal predictions.

## Dashboard

The Streamlit dashboard provides:

- KPI summary
- Data Health
- customer segment distribution
- customer priority filters
- priority customer table
- downloadable priority table
- cohort retention visualization

## Key Findings

The current dataset contains:

- 4,338 customers
- 18,532 qualifying transactions
- approximately $8.91M historical revenue

Customer behavior is heterogeneous, with different combinations of recency, frequency, and monetary value producing distinct behavioral segments.

## Limitations

The project is descriptive and diagnostic rather than predictive.

Historical behavior does not guarantee future behavior.

No causal claims are made from the segmentation or recommendations.

## Future Work

Potential V2 work includes:

- formal churn definition
- predictive churn modeling
- temporal feature engineering
- leakage prevention
- predictive CLV
- advanced segmentation
- PostgreSQL deployment