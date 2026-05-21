"""Run the full identity resolution pipeline."""

import pandas as pd

from src.attribution.conversion_attribution import create_conversion_attribution
from src.attribution.path_builder import build_attribution_paths
from src.common.logging import get_logger
from src.common.paths import EVENTS, PROFILES, ensure_dirs
from src.data_generation.generate_events import generate_events
from src.data_generation.generate_ground_truth import generate_ground_truth
from src.data_generation.generate_profiles import generate_profiles
from src.fraud.suspicious_cluster_detector import detect_suspicious_clusters
from src.graph.cluster_builder import build_clusters
from src.graph.identity_graph_builder import build_identity_graph
from src.lineage.decision_lineage import write_decision_lineage
from src.lineage.graph_lineage import write_graph_lineage
from src.matching.link_explainer import build_link_explanations
from src.scorecards.attribution_report import write_attribution_quality_report
from src.scorecards.graph_quality_report import write_graph_quality_report
from src.scorecards.identity_resolution_report import write_identity_resolution_report
from src.scorecards.matching_accuracy_report import write_matching_accuracy_report
from src.sessionization.session_stitcher import stitch_sessions
from src.storage.duckdb_store import load_duckdb_store

LOGGER = get_logger(__name__)


def run_pipeline() -> dict[str, object]:
    """Run all pipeline stages and return key output counts."""
    ensure_dirs()
    if not (PROFILES / "known_users.csv").exists():
        generate_profiles()
    if not (PROFILES / "ground_truth_identity_map.csv").exists():
        truth = generate_ground_truth()
    else:
        truth = pd.read_csv(PROFILES / "ground_truth_identity_map.csv")
    if not (EVENTS / "all_events.csv").exists():
        generate_events()
    events = pd.read_csv(EVENTS / "all_events.csv")

    sessions = stitch_sessions(events)
    nodes, edges = build_identity_graph(events, truth)
    clusters = build_clusters(truth, edges)
    attribution_paths = build_attribution_paths(events)
    conversion_attribution = create_conversion_attribution(attribution_paths)
    suspicious = detect_suspicious_clusters(events)

    write_decision_lineage(edges)
    build_link_explanations(edges)
    write_graph_lineage()
    write_identity_resolution_report(edges, clusters)
    write_graph_quality_report(nodes, edges, clusters)
    write_matching_accuracy_report(edges, truth)
    write_attribution_quality_report(conversion_attribution, events)
    db_path = load_duckdb_store()

    summary = {
        "profiles": int(len(truth)),
        "events": int(len(events)),
        "sessions": int(len(sessions)),
        "nodes": int(len(nodes)),
        "edges": int(len(edges)),
        "clusters": int(len(clusters)),
        "attribution_paths": int(len(attribution_paths)),
        "suspicious_clusters": int(len(suspicious)),
        "warehouse": db_path,
    }
    LOGGER.info("Pipeline completed: %s", summary)
    return summary


if __name__ == "__main__":
    run_pipeline()

