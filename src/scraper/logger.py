# logger.py

import logging
import os
from datetime import datetime


class Logger:
    """
    A custom logger class for consistent logging across modules.

    Attributes:
        logger (logging.Logger): The logger instance.
    """

    def __init__(self, name, log_file=None):
        """
        Initializes the Logger.

        Args:
            name (str): Name of the logger, typically __name__ of the calling module.
            log_file (str, optional): Path to the log file. If None, logs to console only.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Create file handler if log_file is provided
        if log_file:
            log_dir = os.path.dirname(log_file)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)

    def info(self, message):
        """Log an info message."""
        self.logger.info(message)

    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)

    def error(self, message):
        """Log an error message."""
        self.logger.error(message)

    def critical(self, message):
        """Log a critical message."""
        self.logger.critical(message)


# Create a default logger instance
default_logger = Logger(
    __name__, log_file=f"logs/linkedin_scraper_{datetime.now().strftime('%Y%m%d')}.log"
)
