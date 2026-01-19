"""Pytest plugin for custom test result logging."""

from automation_lib.core import Logger


def pytest_runtest_logreport(report):
    """Customize test result logging with colored emojis and duration.

    This hook is called after each test phase (setup, call, teardown).
    We only log for the 'call' phase to avoid duplicate messages.
    """
    if report.when == "call":
        test_logger = Logger.get_logger("TestResults")

        if report.passed:
            test_logger.info(
                f"✅ TEST PASSED: {report.nodeid} (Duration: {report.duration:.2f}s)"
            )
        elif report.failed:
            test_logger.error(
                f"❌ TEST FAILED: {report.nodeid} (Duration: {report.duration:.2f}s)"
            )
        elif report.skipped:
            test_logger.warning(f"⚠️ TEST SKIPPED: {report.nodeid}")
