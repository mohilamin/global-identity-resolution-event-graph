# AGENTS.md

You are building a FAANG-targeted Data Engineering + Graph Analytics + Attribution + Trust/Fraud Infrastructure project.

Project name:
Global Identity Resolution & Attribution Event Graph

Primary goal:
Build a local production-style identity resolution platform that simulates multi-channel behavioral events, constructs an identity graph, applies deterministic and probabilistic matching, creates attribution paths, scores confidence, and detects suspicious identity clusters.

## Business Context

Large internet platforms must understand identity across fragmented signals:
- anonymous web users
- mobile app users
- logged-in users
- device IDs
- cookies
- sessions
- ad clicks
- purchases
- payments
- support interactions

Identity resolution powers ads attribution, personalization, fraud detection, customer 360, retention analytics, recommendation systems, trust and safety, and marketplace integrity.

## Core Outcome

The system should answer:

"Which fragmented events likely belong to the same identity, how confident are we, and what business/fraud/attribution decisions depend on that link?"

## Build Principles

- Write clean, modular, production-style Python.
- Use Python 3.12.
- Use type hints.
- Use docstrings for public functions.
- Use structured logging.
- Add error handling.
- Use synthetic data only.
- Do not use real sensitive data.
- Do not require external services in V0.1.
- Keep V0.1 deterministic and locally runnable.
- Every identity link must have confidence score and reason codes.
- Every cluster must have explainability.
- Every attribution path must be traceable.
- Every suspicious cluster must include evidence.
- Every major pipeline stage must have tests.
- README must be public-facing and recruiter-friendly.
- Technical docs must be strong enough for senior data engineers and FAANG-style systems reviewers.

## Commit Message Requirements

- Do not use generic AI-like commit messages such as "Build project," "Create files," "Build identity graph," or "Build graph."
- Use human, professional, scoped commit messages.
- Prefer Conventional Commit style:
  - `feat(identity): add entity resolution graph builder`
  - `feat(matching): implement probabilistic identity scoring`
  - `feat(attribution): build multi-touch conversion paths`
  - `feat(fraud): detect suspicious identity clusters`
  - `feat(api): expose identity graph endpoints`
  - `test(graph): cover cluster confidence scoring`
  - `docs(readme): explain event attribution architecture`
  - `fix(matching): correct device-link confidence weights`
- Split unrelated changes into logical commits where reasonable.
- Final commit message should clearly describe the actual work completed.

## Required Validation

```bash
python -m src.data_generation.generate_profiles
python -m src.data_generation.generate_events
python -m src.data_generation.generate_ground_truth
python -m src.pipeline.run_all
python -m pytest
python -m ruff check .
```

