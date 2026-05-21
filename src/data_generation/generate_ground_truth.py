"""Generate ground truth identity map."""

import pandas as pd

from src.common.logging import get_logger
from src.common.paths import PROFILES, ensure_dirs

LOGGER = get_logger(__name__)


def _first_by_identity(path: str, id_col: str) -> pd.DataFrame:
    frame = pd.read_csv(PROFILES / path)
    return frame.groupby("real_identity_id", as_index=False)[id_col].first()


def generate_ground_truth() -> pd.DataFrame:
    """Create a ground truth identity map for evaluation."""
    ensure_dirs()
    required = [
        PROFILES / "known_users.csv",
        PROFILES / "anonymous_users.csv",
        PROFILES / "devices.csv",
        PROFILES / "cookies.csv",
        PROFILES / "emails.csv",
        PROFILES / "phones.csv",
        PROFILES / "payment_instruments.csv",
        PROFILES / "support_accounts.csv",
    ]
    if not all(path.exists() for path in required):
        from src.data_generation.generate_profiles import generate_profiles

        generate_profiles()

    truth = pd.read_csv(PROFILES / "known_users.csv")[["real_identity_id", "known_user_id"]]
    for path, col in [
        ("anonymous_users.csv", "anonymous_user_id"),
        ("devices.csv", "device_id"),
        ("cookies.csv", "cookie_id"),
        ("emails.csv", "email_hash"),
        ("phones.csv", "phone_hash"),
        ("payment_instruments.csv", "payment_instrument_id"),
        ("support_accounts.csv", "support_account_id"),
    ]:
        truth = truth.merge(_first_by_identity(path, col), on="real_identity_id", how="left")
    truth.to_csv(PROFILES / "ground_truth_identity_map.csv", index=False)
    LOGGER.info("Generated ground truth identity map with %s rows", len(truth))
    return truth


if __name__ == "__main__":
    generate_ground_truth()

