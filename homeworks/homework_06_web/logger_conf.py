import logging


def create_logger(loggername='app', filename='logs.log', formatr=('%(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')):
    logger = logging.getLogger(loggername)
    logger.setLevel(logging.INFO)
    file = logging.FileHandler(filename)
    formatter = logging.Formatter(*formatr)
    file.setFormatter(formatter)
    logger.addHandler(file)
    return logger
