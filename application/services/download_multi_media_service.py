from application.domain.entities.models.download_multi_media import DownloadMultiMediaRequest
from application.domain.entities.models.multi_media_download_config import MultiMediaDownloadConfig
from application.usecases.multi_media_usecase import DownloadMultiMediaUseCase

class DownloadMultiMediaService:
    def handle(self, request: DownloadMultiMediaRequest):
        config = MultiMediaDownloadConfig(
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
