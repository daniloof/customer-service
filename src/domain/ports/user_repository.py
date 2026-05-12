from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def get_by_google_id(self, google_id: str):
        pass

    @abstractmethod
    def get_by_email(self, email: str):
        pass

    @abstractmethod
    def create(self, google_id: str, name: str, email: str):
        pass