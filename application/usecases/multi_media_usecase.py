import os
import subprocess
from yt_dlp import YoutubeDL
from application.domain.entities.models.multi_media_download_config import MultiMediaDownloadConfig
from application.domain.entities.models.multi_media import MultiMedia

class DownloadMultiMediaUseCase:
    def __init__(self, config: MultiMediaDownloadConfig):
        self.config = config

    def execute(self) -> MultiMedia:
        url = self.config.url
        output_dir = self.config.output_dir
        os.makedirs(output_dir, exist_ok=True)

        ydl_opts = {
            "format": self._resolve_format(),
            "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": self.config.subtitle_langs or ["en", "es"],
            "noplaylist": True,
            "quiet": False,
            "merge_output_format": "mp4" if self.config.format == "mp4" else None,
            "writethumbnail": self.config.include_thumbnail,
            "write_all_thumbnails": False,
            "http_headers": self.config.http_headers or {}
        }

        # 1. Descargar el video con yt-dlp
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "video")
            original_ext = info.get("ext", "mp4")

        # 2. Detectar archivos generados
        base_path = os.path.join(output_dir, title)
        downloaded_path = f"{base_path}.{original_ext}"
        thumbnail_path = f"{base_path}.webp"
        subtitles_path_vtt = f"{base_path}.{self.config.subtitle_langs[0]}.vtt"
        trimmed_output = f"{base_path}_trimmed.{self._ext()}"

        # 3. Recortar si es necesario
        if self.config.trim_start or self.config.trim_end:
            cmd = ["ffmpeg", "-y"]
            if self.config.trim_start:
                cmd += ["-ss", self.config.trim_start]
            cmd += ["-i", downloaded_path]
            if self.config.trim_end:
                cmd += ["-to", self.config.trim_end]

            if self.config.format == "mp3":
                cmd += ["-vn", "-acodec", "libmp3lame", "-qscale:a", "5", trimmed_output]
            else:
                cmd += ["-c", "copy", trimmed_output]

            subprocess.run(cmd, check=True)
            os.remove(downloaded_path)
            final_media_path = trimmed_output
        else:
            final_media_path = downloaded_path

        # 4. Convertir thumbnail a .jpg si es necesario
        jpg_thumbnail = thumbnail_path.replace(".webp", ".jpg")
        if os.path.exists(thumbnail_path):
            subprocess.run(["ffmpeg", "-y", "-i", thumbnail_path, jpg_thumbnail], check=True)
            os.remove(thumbnail_path)

        # 5. Crear ZIP con todos los archivos relevantes
        zip_path = f"{base_path}.zip"
        files_to_zip = [final_media_path]

        if os.path.exists(jpg_thumbnail):
            files_to_zip.append(jpg_thumbnail)

        if os.path.exists(subtitles_path_vtt):
            files_to_zip.append(subtitles_path_vtt)

        subprocess.run(["zip", "-j", zip_path] + files_to_zip, check=True)

        # 6. Limpiar archivos sueltos
        for f in files_to_zip:
            if os.path.exists(f):
                os.remove(f)

        return MultiMedia(
            title=title,
            downloaded_path=zip_path,
            output_folder=output_dir
        )

    def _resolve_format(self):
        if self.config.format == "mp3":
            return "bestaudio[ext=m4a]/bestaudio/best"
        elif self.config.format == "mp4":
            return "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]"
        else:
            return "best"

    def _ext(self):
        if self.config.format == "mp3":
            return "mp3"
        elif self.config.format == "mp4":
            return "mp4"
        else:
            return "webm"