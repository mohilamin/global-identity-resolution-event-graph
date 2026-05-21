"""Confidence scoring helpers."""


def bounded_score(value: float) -> float:
    """Clamp a confidence value to 0..1."""
    return round(max(0.0, min(1.0, value)), 4)


def confidence_band(score: float) -> str:
    """Return a readable confidence band."""
    if score >= 0.9:
        return "high"
    if score >= 0.75:
        return "medium"
    return "low"

