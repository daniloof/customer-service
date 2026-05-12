from sqlalchemy.orm import Session
from src.domain.ports.user_repository import UserRepository
from src.adapters.outbound.db.models import UserModel
from src.adapters.outbound.db.mappers.user_mapper import to_domain

class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_google_id(self, google_id: str):
        model = self.db.query(UserModel).filter(
            UserModel.google_id == google_id
        ).first()
        if not model:
            return None
        return to_domain(model)

    def get_by_email(self, email: str):
        model = self.db.query(UserModel).filter(
            UserModel.email == email
        ).first()
        if not model:
            return None
        return to_domain(model)

    def create(self, google_id: str, name: str, email: str):
        user = UserModel(google_id=google_id, name=name, email=email)
        self.db.add(user)
        self.db.flush()
        self.db.refresh(user)
        return to_domain(user)