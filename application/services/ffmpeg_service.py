import os
import subprocess
from application.domain.entities.models.multi_media_download_config import MultiMediaDownloadConfig
from application.domain.entities.models.multi_media import MultiMedia

class FFmpegService:
    def __init__(self, config: MultiMediaDownloadConfig):
        self.config = config

    def trim_and_convert_to_mp3(self, MultiMedia: MultiMedia):
        output = os.path.splitext(MultiMedia.downloaded_path)[0] + "_trimmed.mp3"
        cmd = ["ffmpeg", "-y"]
        if self.config.trim_start:
            cmd += ["-ss", self.config.trim_start]
        cmd += ["-i", MultiMedia.downloaded_path]
        if self.config.trim_end:
            cmd += ["-to", self.config.trim_end]
        cmd += ["-vn", "-acodec", "libmp3lame", "-qscale:a", "5", output]
        subprocess.run(cmd, check=True)
        os.remove(MultiMedia.downloaded_path)
        MultiMedia.downloaded_path = output

    def trim_mp4(self, MultiMedia: MultiMedia):
        output = os.path.splitext(MultiMedia.downloaded_path)[0] + "_trimmed.mp4"
        cmd = ["ffmpeg", "-y"]
        if self.config.trim_start:
            cmd += ["-ss", self.config.trim_start]
        cmd += ["-i", MultiMedia.downloaded_path]
        if self.config.trim_end:
            cmd += ["-to", self.config.trim_end]
        cmd += ["-c", "copy", output]
        subprocess.run(cmd, check=True)
        os.remove(MultiMedia.downloaded_path)
        MultiMedia.downloaded_path = output

    def convert_webp_to_jpg(self, MultiMedia: MultiMedia):
        webp = os.path.splitext(MultiMedia.downloaded_path)[0] + ".webp"
        jpg = os.path.splitext(MultiMedia.downloaded_path)[0] + ".jpg"
        if os.path.exists(webp):
            subprocess.run(["ffmpeg", "-y", "-i", webp, jpg], check=True)
            os.remove(webp)
