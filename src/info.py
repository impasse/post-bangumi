from bs4 import BeautifulSoup
import requests

class Mikan:
    @staticmethod
    def get_info_by_torrent_id(torrent_id: str):
        info_url = f'https://mikanani.me/Home/Episode/{torrent_id}'
        html = requests.get(info_url).text
        doc = BeautifulSoup(html, features="html.parser")
        title = doc.select_one('.bangumi-title').text
        episode_title = doc.select_one('.episode-title').text

        return {
            'title': title,
            'episode-title': episode_title
        }
