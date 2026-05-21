"""Time helpers."""

import pandas as pd


def utc_now_iso() -> str:
    """Return current UTC timestamp as ISO text."""
    return pd.Timestamp.now("UTC").isoformat()

