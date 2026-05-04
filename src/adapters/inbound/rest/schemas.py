from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from uuid import UUID

class CustomerCreateRequest(BaseModel):
    name: str
    email: EmailStr

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name must not be empty")
        return v.strip()


class CustomerResponse(BaseModel):
    id: UUID
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class CustomerAddressCreateRequest(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    
class AddressResponse(BaseModel):
    id: UUID
    customer_id: UUID
    street: str
    city: str
    state: str
    zip_code: str

    model_config = ConfigDict(from_attributes=True)

class CustomerDetailResponse(BaseModel):
    id: UUID
    name: str
    email: str
    addresses: list[AddressResponse]

    model_config = ConfigDict(from_attributes=True)