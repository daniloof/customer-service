from src.domain.ports.customer_repository import CustomerRepository
from src.application.dto.customer_dto import CustomerDTO
from src.domain.entities.address import Address
from src.domain.ports.address_repository import AddressRepository

class CustomerService:
    def __init__(
        self,
        customer_repository: CustomerRepository,
        address_repository: AddressRepository
    ):
        self.repository = customer_repository
        self.address_repository = address_repository

    def create_customer(self, name: str, email: str):
        customer = self.repository.create(name, email)

        return CustomerDTO(
        id=customer.id,
        name=customer.name,
        email=customer.email
    )
    
    def list_customer(self):
        customers = self.repository.list()

        return [
            CustomerDTO(
                id=c.id,
                name=c.name,
                email=c.email
            )
            for c in customers
        ]
       
    def add_address_to_customer(self, customer_id, street, city, state, zip_code):
        customer = self.repository.get_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")

        address = Address(
            id=None,
            customer_id=customer_id,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        customer.add_address(address)

        saved = self.address_repository.create(
            customer_id,
            street,
            city,
            state,
            zip_code
        )

        return saved