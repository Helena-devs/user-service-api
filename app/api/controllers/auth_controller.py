from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService


class AuthController:
    def __init__(self, db: Session):
        self.service = AuthService(db)

    def register(self, data: RegisterRequest) -> UserResponse:
        user = self.service.register(data)
        return UserResponse.model_validate(user)

    def login(self, data: LoginRequest) -> TokenResponse:
        token = self.service.login(data)
        return TokenResponse(access_token=token)
