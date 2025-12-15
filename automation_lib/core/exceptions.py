"""Custom exceptions for automation library."""

from typing import Optional


class AutomationError(Exception):
    """Base exception for all automation errors."""

    def __init__(self, message: str, details: Optional[str] = None):
        """Initialize automation error.

        Args:
            message: Error message
            details: Additional error details
        """
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return string representation of error."""
        if self.details:
            return f"{self.message}\nDetails: {self.details}"
        return self.message


# Browser-related exceptions
class BrowserError(AutomationError):
    """Base exception for browser-related errors."""

    pass


class BrowserLaunchError(BrowserError):
    """Exception raised when browser fails to launch."""

    pass


class BrowserConnectionError(BrowserError):
    """Exception raised when browser connection fails."""

    pass


class BrowserTimeoutError(BrowserError):
    """Exception raised when browser operation times out."""

    pass


# Page-related exceptions
class PageError(AutomationError):
    """Base exception for page-related errors."""

    pass


class NavigationError(PageError):
    """Exception raised when page navigation fails."""

    def __init__(self, url: str, message: str, details: Optional[str] = None):
        """Initialize navigation error.

        Args:
            url: The URL that failed to load
            message: Error message
            details: Additional error details
        """
        self.url = url
        super().__init__(message, details)

    def __str__(self) -> str:
        """Return string representation of error."""
        error_msg = f"Failed to navigate to '{self.url}': {self.message}"
        if self.details:
            error_msg += f"\nDetails: {self.details}"
        return error_msg


class PageLoadError(PageError):
    """Exception raised when page fails to load properly."""

    pass


class PageNotReadyError(PageError):
    """Exception raised when page is not ready for interaction."""

    pass


# Locator-related exceptions
class LocatorError(AutomationError):
    """Base exception for locator-related errors."""

    def __init__(self, selector: str, message: str, details: Optional[str] = None):
        """Initialize locator error.

        Args:
            selector: The selector that caused the error
            message: Error message
            details: Additional error details
        """
        self.selector = selector
        super().__init__(message, details)

    def __str__(self) -> str:
        """Return string representation of error."""
        error_msg = f"Locator error for '{self.selector}': {self.message}"
        if self.details:
            error_msg += f"\nDetails: {self.details}"
        return error_msg


class ElementNotFoundError(LocatorError):
    """Exception raised when element is not found on the page."""

    def __init__(self, selector: str, timeout: Optional[int] = None):
        """Initialize element not found error.

        Args:
            selector: The selector that was not found
            timeout: Timeout value if applicable
        """
        message = "Element not found"
        if timeout:
            message += f" (timeout: {timeout}ms)"
        super().__init__(selector, message)


class ElementNotVisibleError(LocatorError):
    """Exception raised when element is not visible."""

    pass


class ElementNotClickableError(LocatorError):
    """Exception raised when element is not clickable."""

    pass


class ElementStateError(LocatorError):
    """Exception raised when element is in unexpected state."""

    pass


class MultipleElementsFoundError(LocatorError):
    """Exception raised when multiple elements match selector expecting single element."""

    def __init__(self, selector: str, count: int):
        """Initialize multiple elements found error.

        Args:
            selector: The selector that matched multiple elements
            count: Number of elements found
        """
        message = f"Expected single element but found {count}"
        super().__init__(selector, message)
        self.count = count


# Database-related exceptions
class DatabaseError(AutomationError):
    """Base exception for database-related errors."""

    pass


class DatabaseConnectionError(DatabaseError):
    """Exception raised when database connection fails."""

    def __init__(
        self, host: str, database: str, message: str, details: Optional[str] = None
    ):
        """Initialize database connection error.

        Args:
            host: Database host
            database: Database name
            message: Error message
            details: Additional error details
        """
        self.host = host
        self.database = database
        super().__init__(message, details)

    def __str__(self) -> str:
        """Return string representation of error."""
        error_msg = f"Failed to connect to database '{self.database}' at '{self.host}': {self.message}"
        if self.details:
            error_msg += f"\nDetails: {self.details}"
        return error_msg


class DatabaseQueryError(DatabaseError):
    """Exception raised when database query fails."""

    def __init__(self, query: str, message: str, details: Optional[str] = None):
        """Initialize database query error.

        Args:
            query: The SQL query that failed
            message: Error message
            details: Additional error details
        """
        self.query = query
        super().__init__(message, details)

    def __str__(self) -> str:
        """Return string representation of error."""
        # Truncate query if too long
        display_query = (
            self.query if len(self.query) <= 100 else self.query[:100] + "..."
        )
        error_msg = f"Query failed: {self.message}\nQuery: {display_query}"
        if self.details:
            error_msg += f"\nDetails: {self.details}"
        return error_msg


class DatabasePoolError(DatabaseError):
    """Exception raised when connection pool encounters an error."""

    pass


# Configuration-related exceptions
class ConfigurationError(AutomationError):
    """Base exception for configuration-related errors."""

    pass


class MissingConfigurationError(ConfigurationError):
    """Exception raised when required configuration is missing."""

    def __init__(self, key: str, message: Optional[str] = None):
        """Initialize missing configuration error.

        Args:
            key: The configuration key that is missing
            message: Optional custom message
        """
        self.key = key
        default_message = f"Required configuration key '{key}' is missing"
        super().__init__(message or default_message)


class InvalidConfigurationError(ConfigurationError):
    """Exception raised when configuration value is invalid."""

    def __init__(self, key: str, value: any, reason: str):
        """Initialize invalid configuration error.

        Args:
            key: The configuration key
            value: The invalid value
            reason: Reason why value is invalid
        """
        self.key = key
        self.value = value
        message = f"Invalid configuration for '{key}': {reason} (value: {value})"
        super().__init__(message)


# Test data-related exceptions
class TestDataError(AutomationError):
    """Base exception for test data-related errors."""

    pass


class TestDataNotFoundError(TestDataError):
    """Exception raised when test data is not found."""

    pass


class TestDataValidationError(TestDataError):
    """Exception raised when test data validation fails."""

    pass


# Assertion-related exceptions
class AssertionError(AutomationError):
    """Base exception for assertion-related errors."""

    pass


class ElementAssertionError(AssertionError):
    """Exception raised when element assertion fails."""

    def __init__(self, selector: str, expected: any, actual: any, assertion_type: str):
        """Initialize element assertion error.

        Args:
            selector: The element selector
            expected: Expected value
            actual: Actual value
            assertion_type: Type of assertion (text, visible, enabled, etc.)
        """
        self.selector = selector
        self.expected = expected
        self.actual = actual
        self.assertion_type = assertion_type
        message = f"Assertion '{assertion_type}' failed for '{selector}': expected '{expected}', got '{actual}'"
        super().__init__(message)


class TimeoutAssertionError(AssertionError):
    """Exception raised when assertion times out."""

    pass
