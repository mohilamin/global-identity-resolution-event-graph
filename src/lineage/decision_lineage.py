"""Decision lineage for identity links."""

import pandas as pd

from src.common.paths import LINEAGE


def write_decision_lineage(edges: pd.DataFrame) -> pd.DataFrame:
    """Write lineage rows for identity decisions."""
    lineage = edges[["edge_id", "source_node_id", "target_node_id", "match_method", "confidence_score", "reason_codes"]].copy()
    lineage["lineage_step"] = "identity_match_decision"
    lineage["source_system"] = "synthetic_identity_runtime"
    lineage.to_csv(LINEAGE / "identity_decision_lineage.csv", index=False)
    return lineage

