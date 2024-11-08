# application/usecases/query_usecase.py
from typing import Dict, List
from application.domain.interfaces.repositories.database_repository import DatabaseRepository
from application.utils.database.db_restrictions import BASE_TABLES, DCL, DDL, DML, TCL
import re

class QueryUseCase:
    def __init__(self, db_repo: DatabaseRepository):
        self.db_repo = db_repo

    def get_tables(self) -> Dict[str, List[Dict[str, str]]]:
        return self.db_repo.get_tables()

    def check_forbidden_statements(self, query: str) -> Dict:
        """Check if the query contains any forbidden combinations of table and statement."""
        query_upper = query.strip().upper()
        
        # Check if any table from BASE_TABLES is present in the query
        table_found = None
        for table in BASE_TABLES:
            if table.upper() in query_upper:
                table_found = table
                break

        # Check if any keyword from DCL, DDL, DML, or TCL is present in the query
        keyword_found = None
        for keyword_list in [DCL, DDL, DML, TCL]:
            for keyword in keyword_list:
                if keyword in query_upper:
                    keyword_found = keyword
                    break
            if keyword_found:
                break
        
        if table_found and keyword_found:
            return {
                "error": f"The combination of statement '{keyword_found}' and table '{table_found.upper()}' is not allowed in this query."
            }
        
        return {}

    def handle_query_result(self, result: List[Dict]) -> Dict:
        """Process the query result to check for errors."""
        for res in result:
            if 'error' in res:
                return {
                    "data": [],
                    "table_columns_details": [],
                    "error": res['error']
                }
        return None

    def extract_table_columns(self, query: str) -> Dict:
        """Extract table names and their column details from the query."""
        table_names = self.extract_table_names(query)
        table_columns_details = {table_name: self.db_repo.get_table_details(table_name) for table_name in table_names}
        return table_columns_details

    def execute_query(self, query: str) -> Dict:
        """Execute the query after checking for forbidden statements and errors."""
        # Check if the query contains forbidden combinations of table and statement
        forbidden_check = self.check_forbidden_statements(query)
        if 'error' in forbidden_check:
            return forbidden_check

        # Execute the query using the repository
        result = self.db_repo.execute_query(query)

        # Handle the query result for any errors
        error_check = self.handle_query_result(result)
        if error_check:
            return error_check

        # Extract table column details if no errors
        table_columns_details = self.extract_table_columns(query)

        return {"data": result, "table_columns_details": table_columns_details}

    def extract_table_names(self, query: str) -> List[str]:
        # Regular expression to get all table names in FROM and JOIN clauses
        tables = re.findall(r'FROM\s+([a-zA-Z0-9_]+)|JOIN\s+([a-zA-Z0-9_]+)', query, re.IGNORECASE)
        table_names = [table[0] if table[0] else table[1] for table in tables]
        return table_names if table_names else ["Unknown Tables"]