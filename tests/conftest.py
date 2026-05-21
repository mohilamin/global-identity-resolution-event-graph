"""Shared pytest fixtures."""

import pytest

from src.pipeline.run_all import run_pipeline


@pytest.fixture(scope="session", autouse=True)
def pipeline_outputs() -> dict[str, object]:
    """Run the deterministic pipeline once for test evidence."""
    return run_pipeline()

