# Implementation Plan

## Phase 1: Project Foundation

Create the Python project setup, Docker files, GitHub Actions workflow, Makefile, config files, README, AGENTS, and architecture documentation.

## Phase 2: Synthetic Identity Surfaces

Generate deterministic synthetic profiles for real identities, known users, anonymous users, devices, cookies, emails, phones, payment instruments, IP addresses, browser fingerprints, and support accounts.

Intentional fragmentation patterns:

- multiple devices per identity
- multiple cookies per identity
- cookie resets
- anonymous browsing before signup
- mobile app activity before known login
- shared household devices
- shared payment instruments
- support account links
- account recovery links
- suspicious multi-account clusters

## Phase 3: Event Generation

Generate at least 300,000 multi-channel events across web, mobile, ads, signup, login, purchase, subscription, payment, support, account recovery, device change, and cookie reset streams.

Each event includes required identity, device, campaign, session, geo, channel, and payload fields.

## Phase 4: Matching and Sessionization

Implement deterministic matching for verified identifiers and login/recovery events. Implement probabilistic matching for device/time continuity, IP/fingerprint overlap, session continuity, geo similarity, and campaign-to-signup continuity.

Session stitching links anonymous and known sessions across login, cookie reset, and device continuity.

## Phase 5: Graph and Attribution

Build graph nodes and identity edges, export graph JSON, create connected-component clusters, and generate attribution paths from ad click to signup, purchase, subscription, and retention.

## Phase 6: Fraud and Trust Signals

Detect suspicious clusters for shared payment, many accounts on one device, bot-like signup bursts, account recovery abuse, suspicious campaign conversions, and impossible device switching.

## Phase 7: Explainability, Lineage, and Scorecards

Generate link explanations, decision lineage, graph lineage, identity resolution scorecards, graph quality reports, matching accuracy reports, session stitching reports, attribution quality reports, and fraud cluster reports.

## Phase 8: API, Dashboard, Warehouse, and Tests

Load outputs into DuckDB, expose demo-friendly FastAPI endpoints, build a clean Streamlit dashboard, and add tests covering generation, matching, graph, attribution, fraud, lineage, scorecards, API, and the full pipeline.

