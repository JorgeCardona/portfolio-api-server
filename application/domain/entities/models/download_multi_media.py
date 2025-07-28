from pydantic import BaseModel
from typing import List, Optional

class DownloadMultiMediaRequest(BaseModel):
    url: str
    format: str = "original"
    subtitle_langs: Optional[List[str]] = None
    trim_start: Optional[str] = None
    trim_end: Optional[str] = None
    include_thumbnail: bool = True

class DownloadMultiMediaResponse(BaseModel):
    video_title: str
    zip_path: str
