"""Conversion attribution outputs."""

import pandas as pd

from src.attribution.attribution_scoring import score_attribution
from src.common.paths import ATTRIBUTION


def create_conversion_attribution(paths: pd.DataFrame) -> pd.DataFrame:
    """Create scored conversion attribution output."""
    scored = score_attribution(paths)
    scored.to_csv(ATTRIBUTION / "conversion_attribution.csv", index=False)
    return scored

