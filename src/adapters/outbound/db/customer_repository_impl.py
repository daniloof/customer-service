from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.domain.ports.customer_repository import CustomerRepository
from src.adapters.outbound.db.models import CustomerModel
from src.adapters.outbound.db.mappers.customer_mapper import to_domain
from src.domain.exceptions import EmailAlreadyExistsError

class CustomerRepositoryImpl(CustomerRepository):
    def __init__(self, db:Session):
        self.db = db

    def create(self, name, email):
        try:
            customer = CustomerModel(name=name, email=email)
            self.db.add(customer)
            self.db.flush()  # Ensure the customer gets an ID before refreshing
            self.db.refresh(customer)

            return to_domain(customer)
        except IntegrityError as e:
            if "unique" in str(e.orig).lower():
                raise EmailAlreadyExistsError()
            raise

    def list(self):
        models = self.db.query(CustomerModel).all()
        return [to_domain(m) for m in models]
    
    def get_by_id(self, customer_id):
        model = self.db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
        if not model:
            return None
        return to_domain(model)