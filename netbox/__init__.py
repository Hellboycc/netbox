import logging
import os

from .version import __version__

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
LOG_DIR = os.path.join(os.path.dirname(BASE_DIR), "logs")


def get_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """Customization logger.

    Args:
        name (str): name of logger
        level (str, optional): log level. Defaults to logging.DEBUG.

    Returns:
        Object of Logger.
    """
    logger = logging.getLogger(name=name)
    logger.setLevel(level=level)
    logger.propagate = False
    # define log formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(filename)s - func:%(funcName)s - %(lineno)d - [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # create stream handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level=logging.WARNING)
    console_handler.setFormatter(fmt=formatter)
    logger.addHandler(console_handler)
    # validation file path exists or not
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    # create file handler
    file_handler = logging.FileHandler(
        filename=os.path.join(LOG_DIR, "test.log"), mode="a", encoding="utf-8"
    )
    file_handler.setLevel(level=logging.DEBUG)
    file_handler.setFormatter(fmt=formatter)
    logger.addHandler(file_handler)

    return logger


logger = get_logger(__name__)
