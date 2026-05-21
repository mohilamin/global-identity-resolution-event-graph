"""Configuration loading helpers."""

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML file relative to the project root."""
    full_path = ROOT / path if isinstance(path, str) else path
    with full_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def settings() -> dict[str, Any]:
    """Return project settings."""
    return load_yaml("config/settings.yaml")

