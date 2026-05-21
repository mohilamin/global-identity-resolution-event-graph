"""Build attribution paths."""

import pandas as pd

from src.common.paths import ATTRIBUTION


def build_attribution_paths(events: pd.DataFrame) -> pd.DataFrame:
    """Build simple multi-touch attribution paths from campaign events to conversions."""
    ATTRIBUTION.mkdir(parents=True, exist_ok=True)
    conversions = events.loc[events["event_type"].isin(["purchase", "subscription"])].copy().head(25_000)
    rows = []
    for idx, row in conversions.reset_index(drop=True).iterrows():
        touches = [row["channel"]]
        if row["channel"] != "direct":
            touches.append("retargeting")
        touches.append("conversion")
        rows.append(
            {
                "attribution_path_id": f"attr_{idx + 1:08d}",
                "conversion_event_id": row["event_id"],
                "known_user_id": row["known_user_id"],
                "campaign_id": row["campaign_id"] or "organic",
                "first_touch_channel": touches[0],
                "last_touch_channel": touches[-2] if len(touches) > 2 else touches[0],
                "multi_touch_path": ">".join(touches),
                "conversion_lag_hours": int((idx % 168) + 1),
                "identity_resolution_dependency_count": int((idx % 4) + 1),
            }
        )
    paths = pd.DataFrame(rows)
    paths.to_csv(ATTRIBUTION / "attribution_paths.csv", index=False)
    return paths

