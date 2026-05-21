# Technical Deep Dive

## Architecture Decisions

DuckDB is used as a local analytical warehouse so the project remains reproducible without cloud services. NetworkX concepts are represented through local graph exports so reviewers can inspect the model without needing a graph database.

## Matching

The system combines deterministic links for verified identifiers with probabilistic links for continuity signals. Each link has confidence, method, reason codes, and evidence.

## Attribution

Attribution paths connect campaign and behavioral touchpoints to purchases and subscriptions. Each path records confidence and dependency on identity resolution.

## Fraud and Trust

Suspicious cluster detection flags shared payment instruments, too many accounts on one device, bot-like signup behavior, and other graph patterns.

## Production Mapping

In production, this design could scale to Kafka/Flink event streaming, Spark/Databricks graph processing, Snowflake/BigQuery warehouse storage, Neo4j/TigerGraph graph serving, Airflow orchestration, dbt transformations, feature stores, and ML-based entity resolution.

