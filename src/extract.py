"""Extract sales rows from CSV without silently discarding malformed values."""
from pathlib import Path
import pandas as pd


def extract_sales(csv_path: str | Path) -> pd.DataFrame:
    """Read all columns as strings so validation can inspect bad inputs."""
    return pd.read_csv(csv_path, dtype=str, keep_default_na=False)
