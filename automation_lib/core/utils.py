"""Utility functions for the automation framework."""

import time
from typing import Any, Callable


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator to retry a function on failure.

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Delay between retries in seconds

    Returns:
        Decorated function
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    time.sleep(delay)
            return None

        return wrapper

    return decorator


def wait_until(
    condition: Callable[[], bool], timeout: float = 10.0, interval: float = 0.5
) -> bool:
    """Wait until a condition is met.

    Args:
        condition: Callable that returns boolean
        timeout: Maximum time to wait in seconds
        interval: Check interval in seconds

    Returns:
        True if condition met, False if timeout
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition():
            return True
        time.sleep(interval)
    return False
