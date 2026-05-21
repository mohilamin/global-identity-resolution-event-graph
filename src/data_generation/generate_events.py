"""Generate synthetic multi-channel events."""

import json

import numpy as np
import pandas as pd

from src.common.config import settings
from src.common.logging import get_logger
from src.common.paths import EVENTS, PROFILES, ensure_dirs

LOGGER = get_logger(__name__)

EVENT_TYPES = [
    "web_page_view",
    "mobile_app",
    "ad_click",
    "signup",
    "login",
    "purchase",
    "subscription",
    "payment",
    "support_ticket",
    "account_recovery",
    "device_change",
    "cookie_reset",
]


def _load_or_generate_truth() -> pd.DataFrame:
    if not (PROFILES / "ground_truth_identity_map.csv").exists():
        from src.data_generation.generate_ground_truth import generate_ground_truth

        return generate_ground_truth()
    return pd.read_csv(PROFILES / "ground_truth_identity_map.csv")


def generate_events() -> dict[str, int]:
    """Generate synthetic events and conversion journeys."""
    ensure_dirs()
    cfg = settings()
    rng = np.random.default_rng(int(cfg.get("random_seed", 42)) + 1)
    event_count = int(cfg.get("target_event_count", 300_000))
    truth = _load_or_generate_truth().fillna("")

    sample = truth.sample(event_count, replace=True, random_state=43).reset_index(drop=True)
    event_types = rng.choice(
        EVENT_TYPES,
        event_count,
        p=[0.32, 0.14, 0.14, 0.06, 0.11, 0.08, 0.04, 0.04, 0.03, 0.01, 0.02, 0.01],
    )
    event_ts = pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 120 * 24 * 60, event_count), unit="m")
    sessions = np.array([f"sess_{i:07d}" for i in rng.integers(1, event_count // 3, event_count)])
    campaign = rng.choice([f"cmp_{i:03d}" for i in range(1, 41)], event_count)
    product = rng.choice([f"prd_{i:04d}" for i in range(1, 501)], event_count)
    channels = rng.choice(["paid_search", "social", "organic", "affiliate", "direct"], event_count)
    regions = rng.choice(["NA", "EU", "APAC", "LATAM"], event_count)

    events = pd.DataFrame(
        {
            "event_id": [f"evt_{i:09d}" for i in range(1, event_count + 1)],
            "event_type": event_types,
            "event_timestamp": event_ts,
            "anonymous_user_id": sample["anonymous_user_id"],
            "known_user_id": np.where(np.isin(event_types, ["signup", "login", "purchase", "subscription", "payment", "support_ticket", "account_recovery"]), sample["known_user_id"], ""),
            "device_id": sample["device_id"],
            "cookie_id": sample["cookie_id"],
            "session_id": sessions,
            "ip_id": [f"ip_{i:06d}" for i in rng.integers(1, 26_000, event_count)],
            "browser_fingerprint_id": [f"bf_{i:06d}" for i in rng.integers(1, 28_000, event_count)],
            "email_hash": np.where(np.isin(event_types, ["signup", "login", "purchase"]), sample["email_hash"], ""),
            "phone_hash": np.where(np.isin(event_types, ["signup", "account_recovery"]), sample["phone_hash"], ""),
            "payment_instrument_id": np.where(np.isin(event_types, ["purchase", "subscription", "payment"]), sample["payment_instrument_id"], ""),
            "campaign_id": np.where(np.isin(event_types, ["ad_click", "signup", "purchase", "subscription"]), campaign, ""),
            "product_id": np.where(np.isin(event_types, ["purchase", "subscription", "web_page_view"]), product, ""),
            "geo_region": regions,
            "channel": channels,
            "user_agent_family": rng.choice(["chrome", "safari", "firefox", "edge"], event_count),
            "event_source": np.where(np.isin(event_types, ["mobile_app"]), "mobile", np.where(np.isin(event_types, ["ad_click"]), "ads", "web")),
            "payload": [json.dumps({"synthetic": True, "amount": float(x)}) for x in rng.lognormal(3.2, 0.6, event_count).round(2)],
        }
    )
    events.to_csv(EVENTS / "all_events.csv", index=False)

    event_to_file = {
        "web_page_view": "web_page_view_events.csv",
        "mobile_app": "mobile_app_events.csv",
        "ad_click": "ad_click_events.csv",
        "signup": "signup_events.csv",
        "login": "login_events.csv",
        "purchase": "purchase_events.csv",
        "subscription": "subscription_events.csv",
        "payment": "payment_events.csv",
        "support_ticket": "support_ticket_events.csv",
        "account_recovery": "account_recovery_events.csv",
        "device_change": "device_change_events.csv",
        "cookie_reset": "cookie_reset_events.csv",
    }
    counts: dict[str, int] = {"all_events": len(events)}
    for event_type, file_name in event_to_file.items():
        subset = events.loc[events["event_type"] == event_type]
        subset.to_csv(EVENTS / file_name, index=False)
        counts[file_name] = len(subset)

    (EVENTS / "event_generation_summary.json").write_text(json.dumps(counts, indent=2), encoding="utf-8")
    LOGGER.info("Generated %s synthetic events", len(events))
    return counts


if __name__ == "__main__":
    generate_events()

