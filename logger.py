import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='automation-tool-60', log_file='app.log', level=logging.INFO):
    """Configures a rotating file logger for the application."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers if function is called multiple times
    if not logger.handlers:
        # Ensure directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Rotation: 5MB per file, keep 3 backup files
        handler = RotatingFileHandler(
            log_file, maxBytes=5*1024*1024, backupCount=3
        )
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Add console output as well for visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Initialize global logger instance
logger = setup_logger()