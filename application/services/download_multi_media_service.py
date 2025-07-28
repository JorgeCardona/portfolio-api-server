from application.domain.entities.models.download import DownloadRequest
from models.download_config import DownloadConfig
from usecases.multi_media_usecase import DownloadMultiMediaUseCase

class DownloadMultiMediaService:
    def handle(self, request: DownloadRequest):
        config = DownloadConfig(
            url=request.url,
            format=request.format,
            output_dir="./downloads",
            subtitle_langs=request.subtitle_langs,
            trim_start=request.trim_start,
            trim_end=request.trim_end,
            include_thumbnail=request.include_thumbnail
        )

        usecase = DownloadMultiMediaUseCase(config)
        video = usecase.execute()

        return {
            "video_title": video.title,
            "zip_path": f"{video.output_folder}.zip"
        }
