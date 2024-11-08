# application/repositories/database_repository.py
import sqlite3
from application.domain.interfaces.repositories.repositories import IDatabaseRepository
from typing import List, Dict

class DatabaseRepository(IDatabaseRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def get_tables(self) -> Dict[str, List[Dict[str, str]]]:
        connection = self._connect()
        cursor = connection.cursor()

        tables_info = {}

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            columns_info = [{"column_name": column[1]} for column in columns]
            tables_info[table_name] = columns_info

        connection.close()
        return tables_info

    def execute_query(self, query: str) -> List[Dict]:
        connection = None
        cursor = None
        result = []

        try:
            # Connect to the database and create a cursor
            connection = self._connect()
            cursor = connection.cursor()

            # Execute the query
            cursor.execute(query)
            
            # Check if the query returns data
            if cursor.description:
                result = cursor.fetchall()
            else:
                # Commit if the command is a non-SELECT operation
                connection.commit()
                result = [{"error": "Operation executed successfully."}]

        except Exception as e:
            # Log the error message for debugging
            print(f"Error executing query: {e}")
            result = [{"error": str(e)}]
        
        finally:
            # Ensure the cursor and connection are properly closed
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()

        return result

    def get_table_details(self, table: str) -> List[Dict]:
        connection = self._connect()
        cursor = connection.cursor()

        cursor.execute(f"PRAGMA table_info({table});")
        result = cursor.fetchall()
        connection.close()

        return result