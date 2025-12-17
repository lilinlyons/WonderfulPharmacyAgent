import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

LOG_DIR = "logging"
WORKFLOW_DIR = os.path.join(LOG_DIR, "workflow")
os.makedirs(LOG_DIR, exist_ok=True)
_LOGGER = None  # singleton

def get_workflow_logger() -> logging.Logger:
    """
    Logger used ONLY inside workflows/.
    Shared across all workflows.
    """
    global _LOGGER
    if _LOGGER:
        return _LOGGER

    logger = logging.getLogger("pharmacy-workflow")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    timestamp = datetime.now().strftime("%Y-%m-%d")

    log_file = os.path.join(
        WORKFLOW_DIR,
        f"workflow-{timestamp}.log"
    )

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    logger.addHandler(handler)

    _LOGGER = logger
    return logger
