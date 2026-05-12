from uuid import UUID
from src.domain.exceptions import RequiredFieldError

class User:
    def __init__(self, id: UUID, google_id: str, name: str, email: str):
        if not google_id or not google_id.strip():
            raise RequiredFieldError("google_id")
        if not name or not name.strip():
            raise RequiredFieldError("name")
        if not email or not email.strip():
            raise RequiredFieldError("email")

        self.id = id
        self.google_id = google_id.strip()
        self.name = name.strip()
        self.email = email.strip().lower()