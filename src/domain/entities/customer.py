from uuid import UUID
from .address import Address

class Customer:
    def __init__(self, id: UUID, name: str, email: str, addresses: None):
        if not name:
            raise ValueError("Name is required")

        self.id = id
        self.name = name
        self.email = email
        self.addresses = addresses or []
    
    def add_address(self, address: Address):
        if len(self.addresses) >= 3:
            raise ValueError("A customer can have a maximum of 3 addresses")
        self.addresses.append(address)