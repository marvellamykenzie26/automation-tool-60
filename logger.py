import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(
    name: str = "automation_tool",
    log_file: str = "logs/app.log",
    max_bytes: int = 5 * 1024 * 1024,  # 5 MB
    backup_count: int = 3,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configures a logger with console output and rotating file storage."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent handler duplication if setup is called multiple times
    if logger.handlers:
        return logger

    log_format = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Ensure the log file directory exists
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Configure rotating file handler
    file_handler = RotatingFileHandler(
        filename=str(log_path),
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)

    # Configure standard stdout console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    return logger