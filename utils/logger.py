import logging
import sys
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler
from pathlib import Path

# Calculate paths relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOG_LEVEL = "INFO" # Default fallback

def setup_logger(name="antigravity", log_file="system.log"):
    """
    Sets up a logger with Rich console handler and file handler.
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Prevent adding handlers multiple times
    if logger.hasHandlers():
        return logger

    # 1. Rich Console Handler (for pretty output)
    console_handler = RichHandler(rich_tracebacks=True, markup=True)
    console_handler.setLevel(LOG_LEVEL)
    console_format = logging.Formatter("%(message)s", datefmt="[%X]")
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # 2. File Handler (Rotating)
    log_path = LOGS_DIR / log_file
    file_handler = RotatingFileHandler(
        log_path, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG) # Always log details to file
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    return logger

# Create the specific loggers
logger = setup_logger()
