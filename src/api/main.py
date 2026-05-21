"""FastAPI service for the identity graph."""

import json
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import FastAPI

from src.api.schemas import ExplainLinkRequest, ResolveIdentityRequest, SimulateEventRequest
from src.common.paths import ATTRIBUTION, CLUSTERS, GRAPH, LINEAGE, SCORECARDS
from src.pipeline.run_all import run_pipeline

app = FastAPI(title="Global Identity Resolution & Attribution Event Graph")


def _records(path: Path, limit: int = 100) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return pd.read_csv(path, low_memory=False).head(limit).fillna("").to_dict(orient="records")


def _json(path: Path) -> Any:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


@app.get("/health")
def health() -> dict[str, str]:
    """Service health."""
    return {"status": "ok", "service": "identity-resolution-event-graph"}


@app.get("/identity-summary")
def identity_summary() -> dict[str, Any]:
    """Return high-level identity summary."""
    report = _json(SCORECARDS / "identity_resolution_report.json")
    graph = _json(SCORECARDS / "graph_quality_report.json")
    return {"identity_resolution": report, "graph_quality": graph}


@app.get("/identity-clusters")
def identity_clusters() -> list[dict[str, Any]]:
    """Return identity clusters."""
    return _records(GRAPH / "identity_clusters.csv")


@app.get("/identity-clusters/{cluster_id}")
def identity_cluster(cluster_id: str) -> dict[str, Any]:
    """Return one identity cluster."""
    rows = _records(GRAPH / "identity_clusters.csv", limit=100000)
    return next((row for row in rows if row.get("cluster_id") == cluster_id), {"cluster_id": cluster_id, "found": False})


@app.get("/identity-links")
def identity_links() -> list[dict[str, Any]]:
    """Return identity links."""
    return _records(GRAPH / "identity_edges.csv")


@app.get("/link-explanations")
def link_explanations() -> Any:
    """Return link explanations."""
    return _json(LINEAGE / "identity_link_explanations.json")[:100]


@app.get("/attribution-paths")
def attribution_paths() -> list[dict[str, Any]]:
    """Return attribution paths."""
    return _records(ATTRIBUTION / "conversion_attribution.csv")


@app.get("/suspicious-clusters")
def suspicious_clusters() -> list[dict[str, Any]]:
    """Return suspicious clusters."""
    return _records(CLUSTERS / "suspicious_identity_clusters.csv")


@app.get("/scorecards")
def scorecards() -> dict[str, Any]:
    """Return scorecard summary."""
    return {path.stem: _json(path) for path in SCORECARDS.glob("*.json")}


@app.get("/graph-summary")
def graph_summary() -> dict[str, Any]:
    """Return graph summary."""
    return _json(GRAPH / "cluster_summary.json")


@app.post("/resolve-identity")
def resolve_identity(request: ResolveIdentityRequest) -> dict[str, Any]:
    """Demo identity resolution endpoint."""
    score = 0.96 if request.email_hash else 0.82 if request.device_id else 0.65
    return {
        "decision": "candidate_link_created" if score >= 0.72 else "insufficient_evidence",
        "confidence_score": score,
        "reason_codes": ["EMAIL_MATCH"] if request.email_hash else ["DEVICE_CONTINUITY"],
    }


@app.post("/explain-link")
def explain_link(request: ExplainLinkRequest) -> dict[str, Any]:
    """Demo link explanation endpoint."""
    return {
        "source_node_id": request.source_node_id,
        "target_node_id": request.target_node_id,
        "why_linked": "This demo explanation uses stored graph evidence when available.",
        "recommended_review": False,
    }


@app.post("/simulate-event")
def simulate_event(request: SimulateEventRequest) -> dict[str, Any]:
    """Demo event simulation endpoint."""
    return {
        "accepted": True,
        "event_type": request.event_type,
        "channel": request.channel,
        "next_stage": "session_stitching_and_identity_resolution",
    }


@app.post("/run-pipeline")
def run_pipeline_endpoint() -> dict[str, Any]:
    """Run the local pipeline."""
    return run_pipeline()
