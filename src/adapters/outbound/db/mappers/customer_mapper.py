from src.domain.entities.customer import Customer
from src.adapters.outbound.db.models import CustomerModel

def to_domain(model: CustomerModel) -> Customer:
    return Customer(
        id=model.id,
        name=model.name,
        email=model.email
    )