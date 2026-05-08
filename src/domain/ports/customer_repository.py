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
    def get_by_email(self, email: str):
        pass
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
    def get_by_email(self, email: str):
        pass

    @abstractmethod
    def update(self, customer_id, name: str, email: str):  # ← novo
        pass

    @abstractmethod
    def delete(self, customer_id):  # ← novo
        pass