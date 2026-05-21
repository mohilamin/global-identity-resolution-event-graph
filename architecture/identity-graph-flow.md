# Identity Graph Flow

The graph contains identity, account, device, browser, payment, support, campaign, session, and conversion nodes. Edges represent explainable identity links with method, confidence score, evidence, and reason codes.

```mermaid
flowchart TD
    A["known_user"] --> B["email"]
    A --> C["phone"]
    A --> D["payment"]
    A --> E["anonymous_user"]
    E --> F["cookie"]
    E --> G["device"]
    G --> H["session"]
    H --> I["conversion"]
```

