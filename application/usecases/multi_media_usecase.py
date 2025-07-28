
from entities.models.multi_media_download_config import MultiMediaDownloadConfig
from services.yt_dlp_service import YtDlpService
from services.ffmpeg_service import FFmpegService
from services.zip_service import ZipService

class DownloadMultiMediaUseCase:
    def __init__(self, config: MultiMediaDownloadConfig):
        self.config = config
        self.ytdlp = YtDlpService(config)
        self.ffmpeg = FFmpegService(config)
        self.zipper = ZipService()

    def execute(self):
        video = self.ytdlp.download()

        if self.config.include_thumbnail:
            self.ffmpeg.convert_webp_to_jpg(video)

        if self.config.format == "mp3":
            self.ffmpeg.trim_and_convert_to_mp3(video)
        elif self.config.format == "mp4":
            self.ffmpeg.trim_mp4(video)

        self.zipper.compress_folder(video.output_folder)
        return video
