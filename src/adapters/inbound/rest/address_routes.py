from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.infrastructure.db.dependencies import get_db
from src.adapters.outbound.db.address_repository_impl import AddressRepositoryImpl
from src.application.services.address_service import AddressService
from src.adapters.inbound.rest.schemas import AddressCreateRequest, AddressResponse

router = APIRouter()

@router.post("/addresses", response_model=AddressResponse,
             summary="Create a new address for a customer")
def create_address(data: AddressCreateRequest, db: Session = Depends(get_db)):
    repository = AddressRepositoryImpl(db)
    service = AddressService(repository)
    result = service.create_address(
        customer_id=data.customer_id,
        street=data.street,
        city=data.city,
        state=data.state,
        zip_code=data.zip_code
    )
    return AddressResponse.model_validate(result)

@router.get("/customers/{customer_id}/addresses", response_model=list[AddressResponse],
             summary="List addresses for a customer")
def list_addresses(customer_id: str, db: Session = Depends(get_db)):
    repository = AddressRepositoryImpl(db)
    service = AddressService(repository)
    results = service.list_addresses_by_customer(customer_id)
    return [AddressResponse.model_validate(r) for r in results]