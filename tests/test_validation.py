import pandas as pd
import pytest
from src.validate import validate_sales


def test_valid_row():
    df = pd.DataFrame([{"order_id":"1", "product":"Mouse", "quantity":"2", "price":"10"}])
    valid, rejected = validate_sales(df)
    assert len(valid) == 1
    assert rejected.empty


def test_duplicate_id_is_rejected():
    df = pd.DataFrame([{"order_id":"1", "product":"Mouse", "quantity":"2", "price":"10"}] * 2)
    valid, rejected = validate_sales(df)
    assert len(valid) == 1
    assert len(rejected) == 1
    assert "duplicate" in rejected.iloc[0]["error"]


def test_negative_quantity_is_rejected():
    df = pd.DataFrame([{"order_id":"1", "product":"Mouse", "quantity":"-2", "price":"10"}])
    valid, rejected = validate_sales(df)
    assert valid.empty
    assert "positive" in rejected.iloc[0]["error"]


def test_missing_price_is_rejected():
    df = pd.DataFrame([{"order_id":"1", "product":"Mouse", "quantity":"2", "price":""}])
    _, rejected = validate_sales(df)
    assert len(rejected) == 1


def test_missing_columns_raise_error():
    with pytest.raises(ValueError, match="Missing required"):
        validate_sales(pd.DataFrame({"order_id": ["1"]}))


def test_non_numeric_price_is_rejected():
    df = pd.DataFrame([{"order_id":"1", "product":"Mouse", "quantity":"2", "price":"oops"}])
    _, rejected = validate_sales(df)
    assert "number" in rejected.iloc[0]["error"]
