# application/usecases/query_usecase.py
from typing import Dict, List
from ..domain.interfaces.repositories.database_repository import DatabaseRepository
import re

class QueryUseCase:
    def __init__(self, db_repo: DatabaseRepository):
        self.db_repo = db_repo

    def get_tables(self) -> Dict[str, List[Dict[str, str]]]:
        return self.db_repo.get_tables()

    def execute_query(self, query: str) -> Dict:
        result = self.db_repo.execute_query(query)
        table_names = self.extract_table_names(query)
        table_columns_details = {table_name: self.db_repo.get_table_details(table_name) for table_name in table_names}
        return {"data": result, "table_columns_details": table_columns_details}

    def extract_table_names(self, query: str) -> List[str]:
        # Regular expression to get all table names in FROM and JOIN clauses
        tables = re.findall(r'FROM\s+([a-zA-Z0-9_]+)|JOIN\s+([a-zA-Z0-9_]+)', query, re.IGNORECASE)
        table_names = [table[0] if table[0] else table[1] for table in tables]
        return table_names if table_names else ["Unknown Tables"]