# Data Dictionary

## Profiles

- `known_users`: logged-in synthetic user accounts.
- `anonymous_users`: anonymous browsing identities.
- `devices`: synthetic devices linked to identities.
- `cookies`: browser cookies and reset generations.
- `emails`, `phones`: hashed synthetic contact identifiers.
- `payment_instruments`: synthetic payment surfaces with shared-payment patterns.
- `ip_addresses`, `browser_fingerprints`: network and browser identity hints.
- `support_accounts`: support identities linked after purchase or recovery.

## Events

`all_events.csv` includes 300,000 synthetic web, mobile, ad, signup, login, purchase, subscription, payment, support, account recovery, device change, and cookie reset events.

## Graph

- `identity_nodes.csv`: graph nodes.
- `identity_edges.csv`: explainable identity links.
- `identity_clusters.csv`: resolved identity clusters.

