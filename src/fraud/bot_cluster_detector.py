"""Bot-like cluster detector."""

import pandas as pd


def detect_bot_like_clusters(events: pd.DataFrame) -> pd.DataFrame:
    """Detect suspicious rapid signup clusters by IP."""
    signups = events.loc[events["event_type"] == "signup"]
    grouped = signups.groupby("ip_id").size().reset_index(name="signup_count")
    return grouped.loc[grouped["signup_count"] >= 8].head(20)

