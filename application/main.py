# application/main.py
# uvicorn application.main:app --reload
# uvicorn application.main:app --host 0.0.0.0 --port 8000 --reload

from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from application.services.query_service import create_query_usecase
from application.domain.entities.models.query import Query as Query_Model
from application.configuration.db_path import DB_PATH
from application.configuration.cors import CORS_CONFIG
from application.services.password_service import PasswordService
from application.domain.entities.models.password import PasswordRequest, PasswordResponse
from application.domain.entities.models.download_multi_media import DownloadMultiMediaRequest, DownloadMultiMediaResponse
from application.services.download_multi_media_service import DownloadMultiMediaService
from fastapi.responses import FileResponse
import os
import threading
from fastapi import Query

app = FastAPI()

query_usecase = create_query_usecase(DB_PATH)
# Create an instance of PasswordService
password_service = PasswordService()
    
app.add_middleware(
    CORSMiddleware,
    **CORS_CONFIG
)

EXPORT_DIR = './exports'

@app.get("/get-multimedia-file")
async def get_multimedia_file(
    url: str = Query(..., description="Website video URL to download"),
    format: str = Query(..., description="Format must be 'mp3', 'mp4', or 'original'"),
    trim_start: str = None,
    trim_end: str = None,
    include_thumbnail: bool = True,
    subtitle_langs: List[str] = ["en", "es"],
    export_dir: str = EXPORT_DIR
):
    try:
        # 1. Create file via service
        request_data = DownloadMultiMediaRequest(
            url=url,
            format=format,
            trim_start=trim_start,
            trim_end=trim_end,
            include_thumbnail=include_thumbnail,
            subtitle_langs=subtitle_langs
        )
        service = DownloadMultiMediaService()
        result = service.handle(request_data)

        filename = result["filename"]
        zip_path = os.path.join(export_dir, filename)

        # 2. Schedule auto-delete in 30 min
        def delete_file_later(path):
            if os.path.exists(path):
                os.remove(path)
                print(f"🗑️ Auto-deleted: {path}")

        threading.Timer(1800, delete_file_later, args=[zip_path]).start()

        # 3. Serve file directly
        if not os.path.exists(zip_path):
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(zip_path, media_type="application/zip", filename=filename)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-multimedia-file", response_model=DownloadMultiMediaResponse)
async def download_video(request: DownloadMultiMediaRequest):
    try:
        download_service = DownloadMultiMediaService()
        result = download_service.handle(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download-multimedia-file")
def download_file(filename: str, export_dir: str = EXPORT_DIR):
    filepath = os.path.join(export_dir, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath, media_type="application/zip", filename=filename)

@app.delete("/delete-multimedia-file")
def delete_file(filename: str, export_dir: str = EXPORT_DIR):
    filepath = os.path.join(export_dir, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    
    os.remove(filepath)
    return {"detail": f"{filename} deleted successfully."}

@app.get("/tables", response_model=Dict[str, List[Dict[str, str]]])
def get_tables():
    try:
        return query_usecase.get_tables()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def execute_query(query: Query_Model):
    try:
        result = query_usecase.execute_query(query.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/generate-password", response_model=PasswordResponse)
async def generate_password(request: PasswordRequest):
    try:
        # Call the service layer to generate the password
        response = password_service.generate_password(request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))