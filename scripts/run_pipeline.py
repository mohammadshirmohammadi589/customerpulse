import sys

sys.path.insert(0, "src")

from customerpulse.pipeline import run_pipeline


if __name__ == "__main__":
    connection = run_pipeline(
        "configs/default.yaml"
    )

    print(
        connection.execute("""
            SELECT
                COUNT(*) AS customers
            FROM customer_metrics
        """).fetchdf()
    )

    print(
        connection.execute("""
            SELECT
                COUNT(*) AS customers
            FROM customer_recommendations
        """).fetchdf()
    )

    connection.close()