from .base import DomainError

class EmailAlreadyExistsError(DomainError):
    def __init__(self, email):
        super().__init__(f"Email already exists: {email}")

class CustomerNotFoundError(DomainError):
    """Raised when a customer is not found."""
    def __init__(self, customer_id):
        super().__init__(f"Customer not found: {customer_id}")