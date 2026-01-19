"""Base Page class for all page objects."""

from typing import Literal

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page

from automation_lib.core.exceptions import PlaywrightCustomError
from automation_lib.core.logger import Logger


class BasePage:
    """Base class for all page objects with common functionality."""

    def __init__(self, page: Page, page_name: str = "BasePage") -> None:
        """Initialize the base page with a Playwright page object.

        Args:
            page: Playwright Page object
            page_name: Name of the page for logging purposes
        """
        self.page = page
        # self.page.on(
        #     "request", lambda request: print(">>", request.method, request.url)
        # )
        # self.page.on(
        #     "response", lambda response: print("<<", response.status, response.url)
        # )
        self.logger = Logger.get_logger(page_name)

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
            self.page.wait_for_url(url)
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during navigate :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def refresh_page(
        self,
        wait_until: Literal[
            "commit", "domcontentloaded", "load", "networkidle"
        ] = "networkidle",
    ) -> None:
        """Refresh the page (soft refresh, like F5)."""
        try:
            self.logger.info("Refreshing the page")
            self.page.reload(wait_until=wait_until)
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during refresh_page :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def hard_refresh_page(self) -> None:
        """Simulate a hard refresh (bypass cache) using JavaScript."""
        try:
            self.logger.info("Performing hard refresh (bypass cache)")
            self.page.evaluate("location.reload(true)")
            self.page.wait_for_load_state("load")
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during hard_refresh_page :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def wait_for_url(self, url: str) -> None:
        """Wait for the page to navigate to a specific URL.

        Args:
            url: The URL to wait for
        """
        try:
            self.logger.info(f"Waiting for URL: {url}")
            self.page.wait_for_url(url)
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during wait_for_url :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def get_title(self) -> str:
        """Get the page title.

        Returns:
            The page title
        """
        try:
            self.logger.info("Getting page title")
            return self.page.title()
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during get_title :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def click_locator(self, locator, description=""):
        """Click on a given locator.
        Args:
            locator: The Locator object to click
            description: Optional description for logging
        """
        try:
            self.logger.info(f"Clicking on: {description or locator}")
            locator.click()
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during click_locator :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def double_click_locator(self, locator, description=""):
        """Double click on a given locator.
        Args:
            locator: The Locator object to double click
            description: Optional description for logging
        """
        try:
            self.logger.info(f"Double clicking on: {description or locator}")
            locator.dblclick()
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during double_click_locator :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def right_click_locator(self, locator, description=""):
        """Right click on a given locator.
        Args:
            locator: The Locator object to right click
            description: Optional description for logging
        """
        try:
            self.logger.info(f"Right clicking on: {description or locator}")
            locator.click(button="right")
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during right_click_locator :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def click_locator_with_modifier(self, locator, modifier: str, description=""):
        """Click on a given locator with a keyboard modifier.
        Args:
            locator: The Locator object to click
            modifier: The keyboard modifier (e.g., 'Shift', 'Control', 'Alt', 'Meta')
            description: Optional description for logging
        """
        try:
            self.logger.info(
                f"Clicking on: {description or locator} with modifier: {modifier}"
            )
            locator.click(modifiers=[modifier])
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during click_locator_with_modifier :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def hover_locator(self, locator, description=""):
        """Hover over a given locator.
        Args:
            locator: The Locator object to hover over
            description: Optional description for logging
        """
        try:
            self.logger.info(f"Hovering over: {description or locator}")
            locator.hover()
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during hover_locator :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def click_position_locator(self, locator, position: dict, description=""):
        """Click on a given locator at a specific position.
        Args:
            locator: The Locator object to click
            position: A dictionary with 'x' and 'y' coordinates
            description: Optional description for logging
        """
        try:
            self.logger.info(
                f"Clicking on: {description or locator} at position: {position}"
            )
            locator.click(position=position)
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during click_position_locator :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def fill_locator(self, locator, value, description=""):
        """Fill a given locator with a value.
        Args:
            locator: The Locator object to fill
            value: The value to fill
            description: Optional description for logging
        """
        try:
            self.logger.info(f"Filling {description or locator} with value: ########")
            locator.fill(value)
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during fill_locator :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def type_characters_sequentially(self, locator, value, delay=0, description=""):
        """Type characters into a given locator sequentially with a delay.
        Args:
            locator: The Locator object to type into
            value: The value to type
            delay: Delay in milliseconds between each character
            description: Optional description for logging
        """
        try:
            self.logger.info(
                f"Typing into {description or locator} with value: ########"
            )
            locator.press_sequentially(value, delay=delay)
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during type_characters_sequentially :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def press_keyboard_key(self, locator, key: str, description=""):
        """Press a keyboard key on a given locator.
        Args:
            locator: The Locator object to press the key on
            key: The key to press (e.g., 'Enter', 'Tab', 'Escape')
            description: Optional description for logging
        """
        try:
            self.logger.info(f"Pressing key '{key}' on: {description or locator}")
            locator.press(key)
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during press_keyboard_key :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def focus_locator(self, locator, description=""):
        """Focus on a given locator.
        Args:
            locator: The Locator object to focus on
            description: Optional description for logging
        """
        try:
            self.logger.info(f"Focusing on: {description or locator}")
            locator.focus()
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during focus_locator :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def check_locator(self, locator, description=""):
        """Check a checkbox locator.
        Args:
            locator: The Locator object to check
            description: Optional description for logging
        """
        try:
            self.logger.info(f"Checking checkbox: {description or locator}")
            locator.check()
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during check_locator :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def select_option_locator_by_value(self, locator, value, description=""):
        """Select an option in a dropdown locator.
        Args:
            locator: The Locator object to select option from
            value: The value to select
            description: Optional description for logging
        """
        try:
            self.logger.info(f"Selecting option '{value}' in: {description or locator}")
            locator.select_option(value)
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during select_option_locator_by_value :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def select_option_locator_by_label(self, locator, label, description=""):
        """Select an option in a dropdown locator by label.
        Args:
            locator: The Locator object to select option from
            label: The label to select
            description: Optional description for logging
        """
        try:
            self.logger.info(f"Selecting option '{label}' in: {description or locator}")
            locator.select_option(label=label)
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during select_option_locator_by_label :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def select_multiple_options_locator_by_values(
        self, locator, values, description=""
    ):
        """Select multiple options in a dropdown locator by values.
        Args:
            locator: The Locator object to select options from
            values: The list of values to select
            description: Optional description for logging
        """
        try:
            self.logger.info(
                f"Selecting options '{values}' in: {description or locator}"
            )
            locator.select_option(values)
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during select_multiple_options_locator_by_values :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def scroll_into_view_locator(self, locator, description=""):
        """Scroll a given locator into view.
        Args:
            locator: The Locator object to scroll into view
            description: Optional description for logging
        """
        try:
            self.logger.info(f"Scrolling into view: {description or locator}")
            locator.scroll_into_view_if_needed()
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during scroll_into_view_locator :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def get_text(self, locator, description="") -> str:
        """Get the text content of a locator as a string (never None)."""
        try:
            self.logger.info(f"Getting text content: {description or locator}")
            value = locator.text_content()
            return value if value is not None else ""
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during get_text :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def get_inner_text(self, locator, description="") -> str:
        """Get the inner text of a locator as a string (never None)."""
        try:
            self.logger.info(f"Getting inner text: {description or locator}")
            value = locator.inner_text()
            return value if value is not None else ""
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during get_inner_text :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def get_attribute(self, locator, attr_name: str, description="") -> str:
        """Get the attribute value of a locator as a string (never None)."""
        try:
            self.logger.info(
                f"Getting attribute '{attr_name}': {description or locator}"
            )
            value = locator.get_attribute(attr_name)
            return value if value is not None else ""
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during get_attribute :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def is_visible(self, locator, description="") -> bool:
        """Check if a locator is visible."""
        try:
            self.logger.info(f"Checking visibility: {description or locator}")
            return locator.is_visible()
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during is_visible :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def is_enabled(self, locator, description="") -> bool:
        """Check if a locator is enabled."""
        try:
            self.logger.info(f"Checking enabled state: {description or locator}")
            return locator.is_enabled()
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during is_enabled :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def wait_for(self, locator, state="visible", timeout=20000, description=""):
        """Wait for a locator to reach a given state (default: visible)."""
        try:
            self.logger.info(
                f"Waiting for locator: {description or locator} to be {state}"
            )
            locator.wait_for(state=state, timeout=timeout)
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during wait_for :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )

    def get_value(self, locator, description="") -> str:
        """Get the value property of an input or similar element as a string (never None)."""
        try:
            self.logger.info(f"Getting value property: {description or locator}")
            value = locator.input_value()
            return value if value is not None else ""
        except PlaywrightError as e:
            self.logger.error(
                f"Playwright error during get_value :{e.message} | Name: {getattr(e, 'name', '')}"
            )
            raise PlaywrightCustomError(
                message=e.message,
                details=f"{getattr(e, 'name', '')}: {getattr(e, 'stack', '')}",
            )
