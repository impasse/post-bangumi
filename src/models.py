from pydantic import BaseModel


class PostDownloadModel(BaseModel):
    category: str
    save_path: str
    torrent_id: str

class ExtractBangumiModel(BaseModel):
    title: str

class ExtractEpisodeModel(BaseModel):
    title: str
