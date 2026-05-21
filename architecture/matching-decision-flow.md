# Matching Decision Flow

Deterministic links use verified signals such as email, phone, payment, login, and account recovery. Probabilistic links use continuity patterns such as device, session, IP/fingerprint, geo, and campaign continuity.

```mermaid
flowchart TD
    A["Candidate Pair"] --> B{"Verified Signal"}
    B -->|yes| C["Deterministic Link"]
    B -->|no| D["Weighted Signals"]
    D --> E["Confidence Score"]
    E --> F{"Threshold"}
    F -->|pass| G["Explained Edge"]
    F -->|fail| H["No Link"]
```

