# Architecture

The platform simulates a local identity resolution control plane. Synthetic profiles and events are generated first, then stitched into sessions, matched with deterministic and probabilistic rules, converted into graph nodes and edges, clustered, attributed to conversions, scored, and exported to DuckDB, API, and dashboard layers.

```mermaid
flowchart LR
    A["Profiles"] --> B["Events"]
    B --> C["Session Stitching"]
    B --> D["Matching Engine"]
    D --> E["Identity Graph"]
    E --> F["Clusters"]
    B --> G["Attribution"]
    F --> H["Fraud Signals"]
    E --> I["Lineage"]
    F --> J["Scorecards"]
    G --> J
    H --> J
    J --> K["DuckDB/API/Dashboard"]
```

