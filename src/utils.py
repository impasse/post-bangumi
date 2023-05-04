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


async def read_log_file(file_path: str, request: Request):
    async with aiofiles.open(file_path, 'r') as f:
        while not await request.is_disconnected():
            line = await f.readline()
            if not line:
                await asyncio.sleep(1)
            else:
                yield line
