from src.domain.entities.user import User
from src.adapters.outbound.db.models import UserModel

def to_domain(model: UserModel) -> User:
    return User(
        id=model.id,
        google_id=model.google_id,
        name=model.name,
        email=model.email
    )