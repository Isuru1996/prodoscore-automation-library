import pytest
from playwright.sync_api import Browser, BrowserContext

from ..playwright import BrowserManager


@pytest.fixture(scope="session")
def browser_manager(test_settings, logger):
    """Create browser manager instance."""
    logger.info(
        f"Creating browser manager (browser: {test_settings.browser_type}, headless: {test_settings.headless})"
    )
    manager = BrowserManager(
        browser_type=test_settings.browser_type, headless=test_settings.headless
    )
    yield manager
    logger.info("Closing browser manager...")
    manager.close()


@pytest.fixture(scope="session")
def browser(browser_manager, logger):
    """Launch browser for each test."""
    logger.info("Launching browser...")
    browser = browser_manager.launch()
    yield browser
    logger.info("Closing browser...")
    browser.close()


@pytest.fixture(scope="class")
def context(browser: Browser, logger):
    """Create browser context for each test."""
    logger.info("Creating browser context...")
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
    )
    yield context
    logger.info("Closing browser context...")
    context.close()


@pytest.fixture(scope="class")
def page(context: BrowserContext, logger):
    """Create page for each test."""
    logger.info("Creating new page...")
    page = context.new_page()
    yield page
    logger.info("Closing page...")
    page.close()
