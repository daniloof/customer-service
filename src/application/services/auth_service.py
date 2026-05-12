import os
import httpx
from datetime import datetime, timedelta, timezone  # Adicionado timezone
from jose import jwt, JWTError

from src.domain.ports.user_repository import UserRepository
from src.domain.exceptions.auth_exceptions import (
    InvalidTokenError,
    InvalidGoogleTokenError
)
from src.application.dto.user_dto import UserDTO, TokenDTO

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.repository = user_repository

    def authenticate_with_google(self, google_token: str) -> TokenDTO:
        user_info = self._verify_google_token(google_token)

        user = self.repository.get_by_google_id(user_info["sub"])
        if not user:
            user = self.repository.create(
                google_id=user_info["sub"],
                name=user_info["name"],
                email=user_info["email"]
            )

        return self._generate_tokens(user)

    def refresh_access_token(self, refresh_token: str) -> TokenDTO:
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != "refresh":
                raise InvalidTokenError()

            user = self.repository.get_by_google_id(payload["sub"])
            if not user:
                raise InvalidTokenError()

            return self._generate_tokens(user)
        except JWTError:
            raise InvalidTokenError()

    def verify_access_token(self, token: str) -> UserDTO:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != "access":
                raise InvalidTokenError()

            return UserDTO(
                id=payload["user_id"],
                name=payload["name"],
                email=payload["email"]
            )
        except JWTError:
            raise InvalidTokenError()

    def _verify_google_token(self, token: str) -> dict:
        try:
            response = httpx.get(
                GOOGLE_TOKEN_INFO_URL,
                params={"id_token": token}
            )
            if response.status_code != 200:
                raise InvalidGoogleTokenError()

            data = response.json()

            if data.get("aud") != GOOGLE_CLIENT_ID:
                raise InvalidGoogleTokenError()

            return data
        except httpx.RequestError:
            raise InvalidGoogleTokenError()

    def _generate_tokens(self, user) -> TokenDTO:
        access_token = self._create_token(
            data={
                "sub": user.google_id,
                "user_id": str(user.id),
                "name": user.name,
                "email": user.email,
                "type": "access"
            },
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = self._create_token(
            data={
                "sub": user.google_id,
                "type": "refresh"
            },
            expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
        return TokenDTO(access_token=access_token, refresh_token=refresh_token)

    def _create_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        # Alteração aqui: datetime.now(timezone.utc) substitui o utcnow()
        to_encode["exp"] = datetime.now(timezone.utc) + expires_delta
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
