from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from src.infrastructure.db.dependencies import get_db
from src.application.services.customer_service import create_customer
from src.adapters.inbound.rest.schemas import CustomerCreateRequest, CustomerResponse
from src.domain.exceptions import EmailAlreadyExistsError

router = APIRouter()

@router.post("/customers", response_model=CustomerResponse)
def create_customer_route(data: CustomerCreateRequest,
                          db: Session = Depends(get_db)):
    try:
        customer = create_customer(
            db=db,
            name=data.name,
            email=data.email
        )

        return CustomerResponse(
            id=str(customer.id),
            name=customer.name,
            email=customer.email
        )
    except EmailAlreadyExistsError:
        raise HTTPException(status_code=409,detail=str("Email already exists"))

@router.get("/health")
def health():
    return{"status": "OK"}