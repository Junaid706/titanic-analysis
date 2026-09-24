"""Logging setup for Titanic Analysis."""
import logging
import sys
from pathlib import Path
from typing import Optional

from .config import get_config


def setup_logging(name: str = "titanic_analysis", config_path: Optional[str] = None) -> logging.Logger:
    """Setup and return configured logger."""
    config = get_config(config_path)
    log_config = config.get_section("logging")

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_config.get("level", "INFO")))

    # Clear existing handlers
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_config.get("level", "INFO")))
    formatter = logging.Formatter(log_config.get("format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    log_file = log_config.get("file")
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(getattr(logging, log_config.get("level", "INFO")))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger