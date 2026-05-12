from .base import DomainError
from .validation_exceptions import ValidationError

class AddressNotFoundError(DomainError):
    def __init__(self, address_id):
        super().__init__(f"Address not found: {address_id}")

class InvalidZipCodeError(ValidationError):  # ← mudança aqui
    def __init__(self, zip_code):
        super().__init__(f"Invalid zip code: {zip_code}")