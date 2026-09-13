"""Configuration loading utilities for CustomerPulse."""

from pathlib import Path

import yaml


def load_config(path: str | Path) -> dict:
    """Load a YAML configuration file."""

    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if config is None:
        return {}

    return config