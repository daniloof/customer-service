from src.domain.entities.address import Address
from src.domain.ports.customer_repository import CustomerRepository
from src.domain.ports.address_repository import AddressRepository

class CustomerAggregateService:
    def __init__(
        self,
        customer_repository: CustomerRepository,
        address_repository: AddressRepository
    ):
        self.customer_repository = customer_repository
        self.address_repository = address_repository

    def add_address_to_customer(self,
                                   customer_id, 
                                   street,
                                   city,
                                   state,
                                   zip_code):
        
        customer = self.customer_repository.get_by_id(customer_id)

        if not customer:
            raise ValueError("Customer not found")
                    # Create the address and associate it with the customer
            
        address = Address(
            id=None,
            customer_id=customer_id,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )

        customer.add_address(address)

        saved = self.address_repository.create(customer_id,
                                               street,
                                               city,
                                               state,
                                               zip_code)

        return saved