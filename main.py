from src import extractor
from src.models import PostDownloadModel
from src.info import Mikan
from src.utils import mkdirp, read_log_file
from fastapi import FastAPI, Body, Request, Response
from fastapi.responses import HTMLResponse, StreamingResponse
from loguru import logger
import os
import re
import uvicorn

app = FastAPI()

log_path = os.getenv("POST_BANGUMI_LOG_PATH", "stdout.log")
base_path = os.getenv('POST_BANGUMI_BASE_PATH', "/mnt")
category_filter = re.compile(os.getenv('POST_BANGUMI_CATEGORY_FILTER', 'Bangumi'))

logger.add(log_path, backtrace=True, diagnose=True)


@app.get('/log')
def read_log(request: Request, response: Response):
    if os.path.exists(log_path):
        response.headers["Content-Type"] = "text/plain; charset=utf-8"
        return StreamingResponse(read_log_file(log_path, request))
    else:
        return HTMLResponse('Log not exists')


@app.post('/api/post_download')
@logger.catch
def post_download(body: PostDownloadModel = Body()):
    logger.info('收到完成通知 {}', body)
    if not category_filter.fullmatch(body.category):
        return {'error': 'category not match'}
    if os.path.isdir(body.save_path):
        return {'error': 'only independent video files are supported'}
    mikan_info = Mikan.get_info_by_torrent_id(body.torrent_id)
    logger.info('mikan info {}', mikan_info)
    search_title = ':'.join([mikan_info['title'], mikan_info['episode-title']])
    episode_info = extractor.extract(search_title)
    logger.info('episode info {}', episode_info)
    title = episode_info.get('title') or episode_info.get['title_japanese'] or episode_info.get['title_english']
    season = str(episode_info['season'])
    episode = str(episode_info['episode_number'])
    ext = os.path.splitext(body.save_path)[1]
    link_dir = os.path.join(base_path, title, f'Season {season}')
    mkdirp(link_dir)
    link_path = os.path.join(link_dir, f"{title} S{season.rjust(2, '0')}E{episode.rjust(2, '0')}{ext}")
    if not os.path.exists(link_path):
        os.link(body.save_path, link_path)
        logger.info(f'Link "{body.save_path}" to "{link_path}"')
    else:
        logger.info(f'Link "{link_path}" already exists')
    return {'error': '', 'save_path': body.save_path, 'link_path': link_path}


@app.post('/api/extract_bangumi')
def extract_bangumi(body: dict = Body()):
    file_name = body['file_name']
    return extractor.extract(file_name)


@app.get('/health')
def health():
    return 'healthy'


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')
