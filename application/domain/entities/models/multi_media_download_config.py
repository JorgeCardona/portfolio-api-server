from dataclasses import dataclass
from typing import List, Optional

@dataclass
class MultiMediaDownloadConfig:
    url: str
    format: str = "original"  # "mp3", "mp4", or "original"
    output_dir: str = "./downloads"
    subtitle_langs: Optional[List[str]] = None
    trim_start: Optional[str] = None  # "HH:MM:SS"
    trim_end: Optional[str] = None    # "HH:MM:SS"
    include_thumbnail: bool = True