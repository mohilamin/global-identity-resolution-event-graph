"""Identity link explanation generation."""

import json

import pandas as pd

from src.common.paths import LINEAGE


def build_link_explanations(edges: pd.DataFrame, limit: int = 5000) -> list[dict[str, object]]:
    """Create human-readable link explanations."""
    explanations = []
    for idx, row in edges.head(limit).reset_index(drop=True).iterrows():
        explanations.append(
            {
                "link_id": f"link_{idx + 1:08d}",
                "source_node": row["source_node_id"],
                "target_node": row["target_node_id"],
                "confidence_score": float(row["confidence_score"]),
                "evidence": row.get("evidence_event_ids", ""),
                "reason_codes": str(row["reason_codes"]).split("|"),
                "match_method": row["match_method"],
                "why_linked": f"Linked by {row['match_method']} evidence: {row['reason_codes']}",
                "risk_flags": [] if float(row["confidence_score"]) >= 0.8 else ["review_low_confidence"],
            }
        )
    LINEAGE.mkdir(parents=True, exist_ok=True)
    (LINEAGE / "identity_link_explanations.json").write_text(
        json.dumps(explanations, indent=2), encoding="utf-8"
    )
    return explanations

