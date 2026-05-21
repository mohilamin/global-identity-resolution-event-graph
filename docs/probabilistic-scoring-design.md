# Probabilistic Scoring Design

The V0.1 probabilistic matcher uses transparent weighted rules rather than opaque ML. Candidate links receive confidence based on device continuity, session overlap, IP and browser fingerprint hints, geo consistency, and campaign-to-signup continuity.

This is intentionally explainable for portfolio review. In production, this could evolve into supervised entity-resolution models, graph embeddings, or real-time feature-store scoring.

