from src import extractor
from src.models import PostDownloadModel, ExtractModel
from src.utils import mkdirp
from src.info import Mikan
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
    episode_info = Mikan.get_info_by_torrent_id(body.torrent_id)
    info = extractor.extract(episode_info.bangumi_title, episode_info.episode_title)
    link_dir = os.path.join(base_path, info.title, info.season)
    mkdirp(link_dir)
    link_path = os.path.join(link_dir, f'{link_dir}', f'{info.title} {info.episode}{ext}')
    if not os.path.exists(link_path):
        os.link(body.save_path, link_path)
        logger.info(f'Link "{body.save_path}" to "{link_path}"')
    else:
        logger.info(f'Link "{link_path}" already exists')
    return {'error': '', 'save_path': body.save_path, 'link_path': link_path}


@app.post('/api/extract')
def extract(body: ExtractModel = Body()):
    info = extractor.extract(body.bangumi_title, body.episode_title)
    return info


@app.get('/api/extract_bangumi')
def extract_bangumi(torrent_id: str):
    info = Mikan.get_info_by_torrent_id(torrent_id)
    return extractor.extract(info.bangumi_title, info.episode_title)


@app.get('/health')
def health():
    return 'healthy'


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
