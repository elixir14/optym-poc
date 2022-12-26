import logging
import os
import sys

from loguru import logger


LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        from optym_poc.main import request_id_contextvar
        message = f"Request ID:{request_id_contextvar.get()}, Message: {record.getMessage()}"
        logger.opt(depth=depth, exception=record.exc_info).log(level, message)


def setup_logging(log_level="DEBUG"):
    # intercept everything at the root logger

    logging.root.handlers = [InterceptHandler()]
    log_level = logging.getLevelName(log_level.upper())
    logging.root.setLevel(log_level)

    # remove every other logger's handlers
    # and propagate to root logger

    logging.getLogger("opytm_poc").handlers = []
    logging.getLogger("opytm_poc").propagate = True

    # for name in logging.root.manager.loggerDict.keys():
    #     logging.getLogger(name).handlers = []
    #     logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])

