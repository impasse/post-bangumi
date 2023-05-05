from src import extractor
from src.models import PostDownloadModel, ExtractBangumiModel, ExtractEpisodeModel
from src.utils import mkdirp, get_dest_path
from fastapi import FastAPI, Body, WebSocket
from fastapi.staticfiles import StaticFiles
from loguru import logger
import os
import re
import uvicorn
import aiofiles
import asyncio

app = FastAPI()

log_path = os.getenv("POST_BANGUMI_LOG_PATH", "stdout.log")
base_path = os.getenv('POST_BANGUMI_BASE_PATH', "/mnt")
category_filter = re.compile(os.getenv('POST_BANGUMI_CATEGORY_FILTER', 'Bangumi'))

logger.add(log_path, backtrace=True, diagnose=True, colorize=True)

app.mount(
    '/log',
    StaticFiles(directory="ui", html=True),
    name='log'
)


@app.websocket('/api/log')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async with aiofiles.open(log_path, 'r') as f:
        while True:
            line = await f.readline()
            if not line:
                await asyncio.sleep(1)
            else:
                await websocket.send_text(line)


@app.post('/api/post_download')
@logger.catch
def post_download(body: PostDownloadModel = Body()):
    logger.info('收到完成通知 {}', body)
    if not category_filter.fullmatch(body.category):
        return {'error': 'category not match'}
    if os.path.isdir(body.save_path):
        return {'error': 'only independent video files are supported'}
    ext = os.path.splitext(body.save_path)[1]
    dest_path = get_dest_path(body.torrent_id)
    logger.info('dest_path = {}', dest_path)
    link_dir = os.path.join(base_path, dest_path.title, f'Season {dest_path.season}')
    mkdirp(link_dir)
    link_path = os.path.join(link_dir, f"{dest_path.title} S{dest_path.season}E{dest_path.episode}{ext}")
    if not os.path.exists(link_path):
        os.link(body.save_path, link_path)
        logger.info(f'Link "{body.save_path}" to "{link_path}"')
    else:
        logger.info(f'Link "{link_path}" already exists')
    return {'error': '', 'save_path': body.save_path, 'link_path': link_path}


@app.get('/api/get_dest_path')
def get_dest_path_api(torrent_id: str):
    return get_dest_path(torrent_id)


@app.post('/api/extract_bangumi')
def extract_bangumi(body: ExtractBangumiModel = Body()):
    info = extractor.extract_bangumi(body.title)
    return info


@app.post('/api/extract_episode')
def extract_bangumi(body: ExtractEpisodeModel = Body()):
    info = extractor.extract_episode(body.title)
    return info


@app.get('/health')
def health():
    return 'healthy'


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
