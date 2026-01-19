import pytest

from ..core import Logger


@pytest.fixture(scope="session")
def logger():
    """Setup logger with pytest's log level."""
    logger = Logger.get_logger("Fixtures")
    logger.info(f"Logger level: {Logger.get_logger_level(logger)}")
    return logger
