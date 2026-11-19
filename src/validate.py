"""Split input into valid sales and rejected rows with reasons."""
import pandas as pd

REQUIRED_COLUMNS = ("order_id", "product", "quantity", "price")


def validate_sales(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required CSV columns: {', '.join(sorted(missing))}")

    valid_rows = []
    rejected_rows = []
    seen_ids = set()

    for _, row in df.iterrows():
        raw = {column: str(row[column]).strip() for column in REQUIRED_COLUMNS}
        problems = []
        order_id = raw["order_id"]
        if not order_id:
            problems.append("missing order_id")
        elif order_id in seen_ids:
            problems.append("duplicate order_id")
        else:
            seen_ids.add(order_id)

        if not raw["product"]:
            problems.append("missing product")

        try:
            quantity = int(raw["quantity"])
            if quantity <= 0:
                problems.append("quantity must be positive")
        except ValueError:
            quantity = None
            problems.append("quantity must be an integer")

        try:
            price = float(raw["price"])
            if not pd.notna(price) or price <= 0 or price == float("inf"):
                problems.append("price must be finite and positive")
        except ValueError:
            price = None
            problems.append("price must be a number")

        if problems:
            rejected_rows.append({**raw, "error": "; ".join(problems)})
        else:
            valid_rows.append({"order_id": order_id, "product": raw["product"],
                               "quantity": quantity, "price": round(price, 2)})

    return (pd.DataFrame(valid_rows, columns=REQUIRED_COLUMNS),
            pd.DataFrame(rejected_rows, columns=[*REQUIRED_COLUMNS, "error"]))
