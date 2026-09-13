"""Basic inspection utilities for source CSV files."""

from pathlib import Path

import pandas as pd


FILE_PATH = Path("data/raw/OnlineRetail.csv")


def inspect_csv(path: Path) -> None:
    """Print basic structural information about a CSV file."""

    df = pd.read_csv(path, encoding="latin1")

    print("Shape:", df.shape)
    print("\nColumns:")
    for column in df.columns:
        print(f"- {column}")

    print("\nData types:")
    print(df.dtypes)

    print("\nFirst 5 rows:")
    print(df.head())


if __name__ == "__main__":
    inspect_csv(FILE_PATH)