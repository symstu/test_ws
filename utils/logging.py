import logging
import logging.config


logging.config.fileConfig('logging.ini')


def get_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    return logger
