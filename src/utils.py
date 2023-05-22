from loguru import logger
import os


def init_user_group():
    if os.getenv("PUID"):
        os.setuid(int(os.getenv("PUID")))
    if os.getenv("PGID"):
        os.setgid(int(os.getenv("PGID")))
    if os.getenv("UMASK"):
        os.umask(int(os.getenv("UMASK")))


def mkdirp(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    except OSError as e:
        logger.error("mkdirp error", e)

