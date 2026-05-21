"""Multi-account abuse detector."""

import pandas as pd


def detect_multi_account_devices(events: pd.DataFrame) -> pd.DataFrame:
    """Detect devices tied to many known users."""
    grouped = events.groupby("device_id")["known_user_id"].nunique().reset_index(name="known_user_count")
    return grouped.loc[grouped["known_user_count"] >= 8].head(20)

