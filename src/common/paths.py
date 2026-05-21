"""Filesystem path helpers."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

PROFILES = DATA / "profiles"
EVENTS = DATA / "events"
GRAPH = DATA / "graph"
ATTRIBUTION = DATA / "attribution"
CLUSTERS = DATA / "clusters"
LINEAGE = DATA / "lineage"
WAREHOUSE = DATA / "warehouse"
SCORECARDS = DATA / "scorecards"


def ensure_dirs() -> None:
    """Create all runtime output directories."""
    for path in [PROFILES, EVENTS, GRAPH, ATTRIBUTION, CLUSTERS, LINEAGE, WAREHOUSE, SCORECARDS]:
        path.mkdir(parents=True, exist_ok=True)

