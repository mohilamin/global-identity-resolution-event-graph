"""Graph export helpers."""

import json

import pandas as pd


def to_graph_json(nodes: pd.DataFrame, edges: pd.DataFrame) -> dict[str, object]:
    """Return graph JSON payload."""
    return {
        "nodes": nodes.to_dict(orient="records"),
        "edges": edges.to_dict(orient="records"),
        "node_count": len(nodes),
        "edge_count": len(edges),
    }


def write_graph_json(path: str, nodes: pd.DataFrame, edges: pd.DataFrame) -> None:
    """Write graph JSON payload."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(to_graph_json(nodes, edges), file, indent=2)

