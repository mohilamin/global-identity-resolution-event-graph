"""DuckDB warehouse loader."""

import duckdb
import pandas as pd

from src.common.paths import ATTRIBUTION, CLUSTERS, GRAPH, PROFILES, SCORECARDS, WAREHOUSE


def load_duckdb_store() -> str:
    """Create the local DuckDB warehouse from generated outputs."""
    WAREHOUSE.mkdir(parents=True, exist_ok=True)
    db_path = WAREHOUSE / "identity_resolution.duckdb"
    con = duckdb.connect(str(db_path))
    tables = {
        "profiles": PROFILES / "ground_truth_identity_map.csv",
        "ground_truth": PROFILES / "ground_truth_identity_map.csv",
        "identity_nodes": GRAPH / "identity_nodes.csv",
        "identity_edges": GRAPH / "identity_edges.csv",
        "identity_clusters": GRAPH / "identity_clusters.csv",
        "attribution_paths": ATTRIBUTION / "attribution_paths.csv",
        "suspicious_clusters": CLUSTERS / "suspicious_identity_clusters.csv",
    }
    for table, path in tables.items():
        frame = pd.read_csv(path, low_memory=False)
        con.register(f"{table}_df", frame)
        con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM {table}_df")
    scorecards = []
    for path in SCORECARDS.glob("*.csv"):
        frame = pd.read_csv(path)
        frame["scorecard_name"] = path.stem
        scorecards.append(frame.astype(str))
    if scorecards:
        scorecard_frame = pd.concat(scorecards, ignore_index=True, sort=False)
        con.register("scorecards_df", scorecard_frame)
        con.execute("CREATE OR REPLACE TABLE scorecards AS SELECT * FROM scorecards_df")
    con.close()
    return str(db_path)
