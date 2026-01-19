"""Pytest plugins for automation framework."""

from .test_result_logger import pytest_runtest_logreport

__all__ = ["pytest_runtest_logreport"]
