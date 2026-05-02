from src.domain.entities import Customer
from src.adapters.outbound.db.models import CustomerModel
from src.adapters.outbound.db.mappers.address_mapper import to_domain as address_to_domain

def to_domain(model: CustomerModel):
    return Customer(
        id=model.id,
        name=model.name,
        email=model.email,
        addresses=[address_to_domain(a) for a in model.addresses]
    )