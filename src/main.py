"""Run: python -m src.main"""
import argparse
import json
from pathlib import Path
from .extract import extract_sales
from .validate import validate_sales
from .transform import transform_sales
from .load import load_sales

ROOT = Path(__file__).resolve().parent.parent


def run(csv_path: Path, output_dir: Path) -> dict:
    raw = extract_sales(csv_path)
    valid, rejected = validate_sales(raw)
    clean = transform_sales(valid)
    output_dir.mkdir(parents=True, exist_ok=True)
    clean.to_csv(output_dir / "clean_sales.csv", index=False)
    rejected.to_csv(output_dir / "rejected_sales.csv", index=False)
    load_sales(clean, output_dir / "sales.db")
    report = {
        "total_rows": len(raw),
        "valid_rows": len(clean),
        "rejected_rows": len(rejected),
        "total_revenue": round(float(clean["total"].sum()), 2),
        "rejection_reasons": rejected["error"].tolist(),
    }
    (output_dir / "quality_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate sales data and load it into SQLite")
    parser.add_argument("--input", type=Path, default=ROOT / "data" / "sales.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "output")
    args = parser.parse_args()
    report = run(args.input, args.output)
    print("ETL completed!")
    print(f"Rows: {report['total_rows']} | Valid: {report['valid_rows']} | Rejected: {report['rejected_rows']}")
    print(f"Total revenue: {report['total_revenue']:.2f}")
    print(f"Files saved to: {args.output.resolve()}")


if __name__ == "__main__":
    main()
