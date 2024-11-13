# application/main.py
# uvicorn application.main:app --reload

from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from application.services.query_service import create_query_usecase
from application.domain.entities.models.query import Query
from application.configuration.db_path import DB_PATH
from application.configuration.cors import CORS_CONFIG
from application.services.password_service import PasswordService
from application.domain.entities.models.password import PasswordRequest, PasswordResponse

app = FastAPI()

query_usecase = create_query_usecase(DB_PATH)
# Create an instance of PasswordService
password_service = PasswordService()
    
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
    
@app.post("/generate-password", response_model=PasswordResponse)
async def generate_password(request: PasswordRequest):
    try:
        # Call the service layer to generate the password
        response = password_service.generate_password(request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))