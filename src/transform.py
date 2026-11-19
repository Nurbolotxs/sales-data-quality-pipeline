"""Calculate the total for each validated sale."""
import pandas as pd


def transform_sales(valid: pd.DataFrame) -> pd.DataFrame:
    result = valid.copy()
    result["total"] = (result["quantity"] * result["price"]).round(2)
    return result
