"""Save clean rows into SQLite."""
import sqlite3
from pathlib import Path
import pandas as pd


def load_sales(clean: pd.DataFrame, db_path: str | Path) -> None:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as connection:
        connection.execute("""CREATE TABLE IF NOT EXISTS sales (
            order_id TEXT PRIMARY KEY,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            price REAL NOT NULL CHECK(price > 0),
            total REAL NOT NULL CHECK(total > 0)
        )""")
        # Replace the dataset atomically on each run, avoiding stale rows.
        connection.execute("DELETE FROM sales")
        connection.executemany(
            "INSERT INTO sales (order_id, product, quantity, price, total) VALUES (?, ?, ?, ?, ?)",
            [(str(r.order_id), str(r.product), int(r.quantity), float(r.price), float(r.total))
             for r in clean.itertuples(index=False)],
        )
