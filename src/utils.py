from loguru import logger
import os


def mkdirp(path):
    try:
        os.umask(22)
        os.makedirs(path)
    except FileExistsError:
        pass
    except OSError as e:
        logger.error("mkdirp error", e)

