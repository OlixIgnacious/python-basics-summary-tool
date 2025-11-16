import pandas as pd
import json
import sys
import argparse
from pathlib import Path

def load_csv(path):
    """Load a CSV file into a pandas DataFrame.

    Args:
        path (str): The file path to the CSV file.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    return pd.read_csv(path)

def summarize(df) -> dict:
    """Generate summary statistics for a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to summarize.

    Returns:
        dict: A dictionary containing summary statistics.
    """
    summary = {
        'num_rows': df.shape[0],
        'num_columns': df.shape[1],
        'column_names': df.columns.tolist(),
        'data_types': df.dtypes.astype('str').to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'descriptive_stats': df.describe().to_dict()
    }
    return summary
    
def save_report(summary, path):
    with open(path, 'w') as f:
        json.dump(summary, f, indent=4)

def main(argv=None):
    parser = argparse.ArgumentParser(description="CSV summary tool")
    parser.add_argument("csv_path", help="Path to CSV file to summarize")
    parser.add_argument("--out", default="summary.json", help="Output summary file (JSON)")
    args = parser.parse_args(argv)

    path = Path(args.csv_path)
    if not path.exists():
        print(f"ERROR: CSV file not found: {path}", file=sys.stderr)
        sys.exit(2)

    try:
        df = load_csv(path)
        summary = summarize(df)
        save_report(summary, Path(args.out))
        print(f"Saved summary to {args.out}")     
    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
