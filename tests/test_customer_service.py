from src.application.services.customer_service import CustomerService
from tests.fakes import FakeCustomerRepository

def test_create_customer():
    repo = FakeCustomerRepository()
    service = CustomerService(repo)
    result = service.create_customer("John Doe", "john.doe@example.com")
    assert result.name == "John Doe"
    assert result.email == "john.doe@example.com"