from pathlib import Path
from typing import Any

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


@pytest.fixture(scope="function")
def context(browser: Browser, logger, request):
    """Create browser context for each test."""
    # Get auth state file from session if setup_authentication ran
    auth_state_file = getattr(request.config, "_auth_state_file", None)

    logger.info("Creating browser context...")
    context_options: dict[str, Any] = {
        "viewport": {"width": 1920, "height": 1080},
    }

    # Load authentication state if available
    if auth_state_file and Path(auth_state_file).exists():
        logger.info(f"Loading authentication state from {auth_state_file}")
        context_options["storage_state"] = auth_state_file

    context = browser.new_context(**context_options)
    yield context
    logger.info("Closing browser context...")
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext, logger):
    """Create page for each test."""
    logger.info("Creating new page...")
    page = context.new_page()
    yield page
    logger.info("Closing page...")
    page.close()
