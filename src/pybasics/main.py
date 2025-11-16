import sys
import json
import argparse
from pathlib import Path
import pandas as pd

def load_csv(path: Path, encoding: str = "utf-8", nrows: int | None = None) -> pd.DataFrame:
    read_args = {"encoding": encoding}
    if nrows:
        return pd.read_csv(path, nrows=nrows, **read_args)
    return pd.read_csv(path, **read_args)

def summarize(df: pd.DataFrame) -> dict:
    """Return concise summary keys used by the project."""
    return {
        "n_rows": int(df.shape[0]),
        "n_cols": int(df.shape[1]),
        "columns": list(df.columns.astype(str)),
        "dtypes": {str(col): str(dtype) for col, dtype in zip(df.columns, df.dtypes)},
        "missing_counts": {str(col): int(df[col].isna().sum()) for col in df.columns},
    }

def save_report(summary: dict, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

def run_cli(argv=None):
    parser = argparse.ArgumentParser(description="CSV summary tool")
    parser.add_argument("csv_path", help="Path to CSV file to summarize")
    parser.add_argument("--out", "-o", default="summary.json", help="Output summary file (JSON)")
    parser.add_argument("--encoding", default="utf-8", help="CSV file encoding")
    parser.add_argument("--max-rows", type=int, default=None, help="Limit number of rows read (for large files)")
    args = parser.parse_args(argv)

    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        print(f"ERROR: CSV file not found: {csv_path}", file=sys.stderr)
        sys.exit(2)

    try:
        df = load_csv(csv_path, encoding=args.encoding, nrows=args.max_rows)
        summary = summarize(df)
        # print to stdout for quick verification and CI logs
        print(json.dumps(summary, indent=2))
        save_report(summary, Path(args.out))
        print(f"Saved summary to {args.out}")
        sys.exit(0)
    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_cli()