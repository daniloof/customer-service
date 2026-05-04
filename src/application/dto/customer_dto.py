from dataclasses import dataclass, field
from uuid import UUID
from typing import List
from src.application.dto.address_dto import AddressDTO

@dataclass
class CustomerDTO:
    id: UUID
    name: str
    email: str
    addresses: List[AddressDTO] = field(default_factory=list)