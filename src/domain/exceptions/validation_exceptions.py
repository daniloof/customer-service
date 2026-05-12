from .base import DomainError

class ValidationError(DomainError):
    """Base para erros de validação."""
    pass

class InvalidFieldError(ValidationError):
    def __init__(self, field: str, reason: str):
        super().__init__(f"Invalid field '{field}': {reason}")

class RequiredFieldError(ValidationError):
    def __init__(self, field: str):
        super().__init__(f"Field '{field}' is required")