from src.application.services.customer_service import CustomerService
from tests.fakes import FakeCustomerRepository
import pytest
from src.domain.exceptions import CustomerNotFoundError

def test_create_customer():
    repo = FakeCustomerRepository()
    service = CustomerService(repo)
    result = service.create_customer("John Doe", "john.doe@example.com")
    assert result.name == "John Doe"
    assert result.email == "john.doe@example.com"

def test_list_customers():
    repo = FakeCustomerRepository()
    service = CustomerService(repo)
    service.create_customer("John", "john@example.com")
    service.create_customer("Jane", "jane@example.com")

    result = service.list_customer()

    assert len(result) == 2
    assert result[0].name == "John"
    assert result[1].name == "Jane"

def test_get_customer_success():
    repo = FakeCustomerRepository()
    service = CustomerService(repo)
    created = service.create_customer("John", "john@example.com")

    result = service.get_customer(created.id)

    assert result.id == created.id
    assert result.name == "John"

def test_get_customer_not_found():
    repo = FakeCustomerRepository()
    service = CustomerService(repo)

    with pytest.raises(CustomerNotFoundError):
        service.get_customer("id-not-found")