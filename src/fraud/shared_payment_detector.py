"""Shared payment detector."""

import pandas as pd


def detect_shared_payments(payments: pd.DataFrame, threshold: int = 6) -> pd.DataFrame:
    """Return payment instruments shared across many identities."""
    grouped = (
        payments.groupby("payment_instrument_id")["real_identity_id"]
        .nunique()
        .reset_index(name="involved_identity_count")
    )
    return grouped.loc[grouped["involved_identity_count"] >= threshold].copy()

