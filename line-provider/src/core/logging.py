import logging
import os

LOG_FILENAME = "line-provider.log"
LOG_FILENAME_ERR = "line-provider_error.log"


def init_logger():
    log_dir = os.path.join(os.path.dirname(__file__), "..", "log")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, LOG_FILENAME)

    log_dir_error = os.path.join(os.path.dirname(__file__), "..", "log")
    if not os.path.exists(log_dir_error):
        os.makedirs(log_dir_error)
    log_file_error = os.path.join(log_dir_error, LOG_FILENAME_ERR)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Console logger
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_format = logging.Formatter("%(asctime)s:%(name)s:%(filename)s:%(funcName)s:%(levelname)s :%(message)s")
    c_handler.setFormatter(c_format)

    # Rotate file handler
    rf_handler = logging.handlers.TimedRotatingFileHandler(log_file, when="midnight", backupCount=5)
    rf_handler.setLevel(logging.WARNING)
    rf_format = logging.Formatter("%(asctime)s:%(name)s:%(filename)s:%(funcName)s:%(levelname)s :%(message)s")
    rf_handler.setFormatter(rf_format)

    # Rotate file handler
    ex_handler = logging.handlers.TimedRotatingFileHandler(log_file_error, when="midnight", backupCount=2)
    ex_handler.setLevel(logging.ERROR)
    ex_format = logging.Formatter("%(asctime)s:%(name)s:%(filename)s:%(funcName)s:%(levelname)s :%(message)s")
    ex_handler.setFormatter(ex_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(ex_handler)
    logger.addHandler(rf_handler)

    logger.info("Logger loaded")
