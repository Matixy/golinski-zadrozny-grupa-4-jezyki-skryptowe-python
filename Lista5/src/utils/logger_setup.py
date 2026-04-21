import logging
from pathlib import Path
import sys

def filter_errors(record):
    """Allows only for logs at levels weaker tham Error(INFO, WARNING, DEBUG)"""
    return record.levelno < logging.ERROR

def set_logger() -> logging.Logger:
    logger = logging.getLogger(__name__) # create or get a logger with the current module name
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:    # avoid duplicated log messages, 
        log_file = Path("cli_app.log")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter(fmt= "%(asctime)s ; %(levelname)s ; %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        #STDOUT
        stdout_handler = logging.StreamHandler(sys.stdout) #console output (debug, info, warning)
        stdout_handler.setFormatter(formatter)
        stdout_handler.addFilter(filter_errors)
        logger.addHandler(stdout_handler)

        #STDERR
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.ERROR)
        stderr_handler.setFormatter(formatter)
        logger.addHandler(stderr_handler)

    return logger

logger = set_logger() #create a global logger instance