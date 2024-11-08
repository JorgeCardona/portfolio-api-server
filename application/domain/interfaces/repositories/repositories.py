# application/domain/interfaces/repositories.py

from abc import ABC, abstractmethod
from typing import List, Dict

class IDatabaseRepository(ABC):
    @abstractmethod
    def get_tables(self) -> Dict[str, List[Dict[str, str]]]:
        pass

    @abstractmethod
    def execute_query(self, query: str) -> List[Dict]:
        pass

    @abstractmethod
    def get_table_details(self, table: str) -> List[Dict]:
        pass