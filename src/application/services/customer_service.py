from src.domain.ports.customer_repository import CustomerRepository
from src.application.dto.customer_dto import CustomerDTO

class CustomerService:
    def __init__(self, repository:CustomerRepository):
        self.repository = repository

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