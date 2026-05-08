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
    
    def update(self, customer_id, name: str, email: str):  # ← novo
        for customer in self.customers:
            if str(customer.id) == str(customer_id):
                customer.name = name
                customer.email = email
                return customer
        return None

    def delete(self, customer_id):  # ← novo
        self.customers = [
            c for c in self.customers
            if str(c.id) != str(customer_id)
        ]


class FakeAddressRepository:
    def __init__(self):
        self.addresses = []

    def create(self, customer_id, street, city, state, zip_code):
        address = Address(id=str(uuid4()), customer_id=customer_id, street=street, city=city, state=state, zip_code=zip_code)
        self.addresses.append(address)
        return address
    
    def get_by_id(self, address_id):  # ← novo
        for address in self.addresses:
            if str(address.id) == str(address_id):
                return address
        return None

    def delete(self, address_id):  # ← novo
        self.addresses = [
            a for a in self.addresses
            if str(a.id) != str(address_id)
        ]