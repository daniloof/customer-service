from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.infrastructure.db.dependencies import get_db
from src.adapters.outbound.db.address_repository_impl import AddressRepositoryImpl
from src.application.services.address_service import AddressService
from src.adapters.inbound.rest.schemas import AddressCreateRequest, AddressResponse

router = APIRouter()

@router.get("/customers/{customer_id}/addresses", response_model=list[AddressResponse],
             summary="List addresses for a customer")
def list_addresses(customer_id: uuid.UUID, db: Session = Depends(get_db)):
    repository = AddressRepositoryImpl(db)
    service = AddressService(repository)
    results = service.list_addresses_by_customer(customer_id)
    return [AddressResponse.model_validate(r) for r in results]