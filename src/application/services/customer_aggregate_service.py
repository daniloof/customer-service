from src.domain.entities import Address
from src.domain.ports.customer_repository import CustomerRepository
from src.domain.ports.address_repository import AddressRepository
from src.domain.exceptions import CustomerNotFoundError, AddressNotFoundError

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
            raise CustomerNotFoundError(customer_id)
            
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
    
    def delete_address(self, customer_id, address_id):  # ← novo
        customer = self.customer_repository.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundError(customer_id)

        address = self.address_repository.get_by_id(address_id)
        if not address:
            raise AddressNotFoundError(address_id)

        self.address_repository.delete(address_id)