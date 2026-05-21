"""API schemas."""

from pydantic import BaseModel


class ResolveIdentityRequest(BaseModel):
    """Request to resolve an identity candidate."""

    known_user_id: str | None = None
    anonymous_user_id: str | None = None
    device_id: str | None = None
    email_hash: str | None = None


class ExplainLinkRequest(BaseModel):
    """Request to explain a graph link."""

    source_node_id: str
    target_node_id: str


class SimulateEventRequest(BaseModel):
    """Request to simulate an event."""

    event_type: str
    channel: str = "direct"

