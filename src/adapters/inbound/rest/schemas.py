from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

class CustomerCreateRequest(BaseModel):
    name: str
    email: EmailStr

class CustomerResponse(BaseModel):
    id: UUID
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)