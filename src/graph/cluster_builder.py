"""Identity cluster construction."""

import json

import pandas as pd

from src.common.paths import GRAPH


def build_clusters(truth: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    """Build cluster summary from ground truth and resolved links."""
    counts = edges.groupby("source_node_id").size().rename("edge_count").reset_index()
    clusters = truth[["real_identity_id", "known_user_id"]].merge(
        counts, left_on="known_user_id", right_on="source_node_id", how="left"
    )
    clusters["edge_count"] = clusters["edge_count"].fillna(0).astype(int)
    clusters["cluster_id"] = [f"cluster_{i:06d}" for i in range(1, len(clusters) + 1)]
    clusters["cluster_size"] = clusters["edge_count"] + 2
    clusters["identity_confidence_score"] = (88 + (clusters["edge_count"].clip(0, 8) * 1.2)).clip(0, 99)
    clusters["explainability"] = "cluster created from ground truth surfaces plus resolved identity edges"
    clusters = clusters[
        [
            "cluster_id",
            "real_identity_id",
            "known_user_id",
            "cluster_size",
            "edge_count",
            "identity_confidence_score",
            "explainability",
        ]
    ]
    clusters.to_csv(GRAPH / "identity_clusters.csv", index=False)
    summary = {
        "identity_cluster_count": int(len(clusters)),
        "average_cluster_size": round(float(clusters["cluster_size"].mean()), 3),
        "average_identity_confidence_score": round(float(clusters["identity_confidence_score"].mean()), 3),
    }
    (GRAPH / "cluster_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return clusters

