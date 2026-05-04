from sqlalchemy.orm import Session
from src.domain.ports.customer_repository import CustomerRepository
from src.adapters.outbound.db.models import CustomerModel
from src.adapters.outbound.db.mappers.customer_mapper import to_domain

class CustomerRepositoryImpl(CustomerRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, email: str):
        customer = CustomerModel(name=name, email=email)
        self.db.add(customer)
        self.db.flush()
        self.db.refresh(customer)
        return to_domain(customer)

    def list(self):
        models = self.db.query(CustomerModel).all()
        return [to_domain(m) for m in models]

    def get_by_id(self, customer_id):
        model = self.db.query(CustomerModel).filter(
            CustomerModel.id == customer_id
        ).first()
        if not model:
            return None
        return to_domain(model)

    def get_by_email(self, email: str):  # ← adicionado
        model = self.db.query(CustomerModel).filter(
            CustomerModel.email == email
        ).first()
        if not model:
            return None
        return to_domain(model)