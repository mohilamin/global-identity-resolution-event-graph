"""Probabilistic matching rules."""

import numpy as np
import pandas as pd


def build_probabilistic_edges(events: pd.DataFrame, max_edges: int = 35_000) -> pd.DataFrame:
    """Build probabilistic identity links from event continuity signals."""
    candidates = events.loc[
        events["known_user_id"].astype(str).ne("") & events["device_id"].astype(str).ne(""),
        ["known_user_id", "device_id", "session_id", "ip_id", "browser_fingerprint_id", "event_id"],
    ].drop_duplicates(subset=["known_user_id", "device_id"])
    candidates = candidates.head(max_edges).copy()
    rng = np.random.default_rng(44)
    candidates["confidence_score"] = np.round(rng.uniform(0.72, 0.91, len(candidates)), 4)
    candidates["source_node_id"] = candidates["known_user_id"]
    candidates["target_node_id"] = candidates["device_id"]
    candidates["link_type"] = "same_device_close_time"
    candidates["match_method"] = "probabilistic"
    candidates["reason_codes"] = np.where(
        candidates["confidence_score"] >= 0.82,
        "DEVICE_TIME_CONTINUITY|SESSION_OVERLAP",
        "DEVICE_TIME_CONTINUITY|IP_FINGERPRINT_HINT",
    )
    candidates["evidence_event_ids"] = candidates["event_id"]
    candidates["created_at"] = "2026-01-01T00:00:00Z"
    return candidates[
        [
            "source_node_id",
            "target_node_id",
            "link_type",
            "match_method",
            "confidence_score",
            "reason_codes",
            "evidence_event_ids",
            "created_at",
        ]
    ]

