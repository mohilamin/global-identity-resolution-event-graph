"""Fraud cluster scorecard wrapper."""

import pandas as pd


def summarize_fraud_clusters(clusters: pd.DataFrame) -> dict[str, float]:
    """Return fraud cluster summary metrics."""
    return {
        "suspicious_cluster_count": float(len(clusters)),
        "average_fraud_risk_score": float(clusters["fraud_risk_score"].mean()),
    }

