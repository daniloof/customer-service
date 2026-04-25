from uuid import UUID

class Address:
    def __init__(self,
                 id: UUID,
                 customer_id: UUID,
                 street: str,
                 city: str,
                 state: str,
                 zip_code: str):
        self.id = id
        self.customer_id = customer_id
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code