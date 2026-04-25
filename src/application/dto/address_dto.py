from dataclasses import dataclass
from uuid import UUID

@dataclass
class AddressDTO:
    id: UUID
    customer_id: UUID
    street: str
    city: str
    state: str
    zip_code: str