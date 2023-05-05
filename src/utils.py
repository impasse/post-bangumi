from loguru import logger
from fastapi import Request
import aiofiles
import os
import asyncio

def mkdirp(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass
    except OSError as e:
        logger.error("mkdirp error", e)
