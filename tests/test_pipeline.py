import json
import sqlite3
from pathlib import Path
from src.main import run, ROOT


def test_full_pipeline(tmp_path: Path):
    report = run(ROOT / "data" / "sales.csv", tmp_path)
    assert report["total_rows"] == 10
    assert report["valid_rows"] == 6
    assert report["rejected_rows"] == 4
    assert report["total_revenue"] == 1386.0
    assert json.loads((tmp_path / "quality_report.json").read_text())["valid_rows"] == 6
    with sqlite3.connect(tmp_path / "sales.db") as conn:
        assert conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0] == 6
        assert conn.execute("SELECT ROUND(SUM(total),2) FROM sales").fetchone()[0] == 1386.0
    # Re-running must not duplicate records.
    run(ROOT / "data" / "sales.csv", tmp_path)
    with sqlite3.connect(tmp_path / "sales.db") as conn:
        assert conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0] == 6
