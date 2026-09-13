import matplotlib.pyplot as plt
import pandas as pd


def plot_segment_distribution(segments: pd.DataFrame):
    fig, ax = plt.subplots()

    data = segments.sort_values(
        "customer_count",
        ascending=True,
    )

    ax.barh(
        data["segment"],
        data["customer_count"],
    )

    ax.set_title("Customer Segment Distribution")
    ax.set_xlabel("Customers")
    ax.set_ylabel("Segment")

    fig.tight_layout()

    return fig


def plot_retention_heatmap(retention: pd.DataFrame):
    data = retention.copy()

    data = data.set_index("cohort_month")

    period_columns = [
        column
        for column in data.columns
        if column.startswith("month_")
    ]

    matrix = data[period_columns]

    fig, ax = plt.subplots(
        figsize=(12, 6),
    )

    image = ax.imshow(
        matrix,
        aspect="auto",
    )

    ax.set_title("Cohort Retention")
    ax.set_xlabel("Period")
    ax.set_ylabel("Cohort Month")

    ax.set_xticks(
        range(len(period_columns))
    )

    ax.set_xticklabels(
        period_columns,
        rotation=45,
        ha="right",
    )

    ax.set_yticks(
        range(len(matrix.index))
    )

    ax.set_yticklabels(
        [
            str(value)[:7]
            for value in matrix.index
        ]
    )

    fig.colorbar(
        image,
        ax=ax,
        label="Retention Rate",
    )

    fig.tight_layout()

    return fig