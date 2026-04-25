from src.domain.entities.address import Address
from src.adapters.outbound.db.models import AddressModel

def to_domain(model: AddressModel) -> Address:
    return Address(
        id=model.id,
        customer_id=model.customer_id,
        street=model.street,
        city=model.city,
        state=model.state,
        zip_code=model.zip_code
    )