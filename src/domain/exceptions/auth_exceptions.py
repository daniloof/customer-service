from src.domain.exceptions.base import DomainError

class InvalidTokenError(DomainError):
    def __init__(self):
        super().__init__("Invalid or expired token")

class UnauthorizedError(DomainError):
    def __init__(self):
        super().__init__("Unauthorized")

class InvalidGoogleTokenError(DomainError):
    def __init__(self):
        super().__init__("Invalid Google token")