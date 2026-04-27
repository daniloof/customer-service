from sqlalchemy.orm import Session
from src.domain.ports.address_repository import AddressRepository
from src.adapters.outbound.db.models import AddressModel
from src.adapters.outbound.db.mappers.address_mapper import to_domain

class AddressRepositoryImpl(AddressRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, customer_id, street, city, state, zip_code):
        address = AddressModel(
            customer_id=customer_id,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        self.db.add(address)
        self.db.flush()  # Ensure the address gets an ID before refreshing
        self.db.refresh(address)

        return to_domain(address)
    
    def list_by_customer(self, customer_id):
        models = self.db.query(AddressModel).filter_by(customer_id=customer_id).all()
        return [to_domain(m) for m in models]