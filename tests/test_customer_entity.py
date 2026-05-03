from src.domain.entities import Customer, Address

def test_customer_add_address():
    # Arrange
    customer = Customer(id="123", name="John Doe", email="john.doe@example.com", addresses=[])
    address = Address(id="999", customer_id="123", street="Rua A", city="São Paulo", state="SP", zip_code="09000-000")

    # Act
    customer.add_address(address)

    # Assert
    assert len(customer.addresses) == 1
    assert customer.addresses[0] == address