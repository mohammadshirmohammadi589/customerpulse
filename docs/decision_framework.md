# CustomerPulse Decision Framework

## Purpose

The decision layer translates customer behavioral signals into transparent business priorities and recommended actions.

It does not produce predictive probabilities.

---

## Priority Rules

| Segment            | Priority | Reason                                             |
| ------------------ | -------- | -------------------------------------------------- |
| High Value At Risk | HIGH     | High historical value combined with weaker recency |
| Champions          | MEDIUM   | Highly recent, frequent, and high-value behavior   |
| Loyal Customers    | MEDIUM   | Frequent customers with strong recent activity     |
| Recent Customers   | MEDIUM   | Recent customers with limited purchase history     |
| Other              | LOW      | No strong immediate behavioral signal              |

---

## Recommendation Rules

### High Value At Risk

**Signal:** High historical value + weak recency.

**Interpretation:** Customer has generated substantial historical value but currently shows weaker recent activity.

**Recommended Action:** Win-back and retention outreach.

**Limitation:** The analysis does not establish that outreach will cause retention.

---

### Champions

**Signal:** Strong Recency, Frequency, and Monetary scores.

**Interpretation:** Customer demonstrates highly engaged historical behavior.

**Recommended Action:** Protect the relationship and consider loyalty treatment.

**Limitation:** High historical engagement does not guarantee future activity.

---

### Loyal Customers

**Signal:** High Frequency combined with relatively strong Recency.

**Interpretation:** Customer demonstrates repeated and relatively recent purchasing.

**Recommended Action:** Retention and relevant upsell opportunities.

**Limitation:** Upsell effectiveness requires experimentation.

---

### Recent Customers

**Signal:** Recent activity with limited historical frequency.

**Interpretation:** Customer has recently entered the customer base or has limited purchase history.

**Recommended Action:** Onboarding and second-purchase engagement.

**Limitation:** Limited history reduces confidence in long-term value interpretation.

---

### Other

**Signal:** No strong rule-based behavioral signal.

**Interpretation:** Customer does not currently match a specialized priority rule.

**Recommended Action:** Monitor customer behavior.

---

## Decision Philosophy

CustomerPulse separates:

**Analytical Layer**

Behavioral measurements and segmentation.

↓

**Decision Layer**

Business priority and recommended action.

This separation allows business rules to evolve without changing the underlying analytical metrics.

---

## Important Interpretation Rule

Priority is not churn probability.

A HIGH priority customer is not necessarily predicted to churn.

It means that the available behavioral signals justify higher business attention under the current rule framework.
