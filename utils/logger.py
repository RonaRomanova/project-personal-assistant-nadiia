import json
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

MAX_BYTES = 1024 * 1024  # 1MB
BACKUP_COUNT = 5
LOGGER_NAME = "nadiia"
LOG_FILE = "nadiia.log"


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record, ensure_ascii=False)


def setup_logger(name=LOGGER_NAME, log_file=LOG_FILE, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = RotatingFileHandler(
            log_file,
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT,
            encoding="utf-8",
        )
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    return logger


def get_logger(name="nadiia"):
    return logging.getLogger(name)
