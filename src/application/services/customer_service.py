from src.infrastructure.db.session import SessionLocal
from src.adapters.outbound.db.models import CustomerModel

def create_customer(name:str, email:str):
    db = SessionLocal()

    try:
        customer = CustomerModel(
            name=name,
            email=email
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer
    finally:
        db.close()