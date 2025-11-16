# python-basics-summary-tool

Simple CLI tool that summarizes a CSV.

## What it does
- Loads a CSV
- Prints number of rows, columns, column names, dtypes, missing counts
- Saves the summary as JSON

## Run locally
1. Ensure Python 3.8+ is installed.
2. (Optional) create venv:
   python -m venv .venv
   source .venv/bin/activate   # mac/linux
   .venv\Scripts\activate      # windows
3. Install pandas:
   pip install pandas
4. Run:
   python main.py path/to/file.csv --out report.json

Example:
   python main.py data/titanic.csv --out summary.json