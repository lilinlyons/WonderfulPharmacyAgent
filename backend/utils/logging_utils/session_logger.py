import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

LOG_DIR = "logging"
SESSION_DIR = os.path.join(LOG_DIR, "sessions")
os.makedirs(SESSION_DIR, exist_ok=True)

_LOGGERS: dict[str, logging.Logger] = {}  # cache per (user_id, session_id)


def get_session_logger(session_id: str, user_id: str | None = None) -> logging.Logger:
    """
    Returns a logger dedicated to a single user session.
    Logs are separated by user_id and session_id.
    """
    user_id = user_id or "anonymous"
    cache_key = f"{user_id}:{session_id}"

    if cache_key in _LOGGERS:
        return _LOGGERS[cache_key]

    # ---- Directories ----
    user_dir = os.path.join(SESSION_DIR, f"user_{user_id}")
    session_dir = os.path.join(user_dir, f"session_{session_id}")
    os.makedirs(session_dir, exist_ok=True)

    # ---- Logger ----
    logger_name = f"pharmacy-session.{user_id}.{session_id}"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # ---- Log file (daily) ----
    timestamp = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(
        session_dir,
        f"session-{timestamp}.log"
    )

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding="utf-8",
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    logger.addHandler(handler)

    _LOGGERS[cache_key] = logger
    return logger
