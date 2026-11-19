# Sales Data Quality & ETL Pipeline

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white) ![pandas](https://img.shields.io/badge/pandas-Data%20Processing-150458?logo=pandas&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white) ![pytest](https://img.shields.io/badge/pytest-Automated%20Tests-0A9EDC?logo=pytest&logoColor=white)

A small, reproducible **ETL and data quality engineering** project built with Python, pandas, SQLite and pytest. It ingests raw sales records, identifies invalid transactions, calculates order totals, loads accepted records into a relational database, and exports a machine-readable quality report.

Built as a portfolio exercise focused on **data validation, defect detection, SQL and automated testing**.

## Pipeline overview

```text
Raw sales CSV
     |
     v
Extract (pandas)
     |
     v
Validate (missing fields, duplicates, numeric rules)
     |                         |
     | valid                   | invalid
     v                         v
Transform (order totals)    rejected_sales.csv
     |
     v
Load (SQLite: sales table)
     |
     +--> clean_sales.csv
     +--> quality_report.json
```

## Example results

Running the included sample dataset produces:

```text
ETL completed!
Rows: 10 | Valid: 6 | Rejected: 4
Total revenue: 1386.00
```

The sample intentionally contains invalid records to demonstrate rejection and reporting. The project has **9 pytest tests**, including a full pipeline integration test.

## Tech stack

| Tool | Purpose |
| --- | --- |
| Python | Pipeline orchestration and validation logic |
| pandas | CSV ingestion and data transformations |
| SQLite | Relational storage and SQL data checks |
| pytest | Unit and integration tests |
| GitHub Actions | CI tests on pushes and pull requests |

## Getting started (Windows / VS Code)

**Prerequisites:** Python 3.13 and Git (for publishing). Open this repository folder in VS Code and run in PowerShell:

```powershell
py -V:3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.main
.\.venv\Scripts\python.exe -m pytest -v
```

You do **not** need to activate the virtual environment. If your Python launcher is unavailable, create the environment with a working Python 3.13 executable instead.

On macOS/Linux, use `python3 -m venv .venv`, `.venv/bin/python -m pip install -r requirements.txt`, `.venv/bin/python -m src.main`, and `.venv/bin/python -m pytest -v`.

### Custom input and output paths

```powershell
.\.venv\Scripts\python.exe -m src.main --input data/sales.csv --output output
```

## Data quality rules

- Reject missing order IDs and product names.
- Reject duplicate order IDs (first occurrence is retained).
- Require quantities to be positive integers.
- Require prices to be finite positive numbers.
- Calculate each accepted order's `total = quantity * price`.
- Store validated records in SQLite with database constraints.

Invalid rows are exported separately with a reason, rather than silently dropped.

## Generated outputs

The `output/` directory is created at runtime and excluded from version control.

| File | Contents |
| --- | --- |
| `clean_sales.csv` | Accepted rows with calculated totals |
| `rejected_sales.csv` | Rejected rows and validation errors |
| `sales.db` | SQLite database containing the `sales` table |
| `quality_report.json` | Input/accepted/rejected counts, revenue and rejection reasons |

To explore SQL-based checks, open `output/sales.db` in a SQLite client and run queries from [`sql/quality_checks.sql`](sql/quality_checks.sql).

## Testing and CI

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

The test suite covers validation rules, transformation behavior, and an end-to-end ETL run. The workflow in [`.github/workflows/tests.yml`](.github/workflows/tests.yml) runs the tests automatically on GitHub after pushes and pull requests.

## Repository structure

```text
sales-data-quality-pipeline/
├── .github/workflows/tests.yml
├── data/sales.csv
├── sql/quality_checks.sql
├── src/
│   ├── extract.py
│   ├── validate.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
├── tests/
│   ├── test_validation.py
│   ├── test_transform.py
│   └── test_pipeline.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Limitations and next steps

This is a learning/portfolio project, **not a production ETL service**. Monetary calculations currently use floating-point numbers rather than `Decimal` or integer cents. Duplicate IDs are reserved by the first occurrence even if that row is invalid. Potential improvements include explicit schema contracts, structured logging, configurable validation rules, scheduled ingestion, and richer SQL reconciliation checks.
