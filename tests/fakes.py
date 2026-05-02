from src.domain.entities import Customer, Address

class FakeCustomerRepository:
    def __init__(self):
        self.customers = {}

    def create(self, name, email):
        customer = Customer(id="123", name=name, email=email, addresses=[])
        self.customers[customer.id] = customer
        return customer
    
    def list(self):
        return self.customers
    
    def get_by_id(self, customer_id):
        for customer in self.customers:
            if customer.id == customer_id:
                return customer
        return None
    
class FakeAddressRepository:
    def __init__(self):
        self.addresses = []

    def create(self, customer_id, street, city, state, zip_code):
        address = Address(id="999", customer_id=customer_id, street=street, city=city, state=state, zip_code=zip_code)
        self.addresses.append(address)
        return address