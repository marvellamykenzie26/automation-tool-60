import logging

import sys

from pathlib import Path

from typing import Optional

class AutomationLogger:
    """Simple logger for automation tool with file and console output."""

    def __init__(self, name: str = "automation-tool-60", log_dir: str = "logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self._configure_handlers()

    def _configure_handlers(self):
        # Clear existing handlers to avoid duplicates
        self.logger.handlers = []

        # File handler
        log_file = self.log_dir / f"{self.name}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_format = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

    def log_exception(self, message: str, exc: Optional[Exception] = None):
        if exc:
            self.logger.exception(message)
        else:
            self.logger.error(message)

if __name__ == "__main__":
    logger = AutomationLogger()
    logger.info("Automation tool started")
    try:
        logger.debug("Processing data")
    except Exception as e:
        logger.log_exception("Error occurred", e)