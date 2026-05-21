"""Graph lineage export."""

import json

from src.common.paths import LINEAGE


def write_graph_lineage() -> dict[str, object]:
    """Write graph lineage JSON."""
    payload = {
        "sources": ["profiles", "events", "ground_truth"],
        "transformations": [
            "session_stitching",
            "deterministic_matching",
            "probabilistic_matching",
            "cluster_building",
            "attribution_path_building",
            "suspicious_cluster_detection",
        ],
        "outputs": ["identity_nodes", "identity_edges", "identity_clusters", "scorecards"],
    }
    (LINEAGE / "graph_lineage.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload

