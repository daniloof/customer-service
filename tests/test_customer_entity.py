from src.domain.entities import Customer, Address
import pytest

def test_customer_add_address():
    # Arrange
    customer = Customer(id="123", name="John Doe", email="john.doe@example.com", addresses=[])
    address = Address(id="999", customer_id="123", street="Rua A", city="São Paulo", state="SP", zip_code="09000-000")

    # Act
    customer.add_address(address)

    # Assert
    assert len(customer.addresses) == 1
    assert customer.addresses[0] == address

def test_customer_name_required():
    with pytest.raises(ValueError):
        Customer(id="123", name="", email="john@example.com")

def test_customer_max_addresses():
    customer = Customer(id="123", name="John", email="john@example.com")
    for i in range(3):
        customer.add_address(Address(id=str(i), customer_id="123",
                             street="Rua A", city="SP", state="SP", zip_code="09000000"))
    with pytest.raises(ValueError):
        customer.add_address(Address(id="4", customer_id="123",
                             street="Rua B", city="SP", state="SP", zip_code="09000000"))