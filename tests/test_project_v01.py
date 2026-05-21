"""V0.1 project acceptance tests."""

import json
from pathlib import Path

import duckdb
import pandas as pd
from fastapi.testclient import TestClient

from src.api.main import app
from src.attribution.attribution_scoring import score_attribution
from src.common.paths import (
    ATTRIBUTION,
    CLUSTERS,
    EVENTS,
    GRAPH,
    LINEAGE,
    PROFILES,
    SCORECARDS,
    WAREHOUSE,
)
from src.data_generation.generate_events import generate_events
from src.data_generation.generate_ground_truth import generate_ground_truth
from src.data_generation.generate_profiles import generate_profiles
from src.fraud.bot_cluster_detector import detect_bot_like_clusters
from src.fraud.multi_account_abuse import detect_multi_account_devices
from src.fraud.shared_payment_detector import detect_shared_payments
from src.graph.graph_metrics import calculate_graph_metrics
from src.ingestion.loaders import load_csv
from src.ingestion.validators import require_columns
from src.lineage.identity_lineage import lineage_coverage
from src.matching.confidence_scoring import bounded_score, confidence_band
from src.matching.deterministic_rules import build_deterministic_edges
from src.matching.probabilistic_matcher import build_probabilistic_edges


def test_profile_generation_counts() -> None:
    summary = generate_profiles()
    assert summary["known_users"] == 20_000
    assert summary["anonymous_users"] >= 30_000


def test_ground_truth_generation_count() -> None:
    truth = generate_ground_truth()
    assert len(truth) == 20_000
    assert truth["real_identity_id"].is_unique


def test_event_generation_count() -> None:
    summary = generate_events()
    assert summary["all_events"] == 300_000


def test_event_files_exist() -> None:
    for name in [
        "web_page_view_events.csv",
        "mobile_app_events.csv",
        "ad_click_events.csv",
        "signup_events.csv",
        "login_events.csv",
        "purchase_events.csv",
        "subscription_events.csv",
        "payment_events.csv",
        "support_ticket_events.csv",
        "account_recovery_events.csv",
        "device_change_events.csv",
        "cookie_reset_events.csv",
    ]:
        assert (EVENTS / name).exists()


def test_all_events_required_columns() -> None:
    events = pd.read_csv(EVENTS / "all_events.csv", nrows=10)
    require_columns(
        events,
        [
            "event_id",
            "event_type",
            "event_timestamp",
            "anonymous_user_id",
            "known_user_id",
            "device_id",
            "cookie_id",
            "session_id",
            "ip_id",
            "browser_fingerprint_id",
            "email_hash",
            "phone_hash",
            "payment_instrument_id",
            "campaign_id",
            "product_id",
            "geo_region",
            "channel",
            "user_agent_family",
            "event_source",
            "payload",
        ],
    )


def test_profile_files_exist() -> None:
    for name in [
        "known_users.csv",
        "anonymous_users.csv",
        "devices.csv",
        "cookies.csv",
        "emails.csv",
        "phones.csv",
        "payment_instruments.csv",
        "ip_addresses.csv",
        "browser_fingerprints.csv",
        "support_accounts.csv",
    ]:
        assert (PROFILES / name).exists()


def test_load_csv_returns_frame() -> None:
    assert not load_csv(PROFILES / "known_users.csv").empty


def test_require_columns_raises_for_missing() -> None:
    try:
        require_columns(pd.DataFrame({"a": [1]}), ["b"])
    except ValueError as exc:
        assert "Missing required columns" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_session_stitching_output_exists() -> None:
    sessions = pd.read_csv(EVENTS / "stitched_sessions.csv")
    assert not sessions.empty
    assert "stitched_identity_flag" in sessions.columns


def test_stiched_compatibility_file_exists() -> None:
    assert (EVENTS / "stiched_sessions.csv").exists()


def test_deterministic_matching_edges() -> None:
    truth = pd.read_csv(PROFILES / "ground_truth_identity_map.csv").head(5)
    edges = build_deterministic_edges(truth)
    assert not edges.empty
    assert (edges["confidence_score"] >= 0.94).all()


def test_probabilistic_matching_edges() -> None:
    events = pd.read_csv(EVENTS / "all_events.csv").head(5000)
    edges = build_probabilistic_edges(events)
    assert not edges.empty
    assert edges["match_method"].eq("probabilistic").all()


def test_confidence_score_bounds() -> None:
    assert bounded_score(2) == 1.0
    assert bounded_score(-1) == 0.0


def test_confidence_bands() -> None:
    assert confidence_band(0.95) == "high"
    assert confidence_band(0.8) == "medium"
    assert confidence_band(0.5) == "low"


def test_identity_nodes_created() -> None:
    nodes = pd.read_csv(GRAPH / "identity_nodes.csv")
    assert {"node_id", "node_type"}.issubset(nodes.columns)
    assert len(nodes) > 50_000


def test_identity_edges_created() -> None:
    edges = pd.read_csv(GRAPH / "identity_edges.csv")
    assert {"source_node_id", "target_node_id", "confidence_score", "reason_codes"}.issubset(edges.columns)
    assert len(edges) > 50_000


def test_identity_clusters_created() -> None:
    clusters = pd.read_csv(GRAPH / "identity_clusters.csv")
    assert len(clusters) == 20_000
    assert clusters["identity_confidence_score"].between(0, 100).all()


def test_graph_json_exists() -> None:
    assert (GRAPH / "identity_graph.json").exists()


def test_cluster_summary_json_exists() -> None:
    payload = json.loads((GRAPH / "cluster_summary.json").read_text())
    assert payload["identity_cluster_count"] == 20_000


def test_graph_metrics_calculate() -> None:
    nodes = pd.read_csv(GRAPH / "identity_nodes.csv").head(100)
    edges = pd.read_csv(GRAPH / "identity_edges.csv").head(100)
    clusters = pd.read_csv(GRAPH / "identity_clusters.csv").head(100)
    metrics = calculate_graph_metrics(nodes, edges, clusters)
    assert metrics["node_count"] == 100


def test_attribution_paths_created() -> None:
    paths = pd.read_csv(ATTRIBUTION / "attribution_paths.csv")
    assert not paths.empty
    assert "multi_touch_path" in paths.columns


def test_conversion_attribution_created() -> None:
    attribution = pd.read_csv(ATTRIBUTION / "conversion_attribution.csv")
    assert attribution["attribution_confidence_score"].between(0, 1).all()


def test_attribution_scoring_range() -> None:
    paths = pd.DataFrame({"identity_resolution_dependency_count": [1, 3], "conversion_lag_hours": [10, 100]})
    scored = score_attribution(paths)
    assert scored["attribution_confidence_score"].between(0, 1).all()


def test_suspicious_clusters_created() -> None:
    clusters = pd.read_csv(CLUSTERS / "suspicious_identity_clusters.csv")
    assert not clusters.empty
    assert clusters["fraud_risk_score"].between(0, 100).all()


def test_shared_payment_detector() -> None:
    payments = pd.DataFrame(
        {"payment_instrument_id": ["p"] * 7, "real_identity_id": [f"r{i}" for i in range(7)]}
    )
    assert not detect_shared_payments(payments).empty


def test_bot_cluster_detector_schema() -> None:
    events = pd.DataFrame({"event_type": ["signup"] * 8, "ip_id": ["ip_1"] * 8})
    assert detect_bot_like_clusters(events).iloc[0]["signup_count"] == 8


def test_multi_account_detector_schema() -> None:
    events = pd.DataFrame({"device_id": ["d"] * 8, "known_user_id": [f"k{i}" for i in range(8)]})
    assert detect_multi_account_devices(events).iloc[0]["known_user_count"] == 8


def test_decision_lineage_created() -> None:
    lineage = pd.read_csv(LINEAGE / "identity_decision_lineage.csv")
    assert "lineage_step" in lineage.columns


def test_link_explanations_created() -> None:
    explanations = json.loads((LINEAGE / "identity_link_explanations.json").read_text())
    assert explanations
    assert "why_linked" in explanations[0]


def test_graph_lineage_created() -> None:
    lineage = json.loads((LINEAGE / "graph_lineage.json").read_text())
    assert "transformations" in lineage


def test_lineage_coverage() -> None:
    edges = pd.read_csv(GRAPH / "identity_edges.csv").head(100)
    assert lineage_coverage(edges) == 100.0


def test_identity_resolution_scorecard_exists() -> None:
    assert (SCORECARDS / "identity_resolution_report.json").exists()
    assert (SCORECARDS / "identity_resolution_report.csv").exists()


def test_graph_quality_scorecard_exists() -> None:
    assert (SCORECARDS / "graph_quality_report.json").exists()
    assert (SCORECARDS / "graph_quality_report.csv").exists()


def test_matching_accuracy_scorecard_exists() -> None:
    assert (SCORECARDS / "matching_accuracy_report.json").exists()
    assert (SCORECARDS / "matching_accuracy_report.csv").exists()


def test_session_stitching_scorecard_exists() -> None:
    assert (SCORECARDS / "session_stitching_report.json").exists()
    assert (SCORECARDS / "session_stitching_report.csv").exists()


def test_attribution_scorecard_exists() -> None:
    assert (SCORECARDS / "attribution_quality_report.json").exists()
    assert (SCORECARDS / "attribution_quality_report.csv").exists()


def test_fraud_cluster_scorecard_exists() -> None:
    assert (SCORECARDS / "fraud_cluster_report.json").exists()
    assert (SCORECARDS / "fraud_cluster_report.csv").exists()


def test_identity_resolution_score_range() -> None:
    payload = json.loads((SCORECARDS / "identity_resolution_report.json").read_text())
    assert 0 <= payload["identity_resolution_quality_score"] <= 100


def test_matching_accuracy_metrics() -> None:
    payload = json.loads((SCORECARDS / "matching_accuracy_report.json").read_text())
    assert 0 <= payload["match_precision_estimate"] <= 1
    assert 0 <= payload["match_recall_estimate"] <= 1


def test_attribution_quality_metrics() -> None:
    payload = json.loads((SCORECARDS / "attribution_quality_report.json").read_text())
    assert payload["attribution_path_count"] > 0


def test_duckdb_store_exists() -> None:
    assert (WAREHOUSE / "identity_resolution.duckdb").exists()


def test_duckdb_tables_readable() -> None:
    con = duckdb.connect(str(WAREHOUSE / "identity_resolution.duckdb"), read_only=True)
    count = con.execute("select count(*) from identity_edges").fetchone()[0]
    con.close()
    assert count > 0


def test_pipeline_summary_fixture(pipeline_outputs: dict[str, object]) -> None:
    assert pipeline_outputs["events"] == 300_000
    assert pipeline_outputs["clusters"] == 20_000


def test_api_health() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_api_identity_summary() -> None:
    client = TestClient(app)
    response = client.get("/identity-summary")
    assert response.status_code == 200
    assert "identity_resolution" in response.json()


def test_api_identity_clusters() -> None:
    client = TestClient(app)
    response = client.get("/identity-clusters")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_api_identity_cluster_detail() -> None:
    client = TestClient(app)
    cluster_id = pd.read_csv(GRAPH / "identity_clusters.csv").iloc[0]["cluster_id"]
    response = client.get(f"/identity-clusters/{cluster_id}")
    assert response.status_code == 200
    assert response.json()["cluster_id"] == cluster_id


def test_api_identity_links() -> None:
    client = TestClient(app)
    response = client.get("/identity-links")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_api_link_explanations() -> None:
    client = TestClient(app)
    response = client.get("/link-explanations")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_api_attribution_paths() -> None:
    client = TestClient(app)
    response = client.get("/attribution-paths")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_api_suspicious_clusters() -> None:
    client = TestClient(app)
    response = client.get("/suspicious-clusters")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_api_scorecards() -> None:
    client = TestClient(app)
    response = client.get("/scorecards")
    assert response.status_code == 200
    assert "identity_resolution_report" in response.json()


def test_api_graph_summary() -> None:
    client = TestClient(app)
    response = client.get("/graph-summary")
    assert response.status_code == 200
    assert response.json()["identity_cluster_count"] == 20_000


def test_api_resolve_identity() -> None:
    client = TestClient(app)
    response = client.post("/resolve-identity", json={"known_user_id": "ku_000001", "email_hash": "email_hash"})
    assert response.status_code == 200
    assert response.json()["confidence_score"] >= 0.9


def test_api_explain_link() -> None:
    client = TestClient(app)
    response = client.post("/explain-link", json={"source_node_id": "ku_000001", "target_node_id": "dev_000001"})
    assert response.status_code == 200
    assert "why_linked" in response.json()


def test_api_simulate_event() -> None:
    client = TestClient(app)
    response = client.post("/simulate-event", json={"event_type": "purchase", "channel": "paid_search"})
    assert response.status_code == 200
    assert response.json()["accepted"] is True


def test_api_run_pipeline_endpoint() -> None:
    client = TestClient(app)
    response = client.post("/run-pipeline")
    assert response.status_code == 200
    assert response.json()["events"] == 300_000


def test_docs_exist() -> None:
    for path in [
        Path("README.md"),
        Path("AGENTS.md"),
        Path("docs/implementation-plan.md"),
        Path("architecture/architecture.md"),
        Path("docs/metrics.md"),
    ]:
        assert path.exists()

