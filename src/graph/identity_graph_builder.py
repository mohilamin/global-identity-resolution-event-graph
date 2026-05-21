"""Build identity graph nodes and edges."""

import json

import pandas as pd

from src.common.paths import GRAPH, PROFILES
from src.matching.deterministic_rules import build_deterministic_edges
from src.matching.probabilistic_matcher import build_probabilistic_edges


def _nodes_from(frame: pd.DataFrame, id_col: str, node_type: str) -> pd.DataFrame:
    return pd.DataFrame({"node_id": frame[id_col].dropna().astype(str).unique(), "node_type": node_type})


def build_identity_graph(events: pd.DataFrame, truth: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build identity graph node and edge exports."""
    GRAPH.mkdir(parents=True, exist_ok=True)
    known = pd.read_csv(PROFILES / "known_users.csv")
    anon = pd.read_csv(PROFILES / "anonymous_users.csv")
    devices = pd.read_csv(PROFILES / "devices.csv")
    cookies = pd.read_csv(PROFILES / "cookies.csv")
    emails = pd.read_csv(PROFILES / "emails.csv")
    phones = pd.read_csv(PROFILES / "phones.csv")
    payments = pd.read_csv(PROFILES / "payment_instruments.csv")
    ips = pd.read_csv(PROFILES / "ip_addresses.csv")
    fingerprints = pd.read_csv(PROFILES / "browser_fingerprints.csv")
    support = pd.read_csv(PROFILES / "support_accounts.csv")

    nodes = pd.concat(
        [
            pd.DataFrame({"node_id": truth["real_identity_id"].astype(str), "node_type": "real_identity"}),
            _nodes_from(known, "known_user_id", "known_user"),
            _nodes_from(anon, "anonymous_user_id", "anonymous_user"),
            _nodes_from(devices, "device_id", "device"),
            _nodes_from(cookies, "cookie_id", "cookie"),
            _nodes_from(emails, "email_hash", "email"),
            _nodes_from(phones, "phone_hash", "phone"),
            _nodes_from(payments, "payment_instrument_id", "payment_instrument"),
            _nodes_from(ips, "ip_id", "ip"),
            _nodes_from(fingerprints, "browser_fingerprint_id", "browser_fingerprint"),
            _nodes_from(support, "support_account_id", "support_account"),
            _nodes_from(events, "session_id", "session"),
            _nodes_from(events.loc[events["campaign_id"].astype(str).ne("")], "campaign_id", "campaign"),
            pd.DataFrame(
                {
                    "node_id": events.loc[events["event_type"].isin(["purchase", "subscription"]), "event_id"].head(20000),
                    "node_type": "conversion",
                }
            ),
        ],
        ignore_index=True,
    ).drop_duplicates("node_id")
    nodes.to_csv(GRAPH / "identity_nodes.csv", index=False)

    deterministic = build_deterministic_edges(truth)
    probabilistic = build_probabilistic_edges(events)
    edges = pd.concat(
        [deterministic.drop(columns=["real_identity_id"], errors="ignore"), probabilistic],
        ignore_index=True,
    )
    edges.insert(0, "edge_id", [f"edge_{i:08d}" for i in range(1, len(edges) + 1)])
    edges.to_csv(GRAPH / "identity_edges.csv", index=False)
    graph_json = {
        "nodes": nodes.head(2000).to_dict(orient="records"),
        "edges": edges.head(5000).to_dict(orient="records"),
        "note": "Truncated graph JSON for demo readability; full CSV exports contain all nodes and edges.",
    }
    (GRAPH / "identity_graph.json").write_text(json.dumps(graph_json, indent=2), encoding="utf-8")
    return nodes, edges

