import pytest

from ..db import DBConfig, MySQLClient


@pytest.fixture(scope="session")
def db_client(test_settings, logger):
    """Create database client with connection pooling."""
    logger.info("Setting up database client...")
    db_config = test_settings.get_db_config()
    if not db_config:
        logger.warning("Database configuration not provided, skipping...")
        pytest.skip("Database configuration not provided")

    logger.info(
        f"Connecting to database: {db_config.get('database')} at {db_config.get('host')}"
    )
    client = MySQLClient(**DBConfig.get_mysql_config(test_settings))
    client.connect()
    logger.info("Database connection pool created")
    yield client
    logger.info("Closing database connection pool...")
    client.disconnect()
    logger.info("Database connection pool closed")
