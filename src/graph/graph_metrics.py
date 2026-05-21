"""Graph quality metrics."""

import pandas as pd


def calculate_graph_metrics(nodes: pd.DataFrame, edges: pd.DataFrame, clusters: pd.DataFrame) -> dict[str, float]:
    """Calculate graph quality metrics."""
    return {
        "node_count": float(len(nodes)),
        "edge_count": float(len(edges)),
        "identity_cluster_count": float(len(clusters)),
        "average_cluster_size": float(clusters["cluster_size"].mean()),
        "graph_connected_component_count": float(len(clusters)),
    }

