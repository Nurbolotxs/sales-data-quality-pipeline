import pandas as pd
from src.transform import transform_sales


def test_total_calculation():
    df = pd.DataFrame([{"order_id":"1", "product":"Mouse", "quantity":3, "price":19.99}])
    result = transform_sales(df)
    assert result.iloc[0]["total"] == 59.97


def test_transform_does_not_modify_input():
    df = pd.DataFrame([{"order_id":"1", "product":"Mouse", "quantity":3, "price":20.0}])
    transform_sales(df)
    assert "total" not in df.columns
