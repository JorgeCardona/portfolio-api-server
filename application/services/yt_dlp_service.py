import os
import re
import yt_dlp
from entities.models.multi_media_download_config import MultiMediaDownloadConfig
from entities.models.multi_media import MultiMedia

class YtDlpService:
    def __init__(self, config: MultiMediaDownloadConfig):
        self.config = config

    def sanitize(self, name: str) -> str:
        return re.sub(r'[\\/*?:"<>|]', "", name)

    def download(self) -> MultiMedia:
        os.makedirs(self.config.output_dir, exist_ok=True)
        ydl_opts = {
            'quiet': False,
            'noplaylist': True,
            'ignoreerrors': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': self.config.subtitle_langs or [],
            'writethumbnail': self.config.include_thumbnail,
            'write_all_thumbnails': False,
            'postprocessors': [],
            'format': 'best'
        }

        if self.config.format == "mp3":
            ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio/best'
        elif self.config.format == "mp4":
            ydl_opts['format'] = 'bestMultiMedia[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
            ydl_opts['merge_output_format'] = 'mp4'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.config.url, download=False)
            title = self.sanitize(info.get("title", "MultiMedia"))
            folder = os.path.join(self.config.output_dir, title)
            os.makedirs(folder, exist_ok=True)

            ydl_opts['outtmpl'] = os.path.join(folder, "%(title)s.%(ext)s")
            ydl.params.update(ydl_opts)
            ydl.download([self.config.url])

            downloaded_file = os.path.join(folder, f"{title}.{info['ext']}")
            return MultiMedia(title=title, downloaded_path=downloaded_file, output_folder=folder)
