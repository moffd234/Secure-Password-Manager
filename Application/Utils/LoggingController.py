import inspect
import logging
import os
from logging import Formatter, FileHandler

BASE_DIR = "../../Application"
PARENT_DIR = os.path.join(BASE_DIR, "logs")

def setup_logging() -> None:
    """
    Configures application-wide logging.

    Sets up the logs directory, file handler with formatting,
    and attaches it to the root logger. Logs will be written to 'logs/app.log'.
    """
    os.makedirs(PARENT_DIR, exist_ok=True)

    log_file = os.path.join(PARENT_DIR, "app.log")
    formatter = Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    file_handler = FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

def log_error_and_method(error: Exception) -> None:
    method_name = inspect.stack()[1].function
    logging.warning(f"{type(error).__name__} occurred in {method_name}: {error}")
