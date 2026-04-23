from uuid import UUID

class Customer:
    def __init__(self, id: UUID, name: str, email: str):
        if not name:
            raise ValueError("Name is required")

        self.id = id
        self.name = name
        self.email = email