# application/domain/entities/query.py
from pydantic import BaseModel

class Query(BaseModel):
    query: str
