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
            self.db.commit()
            self.db.refresh(customer)

            return to_domain(customer)
        except IntegrityError as e:
            self.db.rollback()
            if "unique" in str(e.orig).lower():
                raise EmailAlreadyExistsError()
            raise

    def list(self):
        models = self.db.query(CustomerModel).all()
        return [to_domain(m) for m in models]