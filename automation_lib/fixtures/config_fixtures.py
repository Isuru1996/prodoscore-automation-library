from pathlib import Path

import pytest

from ..config import TestSettings
from ..core import Config


@pytest.fixture(scope="session", autouse=True)
def config(logger):
    """Load test configuration using automation_lib Config."""
    logger.info("Loading test configuration...")
    default_path = Path.cwd() / "config" / "settings.yaml"
    if default_path.exists():
        logger.info(f"Config file found: {default_path}")
        return Config(str(default_path))
    logger.warning("Config file not found, using defaults")
    return Config()


@pytest.fixture(scope="session")
def test_settings(logger):
    """Load test settings using TestSettings."""
    logger.info("Initializing test settings...")
    return TestSettings()
