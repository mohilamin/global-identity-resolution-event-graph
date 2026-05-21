# Demo Script

## 0:00-0:30 Business Problem

Explain that large consumer platforms see fragmented identities across cookies, devices, sessions, ads, purchases, payments, and support.

## 0:30-1:00 Synthetic Data

Run:

```bash
python -m src.data_generation.generate_profiles
python -m src.data_generation.generate_events
python -m src.data_generation.generate_ground_truth
```

Show the profile, event, and ground truth files.

## 1:00-1:45 Identity Graph

Run:

```bash
python -m src.pipeline.run_all
```

Show `identity_nodes.csv`, `identity_edges.csv`, and `identity_clusters.csv`.

## 1:45-2:20 Attribution and Fraud

Show attribution paths and suspicious identity clusters.

## 2:20-3:00 API, Dashboard, and Evidence

Show scorecards, API endpoints, and Streamlit dashboard.

