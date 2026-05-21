"""Attribution confidence scoring."""

import pandas as pd


def score_attribution(paths: pd.DataFrame) -> pd.DataFrame:
    """Score attribution confidence."""
    scored = paths.copy()
    scored["attribution_confidence_score"] = (
        0.9 - (scored["identity_resolution_dependency_count"] * 0.04) - (scored["conversion_lag_hours"] / 1000)
    ).clip(0.5, 0.95)
    return scored

