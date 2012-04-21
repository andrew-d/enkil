import logging


def getLogger(id, minLevel=logging.DEBUG):
    logger = logging.getLogger(id)
    logger.setLevel(minLevel)

    # Create and attach handler(s)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    # Create and attach formatter
    fmt = logging.Formatter('[%(levelname)1.1s %(asctime)s ' \
                            '%(module)s:%(lineno)d] %(message)s')
    logger.setFormatter(fmt)

    return logger
