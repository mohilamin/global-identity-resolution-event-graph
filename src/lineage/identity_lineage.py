"""Identity lineage helpers."""

import pandas as pd


def lineage_coverage(edges: pd.DataFrame) -> float:
    """Return percent of links with reason codes."""
    return round(float(edges["reason_codes"].astype(str).ne("").mean() * 100), 3)

