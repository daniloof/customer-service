from __future__ import annotations
from uuid import UUID
from typing import List
from .address import Address
from src.domain.exceptions import (RequiredFieldError, InvalidFieldError)

class Customer:
    def __init__(self, id: UUID, name: str, email: str, addresses: List[Address] | None = None):
        if not name or not name.strip():
            raise RequiredFieldError("name")

        self.id = id
        self.name = name.strip()
        self.email = email
        self.addresses = addresses or []

    def add_address(self, address: Address):
        if len(self.addresses) >= 3:
            raise ValueError("A customer can have a maximum of 3 addresses")
        self.addresses.append(address)