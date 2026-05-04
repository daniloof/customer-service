# src/domain/entities/address.py
import re
from uuid import UUID
from src.domain.exceptions import InvalidZipCodeError
class Address:
    def __init__(self,
                 id: UUID,
                 customer_id: UUID,
                 street: str,
                 city: str,
                 state: str,
                 zip_code: str):

        clean_zip = re.sub(r"\D", "", zip_code)
        if not clean_zip.isdigit() or len(clean_zip) != 8:
            raise InvalidZipCodeError(zip_code)

        self.id = id
        self.customer_id = customer_id
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code