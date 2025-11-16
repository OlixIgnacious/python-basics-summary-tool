import pandas as pd
from pybasics.main import summarize

def test_summarize():
    df = pd.DataFrame({"a": [1, None, 3], "b": ["x", "y", "z"]})
    s = summarize(df)
    assert s["n_rows"] == 3
    assert s["n_cols"] == 2
    assert "a" in s["columns"]
    assert s["missing_counts"]["a"] == 1
