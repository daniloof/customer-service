from pydantic import BaseModel, EmailStr

class CustomerCreateRequest(BaseModel):
    name: str
    email: EmailStr


class CustomerResponse(BaseModel):
    id: str
    name: str
    email: str