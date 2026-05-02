from .base import DomainError

class AddressNotFoundError(DomainError):
    """Raised when an address is not found."""
    def __init__(self, address_id):
        super().__init__(f"Address not found: {address_id}")

class InvalidZipCodeError(DomainError):
    """Raised when an invalid zip code is provided."""
    pass