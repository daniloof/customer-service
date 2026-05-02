from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from uuid import UUID
from src.infrastructure.db.dependencies import get_db
from src.adapters.outbound.db.customer_repository_impl import CustomerRepositoryImpl
from src.adapters.outbound.db.address_repository_impl import AddressRepositoryImpl
from src.application.services.customer_service import CustomerService
from src.application.services.customer_aggregate_service import CustomerAggregateService
from src.adapters.inbound.rest.schemas import ( CustomerResponse,
                                                CustomerCreateRequest,
                                                AddressResponse,
                                                CustomerAddressCreateRequest)
from src.domain.exceptions import EmailAlreadyExistsError
from src.infrastructure.db.unit_of_work import UnitOfWork

router = APIRouter()

@router.post("/customers", response_model=CustomerResponse, summary="Create a new customer")
def create_customer_route(
    data: CustomerCreateRequest,
    db: Session = Depends(get_db)
):
    service = CustomerService(
        CustomerRepositoryImpl(db)
    )

    try:
        with UnitOfWork(db):
            result = service.create_customer(data.name, data.email)

        return CustomerResponse.model_validate(result)

    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

@router.get("/customers", response_model=list[CustomerResponse], summary="List all customers")
def list_customer_route(db:Session = Depends(get_db)):
    service = CustomerService(CustomerRepositoryImpl(db))
    customers = service.list_customer()

    return [CustomerResponse.model_validate(c) for c in customers]

@router.post("/customers/{customer_id}/address",
             summary="Add an address to a customer",response_model=AddressResponse)
def add_address(customer_id: UUID, data: CustomerAddressCreateRequest, db: Session = Depends(get_db)):
    customer_repository = CustomerRepositoryImpl(db)
    address_repository = AddressRepositoryImpl(db)
    service = CustomerAggregateService(customer_repository, address_repository)

    with UnitOfWork(db):

        result = service.add_address_to_customer(
            customer_id,
            data.street,
            data.city,
            data.state,
            data.zip_code
        )

    return AddressResponse.model_validate(result)