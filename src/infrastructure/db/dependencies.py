from sqlalchemy.orm import Session
from fastapi import Depends
from src.infrastructure.db.session import SessionLocal
from src.adapters.outbound.db.customer_repository_impl import CustomerRepositoryImpl
from src.adapters.outbound.db.address_repository_impl import AddressRepositoryImpl
from src.application.services.customer_service import CustomerService
from src.application.services.customer_aggregate_service import CustomerAggregateService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_customer_service(db: Session = Depends(get_db)) -> CustomerService:
    return CustomerService(CustomerRepositoryImpl(db))


def get_customer_aggregate_service(db: Session = Depends(get_db)) -> CustomerAggregateService:
    return CustomerAggregateService(
        CustomerRepositoryImpl(db),
        AddressRepositoryImpl(db)
    )