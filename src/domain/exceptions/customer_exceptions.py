from .base import DomainError

class EmailAlreadyExistsError(DomainError):
    """Raised when trying to create a customer with an email that already exists."""
    pass

class CustomerNotFoundError(DomainError):
    """Raised when a customer is not found."""
    def __init__(self, customer_id):
        super().__init__(f"Customer not found: {customer_id}")