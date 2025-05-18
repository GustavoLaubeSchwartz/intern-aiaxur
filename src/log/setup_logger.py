""" This module sets up a logger for the application.
    It configures the logger to log messages to both the console and a file.
    The file handler uses timed rotation to create a new log file at midnight.
    The log messages include timestamps, the filename, the log level, the function name,
    the line number, and the message itself.
    The logger is set to the INFO level, meaning it 
    will capture all messages at this level and above.
    The log file is saved in the "log" directory with the name "log.log".
    The console output is formatted to include the local host name. """

import sys
import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logger():
    """
    Set up a logger for the application."""

    formatter = logging.Formatter(
        "[LOCAL HOST] | "
        "%(asctime)s | "
        "%(filename)s | "
        "%(levelname)s | "
        "%(funcName)s:"
        "%(lineno)d:\t"
        "%(message)s "
    )
    logger = logging.getLogger("meu_projeto")
    logger.setLevel(logging.INFO)

    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para arquivo (com rotação diária)
    file_handler = TimedRotatingFileHandler(
        "src/log/application.log", when="midnight", backupCount=7, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
