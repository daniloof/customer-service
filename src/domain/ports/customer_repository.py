from abc import ABC, abstractmethod
from typing import List

class CustomerRepository(ABC):
    @abstractmethod
    def create(self, name: str, email: str):
        pass

    @abstractmethod
    def list(self) -> List:
        pass

    @abstractmethod
    def get_by_id(self, customer_id):
        pass

    @abstractmethod
    def get_by_email(self, email: str):  # ← adicionado
        pass