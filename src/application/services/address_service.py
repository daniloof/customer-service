from src.domain.ports.address_repository import AddressRepository
from src.application.dto.address_dto import AddressDTO

class AddressService:
    def __init__(self, repository: AddressRepository):
        self.repository = repository

    def create_address(self, customer_id, street, city, state, zip_code):
        address = self.repository.create(customer_id, street, city, state, zip_code)
        return AddressDTO(
            id=address.id,
            customer_id=address.customer_id,
            street=address.street,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code
        )

    def list_addresses_by_customer(self, customer_id):
        addresses = self.repository.list_by_customer(customer_id)
        return [
            AddressDTO(
                id=a.id,
                customer_id=a.customer_id,
                street=a.street,
                city=a.city,
                state=a.state,
                zip_code=a.zip_code
            ) for a in addresses
        ]   