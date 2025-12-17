import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

LOG_DIR = "logging"
WORKFLOW_DIR = os.path.join(LOG_DIR, "workflow")
os.makedirs(WORKFLOW_DIR, exist_ok=True)

_LOGGERS: dict[str, logging.Logger] = {}  # one logger per user_id


def get_workflow_logger(user_id: str | None) -> logging.Logger:
    """
    Returns a workflow logger scoped per user_id.
    One directory per user, one rotating log file per day.
    """
    user_id = user_id or "anonymous"
    logger_name = f"pharmacy-workflow.{user_id}"

    if logger_name in _LOGGERS:
        return _LOGGERS[logger_name]

    # ---- User directory ----
    user_dir = os.path.join(WORKFLOW_DIR, f"user_{user_id}")
    os.makedirs(user_dir, exist_ok=True)

    # ---- Logger ----
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # ---- Log file (daily) ----
    timestamp = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(
        user_dir,
        f"workflow-{timestamp}.log"
    )

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=5,
        encoding="utf-8",
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    logger.addHandler(handler)

    _LOGGERS[logger_name] = logger
    return logger
