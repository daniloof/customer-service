from dataclasses import dataclass
from uuid import UUID

@dataclass
class CustomerDTO:
    id: UUID
    name: str
    email: str