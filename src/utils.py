from loguru import logger
import os

def mkdirp(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    except OSError as e:
        logger.error("mkdirp error", e)
