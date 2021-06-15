import logging

def get_logger(name):
    logger = logging.getLogger(name)
    handler = logging.FileHandler('./alert.log', 'a+')
    f = logging.Formatter('%(asctime)s - %(levelname)-10s - %(filename)s - %(funcName)s - %(message)s')
    handler.setFormatter(f)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
