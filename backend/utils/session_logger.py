import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

LOG_DIR = "logging"
SESSION_DIR = os.path.join(LOG_DIR, "sessions")
os.makedirs(LOG_DIR, exist_ok=True)

_LOGGERS = {}  # cache to avoid duplicate handlers


def get_session_logger(session_id: str) -> logging.Logger:
    """
    Returns a logger dedicated to a single session.
    One file per session, reused across requests.
    """
    if session_id in _LOGGERS:
        return _LOGGERS[session_id]

    logger_name = f"pharmacy-agent.{session_id}"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    timestamp = datetime.now().strftime("%Y-%m-%d")

    log_file = os.path.join(
        SESSION_DIR,
        f"session-{timestamp}-{session_id}.log"
    )

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)

    _LOGGERS[session_id] = logger
    return logger
