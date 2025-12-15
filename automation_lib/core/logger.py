"""Logging utilities for the automation framework."""

import logging
import sys
from datetime import datetime
from pathlib import Path


class Logger:
    """Logger class for test automation."""

    @staticmethod
    def setup_logger(
        name: str = "automation", log_file: str = "", level: int = logging.INFO
    ) -> logging.Logger:
        """Set up and configure logger.

        Args:
            name: Logger name
            log_file: Path to log file (optional)
            level: Logging level

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Remove existing handlers
        logger.handlers = []

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File handler (if log_file provided)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    @staticmethod
    def get_logger(name: str = "automation") -> logging.Logger:
        """Get existing logger or create a new one.

        Args:
            name: Logger name

        Returns:
            Logger instance
        """
        return logging.getLogger(name)
