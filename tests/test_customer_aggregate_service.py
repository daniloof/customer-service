import pytest
from src.application.services.customer_aggregate_service import CustomerAggregateService
from tests.fakes import FakeCustomerRepository, FakeAddressRepository
from src.domain.exceptions import CustomerNotFoundError


def test_add_address_to_customer():
    # Arrange
    customer_repo = FakeCustomerRepository()
    address_repo = FakeAddressRepository()
    
    customer = customer_repo.create("John Doe", "john.doe@example.com")

    service = CustomerAggregateService(customer_repo, address_repo)

    result = service.add_address_to_customer(customer.id,
                                             "Rua A",
                                             "São Paulo",
                                             "SP",
                                             "09000-000")

    assert result.customer_id == customer.id
    assert result.street == "Rua A"
    assert result.city == "São Paulo"
    assert result.state == "SP"
    assert result.zip_code == "09000-000"

def test_add_address_to_nonexistent_customer():
    # Arrange
    customer_repo = FakeCustomerRepository()
    address_repo = FakeAddressRepository()

    service = CustomerAggregateService(customer_repo, address_repo)

    with pytest.raises(CustomerNotFoundError):
        service.add_address_to_customer(999,  # Non-existent customer ID
                                       "Rua A",
                                       "São Paulo",
                                       "SP",
                                       "09000-000")