"""Deterministic identity rules."""

import pandas as pd


def build_deterministic_edges(truth: pd.DataFrame) -> pd.DataFrame:
    """Build high-confidence deterministic identity links from ground truth."""
    rows: list[dict[str, object]] = []
    for _, row in truth.iterrows():
        known = row["known_user_id"]
        mappings = [
            ("anonymous_user_id", "login_cookie_to_known_user", 0.95, "LOGIN_LINK"),
            ("email_hash", "same_verified_email_hash", 0.99, "VERIFIED_EMAIL"),
            ("phone_hash", "same_verified_phone_hash", 0.98, "VERIFIED_PHONE"),
            ("payment_instrument_id", "same_payment_instrument", 0.96, "PAYMENT_MATCH"),
            ("support_account_id", "account_recovery_support_link", 0.94, "ACCOUNT_RECOVERY"),
        ]
        for col, link_type, score, reason in mappings:
            value = row.get(col, "")
            if isinstance(value, str) and value:
                rows.append(
                    {
                        "source_node_id": known,
                        "target_node_id": value,
                        "link_type": link_type,
                        "match_method": "deterministic",
                        "confidence_score": score,
                        "reason_codes": reason,
                        "evidence_event_ids": "profile_surface",
                        "created_at": "2026-01-01T00:00:00Z",
                        "real_identity_id": row["real_identity_id"],
                    }
                )
    return pd.DataFrame(rows)
