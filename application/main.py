# application/main.py
# uvicorn application.main:app --reload

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.query_service import create_query_usecase  # Ruta relativa
from domain.entities.models.query import Query  # Ruta relativa
from configuration.db_path import DB_PATH  # Ruta relativa
from configuration.cors import CORS_CONFIG  # Ruta relativa
from typing import Dict, List

app = FastAPI()

query_usecase = create_query_usecase(DB_PATH)

app.add_middleware(
    CORSMiddleware,
    **CORS_CONFIG
)

@app.get("/tables", response_model=Dict[str, List[Dict[str, str]]])
def get_tables():
    try:
        return query_usecase.get_tables()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def execute_query(query: Query):
    try:
        result = query_usecase.execute_query(query.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))