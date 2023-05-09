from bs4 import BeautifulSoup
from collections import namedtuple
import requests

EpisodeInfo = namedtuple('EpisodeInfo', ['bangumi_title', 'episode_title'])


class Mikan:
    @staticmethod
    def get_info_by_torrent_id(torrent_id: str):
        info_url = f'https://mikanani.me/Home/Episode/{torrent_id}'
        html = requests.get(info_url).text
        doc = BeautifulSoup(html, features="html.parser")
        title = doc.select_one('.bangumi-title').text.strip()
        episode_title = doc.select_one('.episode-title').text.strip()

        return EpisodeInfo(bangumi_title=title, episode_title=episode_title)
