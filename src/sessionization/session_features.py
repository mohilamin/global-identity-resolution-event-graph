"""Session feature helpers."""

import pandas as pd


def summarize_session_features(sessions: pd.DataFrame) -> dict[str, float]:
    """Return compact session feature summary."""
    return {
        "session_count": float(len(sessions)),
        "avg_session_events": float(sessions["event_count"].mean()),
        "stitched_rate": float(sessions["stitched_identity_flag"].mean()),
    }

