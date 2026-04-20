from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.adapters.outbound.db.models import CustomerModel
from src.domain.exceptions import EmailAlreadyExistsError

def create_customer(db:Session, name:str, email:str) -> CustomerModel:
    try:
        customer = CustomerModel(name=name,email=email)
        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer
    except IntegrityError as e:
        db.rollback()

        if "unique" in str(e.orig).lower():
            raise EmailAlreadyExistsError()
        raise

def get_customers(db:Session):
    return db.query(CustomerModel).all()