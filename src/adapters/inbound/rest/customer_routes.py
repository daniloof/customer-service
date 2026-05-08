from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from src.adapters.outbound.db.dependencies import (
    get_db,
    get_customer_service,
    get_customer_aggregate_service
)
from src.adapters.outbound.db.unit_of_work import UnitOfWork
from src.application.services.customer_service import CustomerService
from src.application.services.customer_aggregate_service import CustomerAggregateService
from src.adapters.inbound.rest.schemas import (
    CustomerResponse,
    CustomerCreateRequest,
    AddressResponse,
    CustomerAddressCreateRequest,
    CustomerDetailResponse,
    CustomerUpdateRequest
)

router = APIRouter()

@router.post("/customers", response_model=CustomerResponse, status_code=201)  # ← 200 para 201
def create_customer_route(
    data: CustomerCreateRequest,
    service: CustomerService = Depends(get_customer_service),
    db: Session = Depends(get_db)
):
    with UnitOfWork(db):
        result = service.create_customer(data.name, data.email)
    return CustomerResponse.model_validate(result)


@router.get("/customers", response_model=list[CustomerResponse])
def list_customer_route(
    service: CustomerService = Depends(get_customer_service)
):
    customers = service.list_customer()
    return [CustomerResponse.model_validate(c) for c in customers]


@router.post("/customers/{customer_id}/addresses", response_model=AddressResponse, status_code=201)  # ← 200 para 201
def add_address(
    customer_id: UUID,
    data: CustomerAddressCreateRequest,
    service: CustomerAggregateService = Depends(get_customer_aggregate_service),
    db: Session = Depends(get_db)
):
    with UnitOfWork(db):
        result = service.add_address_to_customer(
            customer_id, data.street, data.city, data.state, data.zip_code
        )
    return AddressResponse.model_validate(result)


@router.get("/customers/{customer_id}", response_model=CustomerDetailResponse)
def get_customer_route(
    customer_id: UUID,
    service: CustomerService = Depends(get_customer_service)
):
    customer = service.get_customer(customer_id)
    return CustomerDetailResponse.model_validate(customer)

@router.put("/customers/{customer_id}", response_model=CustomerResponse)  # ← novo
def update_customer_route(
    customer_id: UUID,
    data: CustomerUpdateRequest,
    service: CustomerService = Depends(get_customer_service),
    db: Session = Depends(get_db)
):
    with UnitOfWork(db):
        result = service.update_customer(customer_id, data.name, data.email)
    return CustomerResponse.model_validate(result)

@router.delete("/customers/{customer_id}", status_code=204)  # ← novo
def delete_customer_route(
    customer_id: UUID,
    service: CustomerService = Depends(get_customer_service),
    db: Session = Depends(get_db)
):
    with UnitOfWork(db):
        service.delete_customer(customer_id)

@router.delete("/customers/{customer_id}/addresses/{address_id}", status_code=204)  # ← novo
def delete_address_route(
    customer_id: UUID,
    address_id: UUID,
    service: CustomerAggregateService = Depends(get_customer_aggregate_service),
    db: Session = Depends(get_db)
):
    with UnitOfWork(db):
        service.delete_address(customer_id, address_id)