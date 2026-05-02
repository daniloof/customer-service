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