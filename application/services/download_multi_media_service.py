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
            include_thumbnail=request.include_thumbnail,
            http_headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9"
            }  # ✅ Añadido
        )

        usecase = DownloadMultiMediaUseCase(config)
        video = usecase.execute()

        return {
            "video_title": video.title,
            "zip_path": f"{video.output_folder}.zip"
        }
