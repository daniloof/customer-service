from uuid import uuid4
from src.domain.entities import Customer, Address

class FakeCustomerRepository:
    def __init__(self):
        self.customers = []

    def create(self, name, email):
        customer = Customer(id=str(uuid4()), name=name, email=email, addresses=[])
        self.customers.append(customer)
        return customer

    def list(self):
        return self.customers

    def get_by_id(self, customer_id):
        for customer in self.customers:
            if customer.id == customer_id:
                return customer
        return None

    def get_by_email(self, email: str):  # ← adicionado
        for customer in self.customers:
            if customer.email == email:
                return customer
        return None


class FakeAddressRepository:
    def __init__(self):
        self.addresses = []

    def create(self, customer_id, street, city, state, zip_code):
        address = Address(id=str(uuid4()), customer_id=customer_id, street=street, city=city, state=state, zip_code=zip_code)
        self.addresses.append(address)
        return address