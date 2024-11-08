# application/services/dependency_injection.py
from domain.interfaces.repositories.database_repository import DatabaseRepository
from usecases.query_usecase import QueryUseCase

def create_query_usecase(db_path: str) -> QueryUseCase:
    db_repo = DatabaseRepository(db_path)
    return QueryUseCase(db_repo)
