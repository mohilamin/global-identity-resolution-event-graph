"""Input validators."""

import pandas as pd


def require_columns(frame: pd.DataFrame, columns: list[str]) -> None:
    """Raise ValueError when required columns are missing."""
    missing = sorted(set(columns) - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

