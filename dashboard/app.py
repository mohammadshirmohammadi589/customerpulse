import sys

sys.path.insert(0, "src")

import streamlit as st

from charts import (
    plot_retention_heatmap,
    plot_segment_distribution,
)

from data_access import (
    get_customer_segments,
    get_data_health,
    get_kpis,
    get_priority_customers,
    get_retention_matrix,
)


st.set_page_config(
    page_title="CustomerPulse",
    layout="wide",
)


st.title("CustomerPulse")

st.caption(
    "Customer Intelligence & Retention Analytics"
)

st.info(
    "Priority tiers are transparent behavioral rules, "
    "not predictive churn scores."
)

st.caption(
    "Historical Customer Value represents observed "
    "realized revenue, not predictive CLV."
)


# --------------------------------------------------
# KPI Section
# --------------------------------------------------

kpis = get_kpis()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Customers",
    f"{int(kpis.iloc[0]['customer_count']):,}",
)

col2.metric(
    "Transactions",
    f"{int(kpis.iloc[0]['transaction_count']):,}",
)

revenue = float(
    kpis.iloc[0]["total_revenue"]
)

revenue_display = (
    f"${revenue / 1_000_000:.2f}M"
)

col3.metric(
    "Revenue",
    revenue_display,
)

col4.metric(
    "Avg. Customer Revenue",
    f"{kpis.iloc[0]['average_customer_revenue']:,.2f}",
)


# --------------------------------------------------
# Data Health
# --------------------------------------------------

st.header("Data Health")

st.caption(
    "Data quality checks applied to the standardized transaction layer."
)

health = get_data_health()

st.dataframe(
    health,
    use_container_width=True,
)


# --------------------------------------------------
# Customer Segments
# --------------------------------------------------

st.header("Customer Segments")

st.caption(
    "Segments are rule-based behavioral groups derived from RFM signals."
)

segments = get_customer_segments()

segment_chart = plot_segment_distribution(
    segments
)

st.pyplot(
    segment_chart,
    use_container_width=True,
)

st.dataframe(
    segments,
    use_container_width=True,
)


# --------------------------------------------------
# Customer Priority
# --------------------------------------------------

st.header("Customer Priority")

st.caption(
    "Priority translates observed customer behavior into transparent "
    "business attention tiers."
)

priority = get_priority_customers()

priority_filter = st.selectbox(
    "Priority",
    ["ALL", "HIGH", "MEDIUM", "LOW"],
)

segment_options = [
    "ALL",
    *sorted(priority["segment"].dropna().unique()),
]

segment_filter = st.selectbox(
    "Segment",
    segment_options,
)

filtered_priority = priority.copy()

if priority_filter != "ALL":
    filtered_priority = filtered_priority[
        filtered_priority["priority"] == priority_filter
    ]

if segment_filter != "ALL":
    filtered_priority = filtered_priority[
        filtered_priority["segment"] == segment_filter
    ]

priority_counts = (
    filtered_priority["priority"]
    .value_counts()
    .reindex(
        ["HIGH", "MEDIUM", "LOW"],
        fill_value=0,
    )
)

st.bar_chart(
    priority_counts,
    use_container_width=True,
)

st.dataframe(
    filtered_priority,
    use_container_width=True,
)

st.download_button(
    label="Download Priority Table",
    data=filtered_priority.to_csv(index=False),
    file_name="customer_priority.csv",
    mime="text/csv",
)


# --------------------------------------------------
# Cohort Retention
# --------------------------------------------------

st.header("Cohort Retention")

st.caption(
    "Retention shows the percentage of customers from each acquisition "
    "cohort who remained active in later observed months."
)

retention = get_retention_matrix()

retention_chart = plot_retention_heatmap(
    retention
)

st.pyplot(
    retention_chart,
    use_container_width=True,
)

st.dataframe(
    retention,
    use_container_width=True,
)