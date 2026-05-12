from dataclasses import dataclass
from uuid import UUID

@dataclass
class UserDTO:
    id: UUID
    name: str
    email: str

@dataclass
class TokenDTO:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"