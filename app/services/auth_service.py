from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest


class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def register(self, data: RegisterRequest) -> User:
        if self.repository.get_by_email(data.email):
            raise ConflictError("User with this email already exists")

        return self.repository.create(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
        )

    def login(self, data: LoginRequest) -> str:
        user = self.repository.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")

        if not user.is_active:
            raise UnauthorizedError("User account is inactive")

        return create_access_token(subject=str(user.id))
