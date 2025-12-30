"""Browser management for Playwright."""

from typing import Literal, Optional

from playwright.sync_api import Browser, Playwright, sync_playwright

from automation_lib.core.exceptions import BrowserError, BrowserLaunchError

BrowserType = Literal["chromium", "firefox", "webkit"]


class BrowserManager:
    """Manages Playwright browser instances."""

    def __init__(self, browser_type: BrowserType = "chromium", headless: bool = False):
        """Initialize browser manager.

        Args:
            browser_type: Type of browser to launch
            headless: Whether to run in headless mode
        """
        self.browser_type = browser_type
        self.headless = headless
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None

    def launch(self, **kwargs) -> Browser:
        """Launch a browser instance.

        Args:
            **kwargs: Additional browser launch options

        Returns:
            Browser instance

        Raises:
            BrowserLaunchError: If browser fails to launch
        """
        try:
            self.playwright = sync_playwright().start()

            browser_launcher = {
                "chromium": self.playwright.chromium,
                "firefox": self.playwright.firefox,
                "webkit": self.playwright.webkit,
            }[self.browser_type]

            self.browser = browser_launcher.launch(headless=self.headless, **kwargs)
            return self.browser
        except Exception as e:
            raise BrowserLaunchError(
                message=f"Unexpected error launching {self.browser_type} browser",
                details=str(e),
            )

    def close(self) -> None:
        """Close browser and playwright instance.

        Raises:
            BrowserError: If browser cleanup fails
        """
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
        except Exception as e:
            raise BrowserError(
                message="Unexpected error closing browser", details=str(e)
            )
