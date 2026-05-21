# Session Stitching Design

Session stitching groups events by session ID, calculates start/end times, event counts, device/cookie continuity, and whether the session contains a known identity. The pipeline writes both `stitched_sessions.csv` and the requested compatibility spelling `stiched_sessions.csv`.

