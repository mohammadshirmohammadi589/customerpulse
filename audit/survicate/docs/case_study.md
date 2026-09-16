# Survicate — Customer Health & Retention Analytics

## Business Problem

Customer Success teams need a transparent way to identify
customers whose engagement is declining while considering
customer value and feedback signals.

## Proposed Analytics Approach

Customer Data
→ Engagement Change
→ Feedback Signals
→ Historical Customer Value
→ Customer Health
→ Priority
→ Recommended Action

## Signals

- Month-over-month engagement change
- Survey activity
- Response volume
- NPS
- Historical customer value

## Decision Layer

Customers are assigned HIGH, MEDIUM, or LOW priority.

The prioritization is rule-based and explainable.

## Synthetic Result

20 synthetic customers were analyzed.

7 customers generated a HIGH risk signal.
13 customers were classified as LOW priority.

## Business Use

The framework provides an operational signal for Customer Success
teams to decide which customers may deserve review.

It is not a churn prediction model.

## Limitations

This proof of concept uses synthetic data.

It does not use or claim access to Survicate internal data.

With real historical data, the next step would be validating these
signals against retention, expansion, downgrade, and churn outcomes.
