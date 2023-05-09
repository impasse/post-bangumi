from pydantic import BaseModel


class PostDownloadModel(BaseModel):
    category: str
    save_path: str
    torrent_id: str


class ExtractModel(BaseModel):
    bangumi_title: str
    episode_title: str
