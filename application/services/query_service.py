# application/services/dependency_injection.py
from application.domain.interfaces.repositories.database_repository import DatabaseRepository
from application.usecases.query_usecase import QueryUseCase

def create_query_usecase(db_path: str) -> QueryUseCase:
    db_repo = DatabaseRepository(db_path)
    return QueryUseCase(db_repo)
