"""CSV loading utilities."""

from pathlib import Path

import pandas as pd


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a CSV file with a clear error if missing."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing expected CSV: {csv_path}")
    return pd.read_csv(csv_path)

