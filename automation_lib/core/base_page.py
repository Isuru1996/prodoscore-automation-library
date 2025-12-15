"""Base Page class for all page objects."""

from playwright.sync_api import Locator, Page

from automation_lib.core.exceptions import LocatorError, NavigationError
from automation_lib.core.logger import Logger


class BasePage:
    """Base class for all page objects with common functionality."""

    def __init__(self, page: Page):
        """Initialize the base page with a Playwright page object.

        Args:
            page: Playwright Page object
        """
        self.page = page
        self.logger = Logger.get_logger("test_automation")

    def navigate_to(self, url: str) -> None:
        """Navigate to a specific URL.

        Args:
            url: The URL to navigate to

        Raises:
            NavigationError: If navigation fails
        """
        try:
            self.logger.info(f"Navigating to: {url}")
            self.page.goto(url)
            self.logger.info(f"Successfully navigated to: {url}")
        except Exception as e:
            self.logger.error(f"Navigation failed to {url}: {str(e)}")
            raise NavigationError(
                url=url, message="Unexpected error during navigation", details=str(e)
            )

    def get_title(self) -> str:
        """Get the page title.

        Returns:
            The page title
        """
        return self.page.title()

    def click(self, selector: str) -> None:
        """Click an element.

        Args:
            selector: The element selector

        Raises:
            ElementNotFoundError: If element is not found
            ElementNotClickableError: If element is not clickable
        """
        try:
            self.page.click(selector)
        except Exception as e:
            raise LocatorError(
                selector=selector,
                message="Unexpected error during click",
                details=str(e),
            )

    def fill(self, selector: str, value: str) -> None:
        """Fill an input field.

        Args:
            selector: The input field selector
            value: The value to fill

        Raises:
            ElementNotFoundError: If element is not found
            LocatorError: If fill operation fails
        """
        try:
            self.page.fill(selector, value)
        except Exception as e:
            raise LocatorError(
                selector=selector,
                message="Unexpected error during fill",
                details=str(e),
            )

    def get_text(self, selector: str) -> str:
        """Get text content of an element.

        Args:
            selector: The element selector

        Returns:
            The text content

        Raises:
            ElementNotFoundError: If element is not found
            LocatorError: If text retrieval fails
        """
        try:
            return self.page.locator(selector).text_content() or ""
        except Exception as e:
            raise LocatorError(
                selector=selector,
                message="Unexpected error getting text",
                details=str(e),
            )

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if an element is visible.

        Args:
            selector: The element selector
            timeout: Maximum time to wait in milliseconds

        Returns:
            True if visible, False otherwise
        """
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except Exception as e:
            raise LocatorError(
                selector=selector,
                message="Unexpected error checking visibility",
                details=str(e),
            )

    def wait_for_element(self, selector: str, timeout: int = 10000) -> Locator:
        """Wait for an element to be present.

        Args:
            selector: The element selector
            timeout: Maximum time to wait in milliseconds

        Returns:
            The Locator object

        Raises:
            ElementNotFoundError: If element is not found within timeout
        """
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            return self.page.locator(selector)
        except Exception as e:
            raise LocatorError(
                selector=selector,
                message="Unexpected error waiting for element",
                details=str(e),
            )
