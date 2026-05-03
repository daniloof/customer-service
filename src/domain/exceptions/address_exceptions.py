from .base import DomainError

class AddressNotFoundError(DomainError):
    """Raised when an address is not found."""
    def __init__(self, address_id):
        super().__init__(f"Address not found: {address_id}")

class InvalidZipCodeError(DomainError):
    """Raised when a zip code is invalid."""
    def __init__(self, zip_code):
        super().__init__(f"Invalid zip code: {zip_code}")