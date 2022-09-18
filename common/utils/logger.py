import logging


def getLogger(logger_name=""):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    return logger
