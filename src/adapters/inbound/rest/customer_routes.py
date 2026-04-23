from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from src.infrastructure.db.dependencies import get_db
from src.adapters.outbound.db.customer_repository_impl import CustomerRepositoryImpl
from src.application.services.customer_service import CustomerService
from src.adapters.inbound.rest.schemas import CustomerResponse, CustomerCreateRequest
from src.domain.exceptions import EmailAlreadyExistsError

router = APIRouter()

@router.post("/customers", response_model=CustomerResponse)
def create_customer_route(data: CustomerCreateRequest,
                          db: Session = Depends(get_db)):
    service = CustomerService(CustomerRepositoryImpl(db))
    
    try:
        result = service.create_customer(data.name, data.email)

        return CustomerResponse.model_validate(result)
    
    except EmailAlreadyExistsError:
        raise HTTPException(status_code=409,detail=str("Email already exists"))

@router.get("/customers", response_model=list[CustomerResponse])
def list_customer_route(db:Session = Depends(get_db)):
    service = CustomerService(CustomerRepositoryImpl(db))
    customers = service.list_customer()

    return [CustomerResponse.model_validate(c) for c in customers]