from abc import ABC, abstractmethod
from typing import List

class CustomerRepository (ABC):
    @abstractmethod
    def create(self, name:str, email:str):
        pass

    @abstractmethod
    def list(self) -> List:
        pass