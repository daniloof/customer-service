from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

class AddressRepository(ABC):
    @abstractmethod
    def create(self, customer_id: UUID, street: str, city: str, state: str, zip_code: str):
        pass

    @abstractmethod
    def list_by_customer(self, customer_id: UUID) -> List:
        pass