from loguru import logger
from src.info import Mikan
from collections import namedtuple
from src.extractor import extract_bangumi, extract_episode
import os


def mkdirp(path):
    try:
        os.umask(22)
        os.makedirs(path)
    except FileExistsError:
        pass
    except OSError as e:
        logger.error("mkdirp error", e)


DestPath = namedtuple('DestPath', ['title', 'season', 'episode'])


def get_dest_path(torrent_id: str):
    mikan_info = Mikan.get_info_by_torrent_id(torrent_id)
    bangumi_info = extract_bangumi(mikan_info['title'])
    episode_info = extract_episode(mikan_info['episode-title'])
    title = bangumi_info['title']
    season = (bangumi_info['season_number'] and str(bangumi_info['season_number'])) or \
             (episode_info['season'] and str(episode_info['season'])) or \
             bangumi_info['season'] or '1'
    episode = str(episode_info['episode_number'])
    return DestPath(title, season, episode)
