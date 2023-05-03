from pydantic import BaseModel

class PostDownloadModel(BaseModel):
    category: str
    save_path: str
    torrent_id: str
