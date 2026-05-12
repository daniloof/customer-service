import pytest
from src.domain.entities.customer import Customer
from src.domain.entities.address import Address
from src.domain.exceptions import RequiredFieldError, InvalidZipCodeError

def test_customer_add_address():
    customer = Customer(id="123", name="John Doe", email="john@example.com")
    address = Address(id="999", customer_id="123", street="Rua A",
                      city="São Paulo", state="SP", zip_code="09000000")
    customer.add_address(address)
    assert len(customer.addresses) == 1
    assert customer.addresses[0] == address

def test_customer_name_required():
    with pytest.raises(RequiredFieldError):  # ← era ValueError
        Customer(id="123", name="", email="john@example.com")

def test_customer_name_whitespace():
    with pytest.raises(RequiredFieldError):  # ← era ValueError
        Customer(id="123", name="   ", email="john@example.com")

def test_customer_max_three_addresses():
    customer = Customer(id="123", name="John", email="john@example.com")
    for i in range(3):
        customer.add_address(
            Address(id=str(i), customer_id="123", street="Rua A",
                    city="SP", state="SP", zip_code="09000000")
        )
    with pytest.raises(ValueError):
        customer.add_address(
            Address(id="4", customer_id="123", street="Rua B",
                    city="SP", state="SP", zip_code="09000000")
        )

def test_address_invalid_zip_code():
    with pytest.raises(InvalidZipCodeError):
        Address(id="1", customer_id="123", street="Rua A",
                city="SP", state="SP", zip_code="123")