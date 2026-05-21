"""Generate synthetic identity profile surfaces."""

import json

import numpy as np
import pandas as pd

from src.common.config import settings
from src.common.logging import get_logger
from src.common.paths import PROFILES, ensure_dirs

LOGGER = get_logger(__name__)


def _ids(prefix: str, count: int) -> list[str]:
    return [f"{prefix}_{i:06d}" for i in range(1, count + 1)]


def generate_profiles() -> dict[str, int]:
    """Generate synthetic profiles and identity surfaces."""
    ensure_dirs()
    cfg = settings()
    rng = np.random.default_rng(int(cfg.get("random_seed", 42)))
    identity_count = int(cfg.get("real_identity_count", 20_000))

    real_ids = _ids("rid", identity_count)
    regions = np.array(["NA", "EU", "APAC", "LATAM"])
    channels = np.array(["paid_search", "social", "organic", "affiliate", "direct"])

    known_users = pd.DataFrame(
        {
            "real_identity_id": real_ids,
            "known_user_id": _ids("ku", identity_count),
            "account_created_at": pd.date_range("2025-01-01", periods=identity_count, freq="15min"),
            "home_region": rng.choice(regions, identity_count),
            "primary_channel": rng.choice(channels, identity_count),
            "trust_status": rng.choice(["normal", "watch", "review"], identity_count, p=[0.9, 0.08, 0.02]),
        }
    )

    anonymous_count = identity_count + 10_000
    anon_real = rng.choice(real_ids, anonymous_count, replace=True)
    anonymous_users = pd.DataFrame(
        {
            "real_identity_id": anon_real,
            "anonymous_user_id": _ids("au", anonymous_count),
            "first_seen_at": pd.date_range("2024-11-01", periods=anonymous_count, freq="9min"),
            "source_channel": rng.choice(channels, anonymous_count),
            "cookie_reset_flag": rng.choice([False, True], anonymous_count, p=[0.86, 0.14]),
        }
    )

    device_count = identity_count + 12_000
    devices = pd.DataFrame(
        {
            "real_identity_id": rng.choice(real_ids, device_count, replace=True),
            "device_id": _ids("dev", device_count),
            "device_type": rng.choice(["ios", "android", "desktop", "tablet"], device_count),
            "device_first_seen_at": pd.date_range("2024-10-01", periods=device_count, freq="7min"),
            "shared_device_flag": rng.choice([False, True], device_count, p=[0.95, 0.05]),
        }
    )

    cookie_count = identity_count + 18_000
    cookies = pd.DataFrame(
        {
            "real_identity_id": rng.choice(real_ids, cookie_count, replace=True),
            "cookie_id": _ids("ck", cookie_count),
            "browser_family": rng.choice(["chrome", "safari", "firefox", "edge"], cookie_count),
            "cookie_created_at": pd.date_range("2024-10-15", periods=cookie_count, freq="5min"),
            "reset_generation": rng.integers(0, 4, cookie_count),
        }
    )

    emails = pd.DataFrame(
        {
            "real_identity_id": real_ids,
            "email_hash": [f"email_hash_{i:064x}"[-24:] for i in range(identity_count)],
            "verified_email_flag": True,
        }
    )
    phones = pd.DataFrame(
        {
            "real_identity_id": real_ids,
            "phone_hash": [f"phone_hash_{i:064x}"[-24:] for i in range(identity_count)],
            "verified_phone_flag": rng.choice([False, True], identity_count, p=[0.2, 0.8]),
        }
    )

    payments = pd.DataFrame(
        {
            "real_identity_id": rng.choice(real_ids, identity_count + 2_500, replace=True),
            "payment_instrument_id": _ids("pay", identity_count + 2_500),
            "payment_type": rng.choice(["card", "wallet", "bank"], identity_count + 2_500),
            "shared_payment_flag": False,
        }
    )
    for idx in range(0, min(60, len(payments)), 6):
        payments.loc[idx : idx + 5, "payment_instrument_id"] = f"pay_shared_{idx // 6:03d}"
        payments.loc[idx : idx + 5, "shared_payment_flag"] = True

    ip_count = identity_count + 6_000
    ips = pd.DataFrame(
        {
            "real_identity_id": rng.choice(real_ids, ip_count, replace=True),
            "ip_id": _ids("ip", ip_count),
            "geo_region": rng.choice(regions, ip_count),
            "network_type": rng.choice(["residential", "mobile", "corporate", "proxy"], ip_count),
        }
    )
    fingerprints = pd.DataFrame(
        {
            "real_identity_id": rng.choice(real_ids, identity_count + 8_000, replace=True),
            "browser_fingerprint_id": _ids("bf", identity_count + 8_000),
            "user_agent_family": rng.choice(["chrome", "safari", "firefox", "edge"], identity_count + 8_000),
        }
    )
    support = pd.DataFrame(
        {
            "real_identity_id": rng.choice(real_ids, identity_count // 2, replace=False),
            "support_account_id": _ids("sup", identity_count // 2),
            "support_created_at": pd.date_range("2025-03-01", periods=identity_count // 2, freq="30min"),
        }
    )

    outputs = {
        "known_users": known_users,
        "anonymous_users": anonymous_users,
        "devices": devices,
        "cookies": cookies,
        "emails": emails,
        "phones": phones,
        "payment_instruments": payments,
        "ip_addresses": ips,
        "browser_fingerprints": fingerprints,
        "support_accounts": support,
    }
    for name, frame in outputs.items():
        frame.to_csv(PROFILES / f"{name}.csv", index=False)

    summary = {name: len(frame) for name, frame in outputs.items()}
    (PROFILES / "profile_generation_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    LOGGER.info("Generated identity profile surfaces: %s", summary)
    return summary


if __name__ == "__main__":
    generate_profiles()

