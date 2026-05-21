"""Streamlit dashboard for identity resolution."""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src.common.paths import ATTRIBUTION, CLUSTERS, GRAPH, LINEAGE, SCORECARDS


def _csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def main() -> None:
    """Render the Streamlit dashboard."""
    st.set_page_config(page_title="Identity Resolution Event Graph", layout="wide")
    st.title("Global Identity Resolution & Attribution Event Graph")

    identity_report = _json(SCORECARDS / "identity_resolution_report.json")
    graph_report = _json(SCORECARDS / "graph_quality_report.json")
    attribution_report = _json(SCORECARDS / "attribution_quality_report.json")
    fraud_report = _json(SCORECARDS / "fraud_cluster_report.json")

    st.header("Executive Overview")
    cols = st.columns(4)
    cols[0].metric("Identity Clusters", f"{identity_report.get('identity_cluster_count', 0):,}")
    cols[1].metric("Resolution Quality", identity_report.get("identity_resolution_quality_score", 0))
    cols[2].metric("Graph Edges", f"{int(graph_report.get('edge_count', 0)):,}")
    cols[3].metric("Suspicious Clusters", fraud_report.get("suspicious_cluster_count", 0))

    tabs = st.tabs(
        [
            "Identity Quality",
            "Graph Explorer",
            "Match Decisions",
            "Link Explanations",
            "Sessions",
            "Attribution",
            "Suspicious Clusters",
            "Scorecards",
        ]
    )
    with tabs[0]:
        st.json(identity_report)
        st.json(graph_report)
    with tabs[1]:
        st.dataframe(_csv(GRAPH / "identity_clusters.csv").head(100), use_container_width=True)
        st.dataframe(_csv(GRAPH / "identity_nodes.csv").head(100), use_container_width=True)
    with tabs[2]:
        st.dataframe(_csv(GRAPH / "identity_edges.csv").head(200), use_container_width=True)
    with tabs[3]:
        explanations = _json(LINEAGE / "identity_link_explanations.json")
        st.json(explanations[:20] if isinstance(explanations, list) else explanations)
    with tabs[4]:
        st.dataframe(_csv(Path("data/events/stitched_sessions.csv")).head(200), use_container_width=True)
    with tabs[5]:
        st.json(attribution_report)
        st.dataframe(_csv(ATTRIBUTION / "conversion_attribution.csv").head(200), use_container_width=True)
    with tabs[6]:
        st.dataframe(_csv(CLUSTERS / "suspicious_identity_clusters.csv"), use_container_width=True)
    with tabs[7]:
        for path in sorted(SCORECARDS.glob("*.json")):
            st.subheader(path.stem)
            st.json(_json(path))


if __name__ == "__main__":
    main()

