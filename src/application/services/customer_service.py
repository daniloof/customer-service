from src.domain.ports.customer_repository import CustomerRepository
from src.application.dto.customer_dto import CustomerDTO
from src.application.dto.address_dto import AddressDTO
from src.domain.exceptions import CustomerNotFoundError, EmailAlreadyExistsError

class CustomerService:
    def __init__(self, customer_repository: CustomerRepository):
        self.repository = customer_repository

    def create_customer(self, name: str, email: str):
        existing = self.repository.get_by_email(email)  # ← verifica antes de inserir
        if existing:
            raise EmailAlreadyExistsError(email)

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

    def get_customer(self, customer_id):
        customer = self.repository.get_by_id(customer_id)

        if not customer:
            raise CustomerNotFoundError(customer_id)

        return CustomerDTO(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            addresses=[
                AddressDTO(
                    id=a.id,
                    customer_id=a.customer_id,
                    street=a.street,
                    city=a.city,
                    state=a.state,
                    zip_code=a.zip_code
                )
                for a in customer.addresses
            ]
        )